import { Matrix4, Mesh, Object3D, SkinnedMesh, Vector3 } from "three";
import { triangleContact, type Plane } from "./convexContact";
import type { HandRigAdapter, Pose } from "./HandRigAdapter";
export interface Handle {
  matrix: Matrix4;
  radius: number;
  halfLength: number;
  kind: "bar" | "dumbbell" | "rope";
}
export const CONTACT_TOLERANCE = 0.0001,
  PENETRATION_TOLERANCE = 0.0001;
export function validateHandle(h: Handle) {
  if (
    !Number.isFinite(h.radius) ||
    !Number.isFinite(h.halfLength) ||
    h.radius <= 0 ||
    h.halfLength <= 0 ||
    !h.matrix.elements.every(Number.isFinite) ||
    Math.abs(h.matrix.determinant()) < 1e-12
  )
    throw Error("INVALID_HANDLE");
}
/** Exact SDF of closed finite cylinder, local Y axis, metre units. Rigid metric frame required. */
export function prepareCylinder(h: Handle) {
  validateHandle(h);
  const scale = new Vector3().setFromMatrixScale(h.matrix);
  if (Math.max(...scale.toArray().map((v) => Math.abs(v - 1))) > 1e-5)
    throw Error("NON_METRIC_HANDLE");
  const e = h.matrix.clone().invert().elements;
  return (p: Vector3) => {
    const x = e[0] * p.x + e[4] * p.y + e[8] * p.z + e[12],
      y = e[1] * p.x + e[5] * p.y + e[9] * p.z + e[13],
      z = e[2] * p.x + e[6] * p.y + e[10] * p.z + e[14];
    const r = Math.hypot(x, z) - h.radius,
      a = Math.abs(y) - h.halfLength;
    return (
      Math.hypot(Math.max(r, 0), Math.max(a, 0)) + Math.min(Math.max(r, a), 0)
    );
  };
}
export function signedCylinder(p: Vector3, h: Handle) {
  return prepareCylinder(h)(p);
}
/** Bounded convex SDF minimum, endpoints included. Prepared metric transform is shared. */
export function capsuleGap(
  from: Vector3,
  to: Vector3,
  radius: number,
  h: Handle,
  sdf = prepareCylinder(h),
) {
  const point = new Vector3(),
    at = (t: number) => sdf(point.copy(from).lerp(to, t));
  let lo = 0,
    hi = 1;
  for (let i = 0; i < 32; i++) {
    const a = (2 * lo + hi) / 3,
      b = (lo + 2 * hi) / 3;
    if (at(a) < at(b)) hi = b;
    else lo = a;
  }
  return Math.min(at(0), at(1), at((lo + hi) / 2)) - radius;
}
export class ContactValidator {
  proxy(rig: HandRigAdapter, h: Handle, pose: Pose) {
    validateHandle(h);
    const sdf = prepareCylinder(h);
    const segments = rig.segments().map((s) => {
      const min = capsuleGap(s.from, s.to, s.radius, h, sdf);
      return {
        name: s.name,
        digit: s.digit,
        index: s.index,
        gapM: min,
        contact: Math.abs(min) <= CONTACT_TOLERANCE,
        penetrating: min < -PENETRATION_TOLERANCE,
      };
    });
    const violation = rig.joints.some(
      (j) =>
        !Number.isFinite(pose[j.bone.name]) ||
        pose[j.bone.name] < j.min ||
        pose[j.bone.name] > j.max,
    );
    const allDigits = ["Thumb", "Index", "Middle", "Ring", "Little"].every(
      (d) => segments.some((s) => s.digit === d && s.contact),
    );
    return {
      status: violation
        ? "JOINT_LIMIT"
        : segments.some((s) => s.penetrating)
          ? "PENETRATION"
          : allDigits
            ? "PROXY_CONTACT"
            : "GAP",
      method:
        "bounded 32-step capsule centerline/cylinder SDF minimization; 4mm radius proxy only, not actual tissue",
      segments,
      jointLimit: violation,
    };
  }
  private rest = new WeakMap<Mesh, Vector3[]>();
  /** Actual posed source vertices and triangles; witness-only collision. Absence never proves mesh contact. */
  tissue(root: Object3D, h: Handle, side: string) {
    validateHandle(h);
    let vertices = 0,
      triangles = 0,
      inside = 0,
      intersections = 0,
      min = Infinity,
      maxEdgeRatio = 1,
      collapsed = 0,
      flipped = 0;
    const sdf = prepareCylinder(h);
    const inv = h.matrix.clone().invert(),
      planes: Plane[] = [
        { n: new Vector3(0, 1, 0), d: h.halfLength },
        { n: new Vector3(0, -1, 0), d: h.halfLength },
      ];
    for (let k = 0; k < 12; k++) {
      const angle = ((k + 0.5) * 2 * Math.PI) / 12;
      planes.push({
        n: new Vector3(Math.cos(angle), 0, Math.sin(angle)),
        d: h.radius * Math.cos(Math.PI / 12),
      });
    }
    const meshes: Mesh[] = [];
    root.traverse((o) => {
      if (
        o instanceof Mesh &&
        o.userData.sourceName &&
        new RegExp(side, "i").test(String(o.userData.sourceName)) &&
        /hand|pollicis|lumbrical|interosse|digiti minimi/i.test(
          String(o.userData.sourceName),
        ) &&
        !/foot|halluc|plantar/i.test(String(o.userData.sourceName))
      )
        meshes.push(o);
    });
    for (const m of meshes) {
      const attr = m.geometry.attributes.position;
      if (!this.rest.has(m))
        this.rest.set(
          m,
          Array.from({ length: attr.count }, (_, i) =>
            new Vector3().fromBufferAttribute(attr, i),
          ),
        );
      const rest = this.rest.get(m)!;
      if (m instanceof SkinnedMesh) m.skeleton.update();
      const posed = rest.map((_, i) => m.getVertexPosition(i, new Vector3()));
      for (const p of posed) {
        const d = sdf(p.clone().applyMatrix4(m.matrixWorld));
        min = Math.min(min, d);
        if (d < -PENETRATION_TOLERANCE) inside++;
        vertices++;
      }
      const idx = m.geometry.index,
        n = idx?.count ?? attr.count,
        at = (i: number) => (idx ? idx.getX(i) : i);
      for (let i = 0; i < n; i += 3) {
        const ids = [at(i), at(i + 1), at(i + 2)];
        const [a, b, c] = ids.map((k) => posed[k]),
          [ra, rb, rc] = ids.map((k) => rest[k]);
        const rn = rb.clone().sub(ra).cross(rc.clone().sub(ra)),
          pn = b.clone().sub(a).cross(c.clone().sub(a));
        triangles++;
        if (
          triangleContact(
            [a, b, c].map((v) =>
              v.clone().applyMatrix4(m.matrixWorld).applyMatrix4(inv),
            ),
            planes,
          ).classification === "penetration-candidate"
        )
          intersections++;
        if (rn.lengthSq() > 4e-24 && pn.length() / rn.length() < 0.05)
          collapsed++;
        // Compare against skin-transformed rest normal to avoid treating rigid rotation as inversion.
        if (m instanceof SkinnedMesh) {
          const origin = ra.clone(),
            normalEnd = ra
              .clone()
              .add(rn.clone().normalize().multiplyScalar(0.001));
          const expected = m
            .applyBoneTransform(ids[0], normalEnd)
            .sub(m.applyBoneTransform(ids[0], origin));
          if (expected.dot(pn) < 0) flipped++;
        }
        for (let k = 0; k < 3; k++) {
          const r = rest[ids[k]].distanceTo(rest[ids[(k + 1) % 3]]);
          if (r > 1e-6)
            maxEdgeRatio = Math.max(
              maxEdgeRatio,
              posed[ids[k]].distanceTo(posed[ids[(k + 1) % 3]]) / r,
            );
        }
      }
    }
    return {
      kernel: "Windows contact-v1.1 a8247a4 triangle_contact port",
      status:
        inside || intersections || collapsed || flipped || maxEdgeRatio > 2
          ? "FAIL_TISSUE_GRASP"
          : "GEOMETRY_INSUFFICIENT",
      geometryStatus: "GEOMETRY_INSUFFICIENT",
      sourceSideAttribution:
        "source-label-only; anatomical/spatial sidedness unverified",
      reason:
        "Original source muscle/tendon meshes lack validated fingertip pad surfaces; no positive tissue grasp possible.",
      vertices,
      triangles,
      penetratingVertices: inside,
      penetratingTriangles: intersections,
      minSignedM: Number.isFinite(min) ? min : null,
      maxEdgeRatio,
      collapsedTriangles: collapsed,
      flippedTriangles: flipped,
      method:
        "all selected source vertices and triangles; inversion relative to local skin transform; finite 12-gon closed convex triangle clipping; lower-bound depth, not exact MTV",
    };
  }
}
