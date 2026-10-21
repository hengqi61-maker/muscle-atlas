import { Vector3 } from "three";
export interface Plane {
  n: Vector3;
  d: number;
}
/** Port of Windows contact_geometry.py triangle_contact, a8247a4. */
export function triangleContact(
  triangle: Vector3[],
  planes: Plane[],
  tolerance = 1e-4,
) {
  let poly = triangle.map((p) => p.clone());
  const gap = Math.max(
    ...planes.map((p) => Math.min(...poly.map((v) => p.n.dot(v) - p.d))),
  );
  if (gap > tolerance)
    return { classification: "disjoint", gapLowerBoundM: gap };
  for (const { n, d } of planes) {
    if (!poly.length) break;
    const output: Vector3[] = [];
    for (let i = 0; i < poly.length; i++) {
      const a = poly[i],
        b = poly[(i + 1) % poly.length],
        da = n.dot(a) - d,
        db = n.dot(b) - d;
      if (da <= tolerance) output.push(a);
      if (da <= tolerance !== db <= tolerance)
        output.push(a.clone().lerp(b, (tolerance - da) / (db - da)));
    }
    poly = output;
  }
  if (!poly.length)
    return { classification: "disjoint", gapLowerBoundM: Math.max(0, gap) };
  const witness = poly
      .reduce((a, b) => a.add(b), new Vector3())
      .divideScalar(poly.length),
    depth = Math.min(...planes.map((p) => p.d - p.n.dot(witness)));
  return {
    classification:
      depth > tolerance ? "penetration-candidate" : "surface-contact",
    positionM: witness.toArray(),
    depthLowerBoundM: Math.max(0, depth),
    toleranceM: tolerance,
  };
}
