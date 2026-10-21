import {
  AxesHelper,
  Float32BufferAttribute,
  BufferGeometry,
  CylinderGeometry,
  Group,
  LineBasicMaterial,
  LineSegments,
  Matrix4,
  Mesh,
  MeshStandardMaterial,
  Object3D,
  Quaternion,
  Vector3,
} from "three";
import { GripAnchor } from "./GripAnchor";
import { HandRigAdapter, type Pose, type Side } from "./HandRigAdapter";
import { GraspSolver } from "./GraspSolver";
import { HandPoseLayer } from "./HandPoseLayer";
import { ContactValidator, type Handle } from "./ContactValidator";
import { useGrasp } from "./store";
import config from "../data/pulldown-config.json";
export let activeRuntime: GraspRuntime | null = null;
export class GraspRuntime {
  anchors: Record<Side, GripAnchor>;
  anchored = { Left: false, Right: false };
  rigs: Record<Side, HandRigAdapter>;
  layers: Record<Side, HandPoseLayer>;
  solvers: Record<Side, GraspSolver>;
  validator = new ContactValidator();
  visual = new Group();
  handles: Record<Side, Mesh>;
  axes: AxesHelper[] = [];
  lines: LineSegments;
  lastSolve = -Infinity;
  lastReport = -Infinity;
  lastRevision = -1;
  results: Record<string, unknown> = {};
  restHandle: Record<Side, Matrix4>;
  lastTime = -1;
  wasTransitioning = false;
  constructor(readonly root: Object3D) {
    activeRuntime = this;
    this.rigs = {
      Left: new HandRigAdapter(root, "Left"),
      Right: new HandRigAdapter(root, "Right"),
    };
    this.anchors = {
      Left: new GripAnchor(this.rigs.Left),
      Right: new GripAnchor(this.rigs.Right),
    };
    this.layers = {
      Left: new HandPoseLayer(this.rigs.Left),
      Right: new HandPoseLayer(this.rigs.Right),
    };
    this.solvers = {
      Left: new GraspSolver(this.rigs.Left),
      Right: new GraspSolver(this.rigs.Right),
    };
    this.handles = {
      Left: new Mesh(
        new CylinderGeometry(1, 1, 2, 12),
        new MeshStandardMaterial({
          color: "#8ba5b8",
          metalness: 0.8,
          roughness: 0.3,
        }),
      ),
      Right: new Mesh(
        new CylinderGeometry(1, 1, 2, 12),
        new MeshStandardMaterial({
          color: "#8ba5b8",
          metalness: 0.8,
          roughness: 0.3,
        }),
      ),
    };
    for (const side of ["Left", "Right"] as Side[])
      this.visual.add(this.handles[side]);
    this.lines = new LineSegments(
      new BufferGeometry(),
      new LineBasicMaterial({ vertexColors: true, depthTest: false }),
    );
    this.visual.add(this.lines);
    root.add(this.visual);
    this.restHandle = {
      Left: this.rigs.Left.frame(),
      Right: this.rigs.Right.frame(),
    };
    for (const rig of Object.values(this.rigs))
      for (const j of rig.joints) {
        const axis = new AxesHelper(0.015);
        j.bone.add(axis);
        this.axes.push(axis);
      }
  }
  get needsUpdate() {
    return (
      this.lastRevision !== useGrasp.getState().revision ||
      Object.values(this.layers).some((l) => l.transitioning)
    );
  }
  beforeMixer() {
    for (const a of Object.values(this.anchors)) a.beforeMixer();
    for (const l of Object.values(this.layers)) l.beforeMixer();
  }
  handle(side: Side, time: number): Handle {
    const s = useGrasp.getState(),
      sign = side === "Left" ? 1 : -1;
    let matrix: Matrix4, halfLength: number;
    if (s.kind === "bar") {
      const barY =
          config.barTopY -
          (config.barTravel * (1 - Math.cos((time / 4) * 2 * Math.PI))) / 2,
        from = new Vector3(sign * 0.32, barY - 0.01575, config.gripZ),
        to = new Vector3(sign * 0.46, barY - 0.126, config.gripZ);
      halfLength = from.distanceTo(to) / 2;
      const center = from.clone().add(to).multiplyScalar(0.5);
      center.z += s.offset;
      matrix = new Matrix4().compose(
        center,
        new Quaternion().setFromUnitVectors(
          new Vector3(0, 1, 0),
          to.sub(from).normalize(),
        ),
        new Vector3(1, 1, 1),
      );
    } else {
      halfLength = s.kind === "dumbbell" ? 0.065 : 0.035;
      this.rigs[side].socket.updateWorldMatrix(true, false);
      matrix = this.rigs[side].socket.matrixWorld.clone();
      const offset = new Matrix4().compose(
        new Vector3(
          0,
          0.01 + 1.875 * s.radius,
          Math.min(s.radius + 0.004, 0.02) + s.offset,
        ),
        new Quaternion().setFromAxisAngle(new Vector3(0, 0, 1), Math.PI / 2),
        new Vector3(1, 1, 1),
      );
      matrix.multiply(offset);
      const p = new Vector3(),
        q = new Quaternion(),
        scale = new Vector3();
      matrix.decompose(p, q, scale);
      matrix.compose(p, q, new Vector3(1, 1, 1));
    }
    return { matrix, radius: s.radius, halfLength, kind: s.kind };
  }
  update(time: number, delta: number, now: number) {
    const s = useGrasp.getState(),
      changed = s.revision !== this.lastRevision,
      seek = Math.abs(time - this.lastTime) > 0.15 || time < this.lastTime;
    const due =
      changed || time !== this.lastTime || now - this.lastSolve > 0.12;
    const visualPoints: Vector3[] = [],
      visualColors: number[] = [];
    const report: Record<string, unknown> = {
      axisProvenance: this.rigs.Left.axisProvenance,
    };
    for (const side of ["Left", "Right"] as Side[]) {
      const rig = this.rigs[side],
        layer = this.layers[side],
        control = s.hands[side],
        h = this.handle(side, time);
      if (control.anchor && !control.released) {
        if (!this.anchored[side]) this.anchors[side].capture(h.matrix);
        this.anchored[side] = true;
      } else {
        this.anchors[side].release();
        this.anchored[side] = false;
      }
      const anchor = this.anchors[side].update(h.matrix);
      layer.captureAnimation();
      this.handles[side].matrixAutoUpdate = false;
      this.handles[side].matrix
        .copy(h.matrix)
        .premultiply(this.root.matrixWorld.clone().invert())
        .scale(new Vector3(h.radius, h.halfLength, h.radius));
      if (control.released) layer.release();
      else if (control.auto && due) {
        const result = this.solvers[side].solve(
          h,
          layer.pose,
          control.opposition,
          changed ? 12 : 5,
        );
        layer.set(result.pose, result.opposition);
        this.results[side] = {
          status: result.status,
          residualM: result.residualM,
          evaluations: result.evaluations,
          sweeps: result.sweeps,
        };
      } else if (!control.auto) {
        const pose: Pose = {};
        for (const j of rig.joints)
          pose[j.bone.name] =
            control.joints[j.bone.name] ?? j.max * control.digits[j.digit];
        layer.set(pose, control.opposition);
        this.results[side] = { status: "MANUAL" };
      }
      layer.afterMixer(delta, seek, false);
      const proxy = this.validator.proxy(rig, h, layer.pose);
      for (const [i, seg] of rig.segments().entries()) {
        visualPoints.push(
          this.root.worldToLocal(seg.from),
          this.root.worldToLocal(seg.to),
        );
        const row = proxy.segments[i],
          color = row.penetrating
            ? [1, 0.2, 0.2]
            : row.contact
              ? [0.2, 1, 0.5]
              : [1, 0.75, 0.2];
        visualColors.push(...color, ...color);
      }
      report[side] = {
        ...(this.results[side] as object),
        anchor,
        jointAngles: layer.pose,
        proxy: proxy.status,
        maxGapM: Math.max(...proxy.segments.map((v) => v.gapM)),
        penetratingSegments: proxy.segments.filter((v) => v.penetrating).length,
      };
      if (changed || now - this.lastReport > 1) {
        const tissue = this.validator.tissue(this.root, h, side);
        (report[side] as Record<string, unknown>).tissue = tissue;
      }
    }
    if (due) this.lastSolve = now;
    for (const a of this.axes) a.visible = s.axes;
    this.lines.visible = s.axes;
    this.lines.geometry.dispose();
    this.lines.geometry = new BufferGeometry().setFromPoints(visualPoints);
    this.lines.geometry.setAttribute(
      "color",
      new Float32BufferAttribute(visualColors, 3),
    );
    const transitioning = Object.values(this.layers).some(
      (l) => l.transitioning,
    );
    const finished = this.wasTransitioning && !transitioning;
    if (finished) {
      for (const side of ["Left", "Right"] as Side[])
        (report[side] as Record<string, unknown>).tissue =
          this.validator.tissue(this.root, this.handle(side, time), side);
    }
    this.wasTransitioning = transitioning;
    if (changed || finished || now - this.lastReport > 1) {
      useGrasp.setState({
        report: { ...report, geometryStatus: "GEOMETRY_INSUFFICIENT", time },
      });
      this.lastReport = now;
    }
    this.lastRevision = s.revision;
    this.lastTime = time;
  }
  dispose() {
    if (activeRuntime === this) activeRuntime = null;
    for (const a of this.axes) {
      a.removeFromParent();
      a.dispose();
    }
    this.visual.removeFromParent();
    this.lines.geometry.dispose();
    (this.lines.material as LineBasicMaterial).dispose();
    for (const h of Object.values(this.handles)) {
      h.geometry.dispose();
      (h.material as MeshStandardMaterial).dispose();
    }
  }
}
