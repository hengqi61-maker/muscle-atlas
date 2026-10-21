// Add original shared-rig clips without rewriting any byte of PR21's source BIN.
import fs from "node:fs";
import crypto from "node:crypto";
const parse = (p) => {
  const b = fs.readFileSync(p),
    len = b.readUInt32LE(12);
  return {
    b,
    j: JSON.parse(b.subarray(20, 20 + len)),
    bin: b.subarray(28 + len),
  };
};
const a = parse("artifacts/grasp-v1/grasp-controller.glb"),
  d = parse("public/experimental/rig-v2/unified-rig-prototype.glb");
const names = new Map(a.j.nodes.map((n, i) => [n.name, i])),
  used = new Set(
    d.j.animations.flatMap((c) => c.channels.map((c) => c.target.node)),
  );
let maxReferenceError = 0;
for (const i of used) {
  const src = d.j.nodes[i],
    dst = a.j.nodes[names.get(src.name)];
  if (!dst) throw Error("missing " + src.name);
  for (const key of ["translation", "rotation", "scale"]) {
    const defaults =
        key === "rotation"
          ? [0, 0, 0, 1]
          : key === "scale"
            ? [1, 1, 1]
            : [0, 0, 0],
      x = src[key] ?? defaults,
      y = dst[key] ?? defaults,
      error = Math.max(...x.map((v, k) => Math.abs(v - y[k])));
    maxReferenceError = Math.max(maxReferenceError, error);
    if (error > 64 * 2 ** -23)
      throw Error("incompatible reference " + src.name + " " + key);
  }
}
const chunks = [a.bin],
  views = new Map(),
  accessors = new Map();
let length = a.bin.length;
function accessor(index) {
  if (accessors.has(index)) return accessors.get(index);
  const acc = d.j.accessors[index];
  if (acc.sparse) throw Error("Sparse animation unsupported");
  if (!views.has(acc.bufferView)) {
    const v = d.j.bufferViews[acc.bufferView],
      pad = (4 - (length % 4)) % 4;
    if (pad) {
      chunks.push(Buffer.alloc(pad));
      length += pad;
    }
    const view = a.j.bufferViews.length;
    views.set(acc.bufferView, view);
    a.j.bufferViews.push({ ...v, byteOffset: length });
    const data = d.bin.subarray(
      v.byteOffset ?? 0,
      (v.byteOffset ?? 0) + v.byteLength,
    );
    chunks.push(data);
    length += data.length;
  }
  const next = a.j.accessors.length;
  accessors.set(index, next);
  a.j.accessors.push({ ...acc, bufferView: views.get(acc.bufferView) });
  return next;
}
a.j.animations = d.j.animations.map((c) => ({
  ...c,
  samplers: c.samplers.map((s) => ({
    ...s,
    input: accessor(s.input),
    output: accessor(s.output),
  })),
  channels: c.channels.map((c) => ({
    ...c,
    target: { ...c.target, node: names.get(d.j.nodes[c.target.node].name) },
  })),
}));
const pad = (4 - (length % 4)) % 4;
if (pad) chunks.push(Buffer.alloc(pad));
const bin = Buffer.concat(chunks);
a.j.buffers = [{ byteLength: bin.length }];
let json = Buffer.from(JSON.stringify(a.j));
json = Buffer.concat([json, Buffer.alloc((4 - (json.length % 4)) % 4, 32)]);
const out = Buffer.alloc(12 + 8 + json.length + 8 + bin.length);
out.writeUInt32LE(0x46546c67, 0);
out.writeUInt32LE(2, 4);
out.writeUInt32LE(out.length, 8);
out.writeUInt32LE(json.length, 12);
out.writeUInt32LE(0x4e4f534a, 16);
json.copy(out, 20);
out.writeUInt32LE(bin.length, 20 + json.length);
out.writeUInt32LE(0x004e4942, 24 + json.length);
bin.copy(out, 28 + json.length);
fs.mkdirSync("artifacts/grasp-v2", { recursive: true });
fs.writeFileSync("artifacts/grasp-v2/controller-motion.glb", out);
const sha = (b) => crypto.createHash("sha256").update(b).digest("hex");
const report = {
  sourceSha256: sha(a.b),
  donorSha256: sha(d.b),
  outputSha256: sha(out),
  bytes: out.length,
  maxReferenceError,
  originalBufferPrefixIdentical: bin.subarray(0, a.bin.length).equals(a.bin),
  channels: a.j.animations.map((a) => ({
    name: a.name,
    channels: a.channels.length,
  })),
};
fs.writeFileSync(
  "artifacts/grasp-v2/assembly.json",
  JSON.stringify(report, null, 2),
);
console.log(JSON.stringify(report, null, 2));
