import fs from "node:fs";
import crypto from "node:crypto";
import validator from "gltf-validator";
const read = (p) => {
  const bytes = fs.readFileSync(p),
    len = bytes.readUInt32LE(12);
  return {
    bytes,
    json: JSON.parse(bytes.subarray(20, 20 + len)),
    bin: bytes.subarray(28 + len),
  };
};
const src = read("artifacts/grasp-v1/grasp-controller.glb"),
  out = read("artifacts/grasp-v2/controller-motion.glb");
const sha = (b) => crypto.createHash("sha256").update(b).digest("hex");
const a = (g, i) => {
  const ac = g.json.accessors[i],
    v = g.json.bufferViews[ac.bufferView],
    sizes = { 5121: 1, 5123: 2, 5125: 4, 5126: 4 },
    dim = { SCALAR: 1, VEC2: 2, VEC3: 3, VEC4: 4, MAT4: 16 },
    start = (v.byteOffset ?? 0) + (ac.byteOffset ?? 0);
  return g.bin.subarray(
    start,
    start + ac.count * sizes[ac.componentType] * dim[ac.type],
  );
};
const positions = src.json.meshes.map((m, i) => ({
  name: m.name,
  sha256: sha(a(src, m.primitives[0].attributes.POSITION)),
  unchanged: a(src, m.primitives[0].attributes.POSITION).equals(
    a(out, out.json.meshes[i].primitives[0].attributes.POSITION),
  ),
}));
const counts = Object.fromEntries(
  src.json.skins[0].joints.map((i) => [src.json.nodes[i].name, 0]),
);
for (const m of src.json.meshes)
  for (const p of m.primitives) {
    if (p.attributes.JOINTS_0 === undefined) continue;
    const ja = src.json.accessors[p.attributes.JOINTS_0],
      jb = a(src, p.attributes.JOINTS_0),
      wb = a(src, p.attributes.WEIGHTS_0),
      wa = src.json.accessors[p.attributes.WEIGHTS_0];
    for (let i = 0; i < ja.count * 4; i++) {
      const joint =
          ja.componentType === 5121 ? jb.readUInt8(i) : jb.readUInt16LE(i * 2),
        weight =
          wa.componentType === 5126
            ? wb.readFloatLE(i * 4)
            : wa.componentType === 5121
              ? wb.readUInt8(i) / 255
              : wb.readUInt16LE(i * 2) / 65535;
      if (weight > 0)
        counts[src.json.nodes[src.json.skins[0].joints[joint]].name]++;
    }
  }
const finger = Object.entries(counts).filter(([name]) =>
  /^(Left|Right)(Thumb|Index|Middle|Ring|Little)(CMC|MCP|PIP|DIP|IP)$/.test(
    name,
  ),
);
const baseline = await validator.validateBytes(new Uint8Array(src.bytes), {}),
  v = await validator.validateBytes(new Uint8Array(out.bytes), {}),
  report = {
    assetSha256: sha(out.bytes),
    sourceSha256: sha(src.bytes),
    allPositionsUnchanged: positions.every((r) => r.unchanged),
    sourceMeshes: src.json.nodes.filter((n) => n.extras?.sourceName).length,
    positions,
    fingerInfluences: Object.fromEntries(finger),
    zeroInfluence: finger.filter(([, n]) => !n).map(([name]) => name),
    baselineValidator: baseline.issues,
    validator: v.issues,
  };
fs.writeFileSync(
  "artifacts/grasp-v2/asset-audit.json",
  JSON.stringify(report, null, 2),
);
console.log({
  allPositionsUnchanged: report.allPositionsUnchanged,
  sourceMeshes: report.sourceMeshes,
  zeroInfluence: report.zeroInfluence.length,
  errors: v.issues.numErrors,
  warnings: v.issues.numWarnings,
});
if (!report.allPositionsUnchanged || v.issues.numErrors) process.exitCode = 1;
