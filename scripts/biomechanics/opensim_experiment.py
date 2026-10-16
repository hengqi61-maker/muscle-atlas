"""Real OpenSim shoulder-model inspection and explicitly prescribed pose sweeps."""
import argparse
import csv
import hashlib
import json
import math
import subprocess
from pathlib import Path

import numpy as np
import opensim as osim


def transform(frame, state):
    value = frame.getTransformInGround(state)
    result = np.eye(4)
    for i in range(3):
        result[i, 3] = value.p().get(i)
        for j in range(3):
            result[i, j] = value.R().get(i, j)
    return result


def flat(m):
    return m.reshape(16, order="F").tolist()


def execute(model_file, out, source_commit):
    model = osim.Model(str(model_file))
    model.setUseVisualizer(False)
    state = model.initSystem()
    model.realizePosition(state)
    bodies, joints, coords, muscles = model.getBodySet(), model.getJointSet(), model.getCoordinateSet(), model.getMuscles()
    parents = {}
    joint_info = []
    for i in range(joints.getSize()):
        joint = joints.get(i)
        parent = joint.getParentFrame().findBaseFrame().getName()
        child = joint.getChildFrame().findBaseFrame().getName()
        parents[child] = None if parent == "ground" else parent
        joint_info.append({"name": joint.getName(), "type": joint.getConcreteClassName(), "parentBody": parent, "childBody": child})
    coordinate_info = [{"name": coords.get(i).getName(), "default": coords.get(i).getDefaultValue(),
                        "range": [coords.get(i).getRangeMin(), coords.get(i).getRangeMax()],
                        "unit": "rad" if int(coords.get(i).getMotionType()) == 1 else "m",
                        "motionType": int(coords.get(i).getMotionType()), "locked": coords.get(i).getLocked(state)} for i in range(coords.getSize())]
    names = [bodies.get(i).getName() for i in range(bodies.getSize())]

    def observation():
        worlds = {name: transform(bodies.get(name), state) for name in names}
        return {name: {"localMatrix": flat(np.linalg.inv(worlds[parents[name]]) @ worlds[name] if parents[name] else worlds[name]),
                       "worldMatrix": flat(worlds[name])} for name in names}

    reference = observation()
    nodes = [{"id": name, "parentId": parents[name], "side": "midline" if name == "thorax" else "right",
              **reference[name], "anatomicalAxesKnown": False} for name in names]
    attachments = []
    for i in range(muscles.getSize()):
        muscle = muscles.get(i)
        points = muscle.getGeometryPath().getPathPointSet()
        for j in range(points.getSize()):
            point = points.get(j)
            location = point.getLocation(state)
            attachments.append({"muscleId": muscle.getName(), "pathPointId": point.getName(),
                                "parentFrame": point.getParentFrame().getAbsolutePathString(),
                                "position_m": [location.get(k) for k in range(3)],
                                "evidence": {"type": "model-provided", "confidence": "limited",
                                             "uncertainties": ["Generic model path point at default pose; may be a via/wrapping point, not a calibrated surface attachment"]}})
    samples, measurements = [], []
    for experiment, coordinate, degrees in [
            ("prescribed-GH-elevation", "shoulder_elv", [0, 15, 30, 45, 60]),
            ("prescribed-scapula-upward", "scapula_upward_rot", [0, 3, 6, 9, 12])]:
        for k, degree in enumerate(degrees):
            time = len(samples)
            state.setTime(time)
            for i in range(coords.getSize()):
                coords.get(i).setValue(state, coords.get(i).getDefaultValue(), False)
            commanded = math.radians(degree)
            coord = coords.get(coordinate)
            if not coord.getRangeMin() <= commanded <= coord.getRangeMax():
                raise ValueError(f"Test command outside model coordinate range: {coordinate} {degree}")
            coord.setValue(state, commanded, False)
            model.assemble(state)
            model.realizePosition(state)
            poses = observation()
            samples.append({"timeSeconds": time, "phase": f"{experiment}:operator-command-{degree}deg",
                            "origin": "operator-specified", "transforms": poses})
            lengths = {muscles.get(i).getName(): muscles.get(i).getLength(state) for i in range(muscles.getSize())}
            assert all(math.isfinite(v) and v > 0 for v in lengths.values())
            measurements.append({"experiment": experiment, "sampleIndex": time, "coordinate": coordinate,
                                 "commanded_deg": degree, "actual_rad": coord.getValue(state),
                                 "musclePathLength_m": lengths, "scope": "Prescribed model test pose, not a measured or recommended exercise trajectory"})
    script_hash = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    git_head = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    packet = {"schemaVersion": "1.0.0", "experimentId": "official-thoracoscapular-prescribed-sweeps",
              "source": {"kind": "opensim-model", "uri": f"https://github.com/opensim-org/opensim-core/blob/{source_commit}/OpenSim/Tests/shared/ThoracoscapularShoulderModel.osim",
                         "sha256": hashlib.sha256(model_file.read_bytes()).hexdigest(), "gitCommit": source_commit,
                         "producerCommit": git_head, "software": osim.GetVersionAndDate() + "; script SHA256=" + script_hash,
                         "licenseStatus": "OpenSim-core repository Apache-2.0; retained locally, not redistributed; model-specific attribution retained"},
              "coordinates": {"lengthUnit": "m", "timeUnit": "s", "handedness": "right",
                              "axes": {"x": "OpenSim model ground X", "y": "OpenSim model ground Y", "z": "OpenSim model ground Z; not yet aligned to Mac"},
                              "matrixStorage": "column-major-16", "vectorConvention": "column-vectors",
                              "transformMeaning": "T_parent_from_local; T_world_from_local", "rotationConvention": "active-right-handed-matrix"},
              "referencePose": {"kind": "model-default", "description": "Actual model defaults before prescribed tests; not aligned to Mac rest pose", "anatomicallyCalibrated": False},
              "coverage": {"sides": ["right", "midline"], "mirrored": False, "independentlyValidated": False},
              "evidence": {"type": "model-provided", "confidence": "limited", "uncertainties": ["Single generic upper limb; no individual calibration, left-side validation or real pulldown/face-pull data", "Sample timestamps index pose tests; transitions and speeds are not physiological"]},
              "nodes": nodes, "samples": samples, "attachments": attachments}
    out.mkdir(parents=True, exist_ok=True)
    (out / "shoulder.packet.json").write_text(json.dumps(packet, indent=2) + "\n")
    report = {"opensim": osim.GetVersionAndDate(), "modelSha256": packet["source"]["sha256"], "producerGitCommit": git_head,
              "scriptSha256": script_hash, "bodies": names, "joints": joint_info, "coordinates": coordinate_info,
              "constraints": [{"name": model.getConstraintSet().get(i).getName(), "type": model.getConstraintSet().get(i).getConcreteClassName()} for i in range(model.getConstraintSet().getSize())],
              "muscles": [muscles.get(i).getName() for i in range(muscles.getSize())], "pathPointCount": len(attachments),
              "samples": measurements, "limits": packet["evidence"]["uncertainties"]}
    (out / "shoulder-report.json").write_text(json.dumps(report, indent=2) + "\n")
    with (out / "shoulder-coordinates.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=["experiment", "sampleIndex", "coordinate", "commanded_deg", "actual_rad"])
        writer.writeheader()
        writer.writerows({k: row[k] for k in writer.fieldnames} for row in measurements)
    print(json.dumps({"bodies": len(names), "joints": len(joint_info), "coordinates": len(coordinate_info),
                      "muscles": muscles.getSize(), "pathPoints": len(attachments), "poses": len(samples), "modelSha256": report["modelSha256"]}), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("model", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--source-commit", required=True)
    args = parser.parse_args()
    execute(args.model, args.out, args.source_commit)
