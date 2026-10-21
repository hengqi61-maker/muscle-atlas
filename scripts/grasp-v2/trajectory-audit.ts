import fs from "node:fs";
import { AnimationMixer, Matrix4, Quaternion, Vector3 } from "three";
import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";
import { HandRigAdapter } from "../../src/grasp-v2/HandRigAdapter";
import { HandPoseLayer } from "../../src/grasp-v2/HandPoseLayer";
import { GraspSolver } from "../../src/grasp-v2/GraspSolver";
import { ContactValidator } from "../../src/grasp-v2/ContactValidator";
const bytes = fs.readFileSync("artifacts/grasp-v2/controller-motion.glb");
const rows = [];
for (const clipName of ["CurlProbe", "PulldownProbe"]) {
  const g = await new GLTFLoader().parseAsync(
    bytes.buffer.slice(bytes.byteOffset, bytes.byteOffset + bytes.byteLength),
    "",
  );
  const mixer = new AnimationMixer(g.scene),
    clip = g.animations.find((c) => c.name === clipName)!;
  mixer.clipAction(clip).play();
  const rigs = {
      Left: new HandRigAdapter(g.scene, "Left"),
      Right: new HandRigAdapter(g.scene, "Right"),
    },
    layers = {
      Left: new HandPoseLayer(rigs.Left),
      Right: new HandPoseLayer(rigs.Right),
    },
    validator = new ContactValidator();
  for (let frame = 0; frame <= 120; frame++) {
    const time = (frame / 120) * clip.duration;
    for (const l of Object.values(layers)) l.beforeMixer();
    mixer.setTime(time === clip.duration ? time - 1e-8 : time);
    g.scene.updateMatrixWorld(true);
    for (const side of ["Left", "Right"] as const) {
      const rig = rigs[side],
        layer = layers[side];
      layer.captureAnimation();
      const matrix = rig.socket.matrixWorld
          .clone()
          .multiply(
            new Matrix4().compose(
              new Vector3(0, 0.055, 0.02),
              new Quaternion().setFromAxisAngle(
                new Vector3(0, 0, 1),
                Math.PI / 2,
              ),
              new Vector3(1, 1, 1),
            ),
          ),
        p = new Vector3(),
        q = new Quaternion(),
        s = new Vector3();
      matrix.decompose(p, q, s);
      matrix.compose(p, q, new Vector3(1, 1, 1));
      const handle = {
          matrix,
          radius: 0.024,
          halfLength: 0.065,
          kind: "dumbbell" as const,
        },
        result = new GraspSolver(rig).solve(handle, rig.preset(0.6), 0.5, 32);
      layer.set(result.pose, result.opposition);
      layer.afterMixer(0.016, true, false);
      const contact = validator.proxy(rig, handle, result.pose),
        tissue = validator.tissue(g.scene, handle, side);
      rows.push({
        clip: clipName,
        frame,
        time,
        side,
        solver: result.status,
        proxy: contact.status,
        residualM: result.residualM,
        finiteMatrices: rig.joints.every((j) =>
          j.bone.matrixWorld.elements.every(Number.isFinite),
        ),
        tissue,
      });
    }
    if (frame % 30 === 0) console.log(clipName, frame);
  }
}
const report = {
  framesPerClip: 121,
  clips: 2,
  samples: rows.length,
  finiteMatrices: rows.every((r) => r.finiteMatrices),
  proxyContactSamples: rows.filter((r) => r.proxy === "PROXY_CONTACT").length,
  tissuePass: 0,
  scope:
    "actual hand source triangles at discrete poses; not full-body acceptance or continuous collision",
  rows,
};
fs.writeFileSync(
  "artifacts/grasp-v2/trajectory-audit.json",
  JSON.stringify(report, null, 2),
);
if (!report.finiteMatrices) process.exitCode = 1;
