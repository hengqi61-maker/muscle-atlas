import fs from "node:fs";
import crypto from "node:crypto";
import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";
import { Matrix4, Vector3, Quaternion } from "three";
import { HandRigAdapter } from "../../src/grasp-v2/HandRigAdapter";
import { GraspSolver } from "../../src/grasp-v2/GraspSolver";
import { ContactValidator } from "../../src/grasp-v2/ContactValidator";
const bytes = fs.readFileSync("artifacts/grasp-v2/controller-motion.glb"),
  g = await new GLTFLoader().parseAsync(
    bytes.buffer.slice(bytes.byteOffset, bytes.byteOffset + bytes.byteLength),
    "",
  );
const rigs = {
    Left: new HandRigAdapter(g.scene, "Left"),
    Right: new HandRigAdapter(g.scene, "Right"),
  },
  rows = [],
  cases = [],
  rest: Record<string, number[]> = {};
g.scene.updateMatrixWorld(true);
for (const r of Object.values(rigs))
  for (const j of r.joints) rest[j.bone.name] = j.bone.matrixWorld.toArray();
for (const amount of [0, 0.2, 0.45, 0.7, 1]) {
  const pose: Record<string, { x: number; y: number; z: number }> = {},
    matrices: Record<string, number[]> = {};
  for (const r of Object.values(rigs)) {
    r.apply(r.preset(amount), amount * 0.55);
    for (const j of r.joints) {
      pose[j.bone.name] = {
        x: j.max * amount,
        y:
          j.digit === "Thumb" && j.index === 0
            ? amount * 0.55 * (r.side === "Left" ? 1 : -1)
            : 0,
        z: 0,
      };
      matrices[j.bone.name] = j.bone.matrixWorld.toArray();
    }
  }
  cases.push({ name: `v2-${amount}`, pose });
  rows.push({ name: `v2-${amount}`, matrices });
}
const solverRows = [];
for (const r of Object.values(rigs)) {
  const solver = new GraspSolver(r);
  for (const [radius, y, z] of [
    [0.008, 0.025, 0.035],
    [0.016, 0.04, 0.02],
    [0.024, 0.055, 0.02],
    [0.04, 0.085, 0.02],
  ]) {
    r.reset();
    const matrix = r.socket.matrixWorld
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
      position = new Vector3(),
      quaternion = new Quaternion(),
      scale = new Vector3();
    matrix.decompose(position, quaternion, scale);
    matrix.compose(position, quaternion, new Vector3(1, 1, 1));
    const h = { matrix, radius, halfLength: 0.065, kind: "dumbbell" as const };
    const result = solver.solve(h, r.preset(0.6), 0.5, 32);
    const pose: Record<string, { x: number; y: number; z: number }> = {},
      matrices: Record<string, number[]> = {};
    for (const j of r.joints) {
      pose[j.bone.name] = {
        x: result.pose[j.bone.name],
        y:
          j.digit === "Thumb" && j.index === 0
            ? result.opposition * (r.side === "Left" ? 1 : -1)
            : 0,
        z: 0,
      };
      matrices[j.bone.name] = j.bone.matrixWorld.toArray();
    }
    const name = `solver-${r.side}-${radius}`;
    cases.push({ name, pose });
    rows.push({ name, matrices });
    solverRows.push({ side: r.side, radius, ...result });
  }
}
fs.writeFileSync(
  "artifacts/grasp-v2/numerical.json",
  JSON.stringify(
    {
      assetSha256: crypto.createHash("sha256").update(bytes).digest("hex"),
      solverRows,
    },
    null,
    2,
  ),
);
console.log("wrote numeric inputs and results");

fs.writeFileSync(
  "artifacts/grasp-v2/pose-input.json",
  JSON.stringify(cases, null, 2),
);
fs.writeFileSync(
  "artifacts/grasp-v2/three-matrices.json",
  JSON.stringify({ rest, rows }, null, 2),
);
