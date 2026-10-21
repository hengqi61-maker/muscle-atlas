import fs from "node:fs";
import { Matrix4 } from "three";
const dir = "artifacts/grasp-v2",
  native = JSON.parse(fs.readFileSync(dir + "/native/blender-reference.json")),
  three = JSON.parse(fs.readFileSync(dir + "/three-matrices.json"));
const rows = [];
for (const r of three.rows) {
  const n = native.cases.find((c) => c.name === r.name);
  let matrix = 0,
    origin = 0;
  for (const [name, values] of Object.entries(r.matrices)) {
    const m = n.matrices[name],
      a = new Matrix4()
        .fromArray(values)
        .multiply(new Matrix4().fromArray(three.rest[name]).invert()),
      b = new Matrix4()
        .fromArray(m)
        .multiply(new Matrix4().fromArray(native.rest[name]).invert());
    matrix = Math.max(
      matrix,
      ...a.elements.map((v, i) => Math.abs(v - b.elements[i])),
    );
    origin = Math.max(
      origin,
      Math.hypot(values[12] - m[12], values[13] - m[13], values[14] - m[14]),
    );
  }
  rows.push({
    name: r.name,
    maxDeformationMatrixError: matrix,
    maxJointOriginErrorM: origin,
  });
}
const tolerance = 64 * 2 ** -23,
  result = {
    status: rows.every(
      (r) =>
        r.maxDeformationMatrixError < tolerance &&
        r.maxJointOriginErrorM < tolerance,
    )
      ? "PASS"
      : "FAIL",
    blender: native.blender,
    tolerance,
    scope:
      "actual v2 adapter vs native Blender, deformation matrices cancel importer bone frame conventions",
    rows,
  };
fs.writeFileSync(dir + "/blender-parity.json", JSON.stringify(result, null, 2));
console.log(result);
if (result.status === "FAIL") process.exitCode = 1;
