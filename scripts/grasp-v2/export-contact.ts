/** Offline Windows packet-v1.1 adapter. Source triangles preserved; calibration remains unknown. */
import fs from "node:fs";
import crypto from "node:crypto";
import { execFileSync } from "node:child_process";
import { CylinderGeometry, Matrix4, Mesh, SkinnedMesh, Vector3 } from "three";
import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";
const hash = (b: Buffer) => crypto.createHash("sha256").update(b).digest("hex");
function geometryHash(v: number[][], t: number[][]) {
  const bytes = Buffer.alloc(v.length * 24 + t.length * 12);
  let o = 0;
  for (const p of v)
    for (const x of p) {
      bytes.writeDoubleLE(x, o);
      o += 8;
    }
  for (const row of t)
    for (const x of row) {
      bytes.writeUInt32LE(x, o);
      o += 4;
    }
  return hash(bytes);
}
const b = fs.readFileSync("artifacts/grasp-v2/controller-motion.glb"),
  g = await new GLTFLoader().parseAsync(
    b.buffer.slice(b.byteOffset, b.byteOffset + b.byteLength),
    "",
  );
g.scene.updateMatrixWorld(true);
const geometry = new CylinderGeometry(0.024, 0.024, 0.13, 12),
  v = Array.from({ length: geometry.attributes.position.count }, (_, i) =>
    new Vector3()
      .fromBufferAttribute(geometry.attributes.position, i)
      .toArray(),
  ),
  t = Array.from({ length: geometry.index!.count / 3 }, (_, i) =>
    [0, 1, 2].map((k) => geometry.index!.getX(i * 3 + k)),
  );
const hands = [];
for (const side of ["left", "right"]) {
  const sources: object[] = [];
  g.scene.traverse((o) => {
    const name = String(o.userData.sourceName ?? "");
    if (
      !(o instanceof Mesh) ||
      !name.includes(side) ||
      !/hand|pollicis|lumbrical|interosse|digiti minimi/i.test(name) ||
      /foot|halluc|plantar/i.test(name)
    )
      return;
    if (o instanceof SkinnedMesh) o.skeleton.update();
    const p = o.geometry.attributes.position,
      idx = o.geometry.index,
      verts = Array.from({ length: p.count }, (_, i) =>
        o
          .getVertexPosition(i, new Vector3())
          .applyMatrix4(o.matrixWorld)
          .toArray(),
      ),
      triangles = Array.from({ length: (idx?.count ?? p.count) / 3 }, (_, i) =>
        [0, 1, 2].map((k) => (idx ? idx.getX(i * 3 + k) : i * 3 + k)),
      );
    const raw = Array.from({ length: p.count }, (_, i) =>
      new Vector3().fromBufferAttribute(p, i).toArray(),
    );
    sources.push({
      sourceId: name,
      originalMeshSha256: geometryHash(raw, triangles),
      posedWorldVertices: verts,
      triangles,
      originalTriangleIds: triangles.map((_, i) => i),
      geometryKind: "actual-source-triangles",
      region: "hand-other",
      posedGeometrySha256: geometryHash(verts, triangles),
    });
  });
  hands.push({
    side,
    skeletonId: "PR21-57-joint-additive",
    wristWorldMatrix: null,
    palmWorldMatrix: null,
    handWorldMatrix: null,
    sources,
    frameStatus: "unknown",
    independentlyExported: false,
  });
}
const packet = {
  schemaVersion: "1.1.0",
  coordinates: "right-handed-metres-seconds-column-major-active",
  variant: "grasp-v2-rest",
  provenance:
    "PR21 additive source rig; runtime geometry export, not independent anatomical calibration",
  toleranceM: 0.0001,
  inputProvenance: {
    producerCommit: execFileSync("git", ["rev-parse", "HEAD"], {
      encoding: "utf8",
    }).trim(),
    assetSha256: hash(b),
    originalAssetSha256: hash(
      fs.readFileSync("artifacts/grasp-v1/grasp-controller.glb"),
    ),
    coordinateFrame: "glTF RH Y-up metres",
    hashSerialization: "float64-le-xyz-then-uint32-le-triples",
    evidenceKind: "legacy-unverified",
  },
  timeline: {
    clipId: "rest",
    durationSeconds: 0,
    expectedTimesSeconds: [0],
    interpolation: "sampled-only",
    scope: "discrete-samples-not-continuous-collision",
  },
  samples: [
    {
      timeSeconds: 0,
      prop: {
        id: "v2-finite-dumbbell-handle",
        worldMatrix: new Matrix4().makeTranslation(0.25, 0.8, 0.1).toArray(),
        dimensionsM: [0.048, 0.13, 0.048],
        vertices: v,
        triangles: t,
        geometryKind: "actual-convex-mesh",
        geometrySha256: geometryHash(v, t),
      },
      hands,
    },
  ],
};
fs.writeFileSync(
  "artifacts/grasp-v2/contact-v1.1.json",
  JSON.stringify(packet),
);
console.log("contact-v1.1 exported; unknown calibration is intentional");
