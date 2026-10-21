import fs from "node:fs";
import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";
import { Matrix4, Quaternion, Vector3 } from "three";
import { HandRigAdapter } from "../../src/grasp-v2/HandRigAdapter";
import { GraspSolver } from "../../src/grasp-v2/GraspSolver";
const b = fs.readFileSync("artifacts/grasp-v2/controller-motion.glb"),
  g = await new GLTFLoader().parseAsync(
    b.buffer.slice(b.byteOffset, b.byteOffset + b.byteLength),
    "",
  );
const r = new HandRigAdapter(g.scene, "Left"),
  solver = new GraspSolver(r);
const rows = [];
r.reset();
const frame = r.socket.matrixWorld.clone();
for (const radius of [0.008, 0.016, 0.024])
  for (const y of [0.025, 0.04, 0.055])
    for (const z of [0.008, 0.02, 0.035]) {
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
        );
      const p = new Vector3(),
        q = new Quaternion(),
        s = new Vector3();
      matrix.decompose(p, q, s);
      matrix.compose(p, q, new Vector3(1, 1, 1));
      const result = solver.solve(
        { matrix, radius, halfLength: 0.065, kind: "dumbbell" },
        r.preset(0.6),
        0.5,
        32,
      );
      rows.push({
        radius,
        y,
        z,
        status: result.status,
        residualM: result.residualM,
        contacts: result.contact.segments
          .filter((s) => s.contact)
          .map((s) => s.name),
        penetration: result.contact.segments.filter((s) => s.penetrating)
          .length,
      });
    }
fs.writeFileSync(
  "artifacts/grasp-v2/reach-probe.json",
  JSON.stringify(rows, null, 2),
);
console.log(rows.sort((a, b) => a.residualM - b.residualM).slice(0, 5));
