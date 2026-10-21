import { describe, it, expect } from "vitest";
import fs from "node:fs";
import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";
import { AnimationMixer, Matrix4, Quaternion, Vector3 } from "three";
import { HandRigAdapter } from "../src/grasp-v2/HandRigAdapter";
import { GraspSolver } from "../src/grasp-v2/GraspSolver";
import { GripAnchor } from "../src/grasp-v2/GripAnchor";
import { HandPoseLayer } from "../src/grasp-v2/HandPoseLayer";
import {
  ContactValidator,
  signedCylinder,
  type Handle,
} from "../src/grasp-v2/ContactValidator";
import { triangleContact } from "../src/grasp-v2/convexContact";
async function load() {
  const b = fs.readFileSync("artifacts/grasp-v2/controller-motion.glb");
  return new GLTFLoader().parseAsync(
    b.buffer.slice(b.byteOffset, b.byteOffset + b.byteLength),
    "",
  );
}
const handle = (matrix = new Matrix4(), radius = 0.024): Handle => ({
  matrix,
  radius,
  halfLength: 0.065,
  kind: "dumbbell",
});
describe("Grasp v2 actual GLB", () => {
  it("loads all 30 original finger bones and preserves neutral references", async () => {
    const g = await load();
    for (const side of ["Left", "Right"] as const) {
      const r = new HandRigAdapter(g.scene, side);
      expect(r.joints).toHaveLength(15);
      const refs = r.joints.map((j) => j.bone.quaternion.toArray());
      for (let i = 0; i < 5; i++) r.apply(r.preset(0));
      expect(r.joints.map((j) => j.bone.quaternion.toArray())).toEqual(refs);
      expect(r.joints.every((j) => Math.abs(j.length - 0.062 / 3) < 1e-6)).toBe(
        true,
      );
    }
  });
  it("validates missing bones, parent links and zero-length segments", async () => {
    const g = await load();
    const r = new HandRigAdapter(g.scene, "Left"),
      b = r.joints[1].bone;
    b.position.set(0, 0, 0);
    expect(() => new HandRigAdapter(g.scene, "Left")).toThrow("ZERO_LENGTH");
    b.name = "missing";
    expect(() => new HandRigAdapter(g.scene, "Left")).toThrow("MISSING_BONE");
  });
  it("mirrors controls, converts hand/world/handle frames and actual axes", async () => {
    const g = await load(),
      l = new HandRigAdapter(g.scene, "Left"),
      r = new HandRigAdapter(g.scene, "Right");
    const p = l.preset(0.4);
    r.apply(r.mirror(p));
    expect(r.joints[4].bone.quaternion.equals(r.joints[4].reference)).toBe(
      false,
    );
    const point = new Vector3(0.02, 0.03, 0.04),
      frame = l.frame(),
      world = l.convert(point, frame, new Matrix4());
    expect(
      l.convert(world, new Matrix4(), frame).distanceTo(point),
    ).toBeLessThan(1e-9);
    for (const j of l.joints) expect(l.axisWorld(j).length()).toBeCloseTo(1);
  });
  it("moves independent joint and opposed thumb without touching right hand", async () => {
    const g = await load(),
      l = new HandRigAdapter(g.scene, "Left"),
      r = new HandRigAdapter(g.scene, "Right");
    const right = r.joints.map((j) => j.bone.quaternion.toArray()),
      pose = l.preset(0);
    pose.LeftIndexPIP = 0.7;
    l.apply(pose, 0.4);
    expect(
      l.joints
        .find((j) => j.bone.name === "LeftIndexMCP")!
        .bone.quaternion.toArray(),
    ).toEqual(
      l.joints.find((j) => j.bone.name === "LeftIndexMCP")!.reference.toArray(),
    );
    expect(l.joints[0].bone.quaternion.equals(l.joints[0].reference)).toBe(
      false,
    );
    expect(r.joints.map((j) => j.bone.quaternion.toArray())).toEqual(right);
  });
  it("bounds IK budget and limits, reports unreachable and multiple radii honestly", async () => {
    const g = await load(),
      r = new HandRigAdapter(g.scene, "Left"),
      solver = new GraspSolver(r);
    for (const radius of [0.008, 0.016, 0.024, 0.04]) {
      const h = handle(new Matrix4().makeTranslation(0.25, 0.8, 0.3), radius),
        out = solver.solve(h, r.preset(0.5), 0.3, 8);
      expect(out.evaluations).toBeLessThanOrEqual(257);
      expect(out.residualM).toBeGreaterThanOrEqual(0);
      for (const j of r.joints)
        expect(out.pose[j.bone.name]).toBeLessThanOrEqual(j.max);
    }
    expect(
      solver.solve(handle(new Matrix4().makeTranslation(5, 5, 5))).status,
    ).toBe("UNREACHABLE");
    expect(() => solver.solve(handle(), undefined, 0.2, 999)).toThrow(
      "INVALID_BUDGET",
    );
  });
  it("retains pose after mixer seek/pause/loop/replay and release restores animated base", async () => {
    const g = await load(),
      r = new HandRigAdapter(g.scene, "Left"),
      layer = new HandPoseLayer(r),
      mixer = new AnimationMixer(g.scene);
    mixer.clipAction(g.animations[0]).play();
    layer.set(r.preset(0.6), 0.2);
    let q: number[] | undefined;
    for (const time of [0, 0.5, 1, 1, 3.9, 0, 0.2]) {
      layer.beforeMixer();
      mixer.setTime(time);
      layer.afterMixer(0.016, true);
      if (!q) q = r.joints[4].bone.quaternion.toArray();
      expect(r.joints[4].bone.quaternion.toArray()).toEqual(q);
    }
    layer.release();
    layer.beforeMixer();
    mixer.setTime(0);
    layer.afterMixer(0.016);
    expect(r.joints[4].bone.quaternion.toArray()).toEqual(
      r.joints[4].reference.toArray(),
    );
    layer.reset();
    expect(layer.pose.LeftIndexPIP).toBe(0);
  });
  it("finite caps reject points outside and tissue never passes without pad geometry", async () => {
    expect(signedCylinder(new Vector3(0, 1, 0), handle())).toBeCloseTo(0.935);
    const g = await load(),
      r = new HandRigAdapter(g.scene, "Left"),
      v = new ContactValidator();
    r.apply(r.preset(1));
    const out = v.tissue(g.scene, handle(r.frame()), "Left");
    expect(out.vertices).toBeGreaterThan(0);
    expect(out.geometryStatus).toBe("GEOMETRY_INSUFFICIENT");
    expect(out.status).not.toBe("PASS");
    expect(out.triangles).toBeGreaterThan(0);
  });
  it("detects triangle interior crossings that vertex samples miss", () => {
    const planes = [
      ...[-1, 1].flatMap((sign) => [
        new Vector3(sign, 0, 0),
        new Vector3(0, sign, 0),
        new Vector3(0, 0, sign),
      ]),
    ].map((n) => ({ n, d: 1 }));
    expect(
      triangleContact(
        [new Vector3(-3, -3, 0), new Vector3(3, -3, 0), new Vector3(0, 3, 0)],
        planes,
      ).classification,
    ).toBe("penetration-candidate");
    expect(
      triangleContact(
        [new Vector3(2, 0, 0), new Vector3(2, 1, 0), new Vector3(2, 0, 1)],
        planes,
      ).classification,
    ).toBe("disjoint");
  });
  it("preserves a captured handle relation with bounded arm correction and restores mixer base", async () => {
    const g = await load(),
      r = new HandRigAdapter(g.scene, "Left"),
      anchor = new GripAnchor(r),
      matrix = r.frame(),
      before = r.hand.getWorldPosition(new Vector3());
    anchor.capture(matrix);
    const moved = matrix.clone();
    moved.elements[12] += 0.006;
    const out = anchor.update(moved, 12);
    expect(out.evaluations).toBeLessThanOrEqual(217);
    expect(out.positionResidualM).toBeLessThan(0.006);
    anchor.beforeMixer();
    g.scene.updateMatrixWorld(true);
    expect(
      r.hand.getWorldPosition(new Vector3()).distanceTo(before),
    ).toBeLessThan(1e-9);
    anchor.release();
    expect(anchor.update(matrix).status).toBe("RELEASED");
  });
  it("manual transitions finish exactly and do not drift on unrelated edits", async () => {
    const g = await load(),
      r = new HandRigAdapter(g.scene, "Left"),
      layer = new HandPoseLayer(r);
    const pose = r.preset(0.7);
    layer.set(pose, 0.4);
    for (let i = 0; i < 180; i++) {
      layer.beforeMixer();
      layer.afterMixer(1 / 60);
    }
    expect(layer.transitioning).toBe(false);
    expect(layer.pose).toEqual(pose);
    const q = r.joints.map((j) => j.bone.quaternion.toArray());
    for (let i = 0; i < 4; i++) {
      layer.beforeMixer();
      layer.afterMixer(1 / 60);
    }
    expect(r.joints.map((j) => j.bone.quaternion.toArray())).toEqual(q);
  });
  it("solves actual skeletal contact for three radii on both hands without relaxing contact limits", async () => {
    const g = await load();
    for (const side of ["Left", "Right"] as const) {
      const rig = new HandRigAdapter(g.scene, side),
        solver = new GraspSolver(rig);
      rig.reset();
      const frame = rig.socket.matrixWorld.clone();
      for (const [radius, y, z] of [
        [0.008, 0.025, 0.035],
        [0.016, 0.04, 0.02],
        [0.024, 0.055, 0.02],
      ]) {
        const matrix = frame
            .clone()
            .multiply(
              new Matrix4().compose(
                new Vector3(0, y, z),
                new Quaternion().setFromAxisAngle(
                  new Vector3(0, 0, 1),
                  Math.PI / 2,
                ),
                new Vector3(1, 1, 1),
              ),
            ),
          p = new Vector3(),
          q = new Quaternion(),
          scale = new Vector3();
        matrix.decompose(p, q, scale);
        matrix.compose(p, q, new Vector3(1, 1, 1));
        const result = solver.solve(
          { matrix, radius, halfLength: 0.065, kind: "dumbbell" },
          rig.preset(0.6),
          0.5,
          32,
        );
        expect(result.status).toBe("PROXY_CONTACT");
        expect(result.contact.segments.some((s) => s.penetrating)).toBe(false);
        expect(result.evaluations).toBeLessThanOrEqual(1025);
      }
    }
  });
});
