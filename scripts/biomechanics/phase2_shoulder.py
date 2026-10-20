"""Phase2 local model sensitivity; no clinical or motion approval inference."""
import argparse
import hashlib
import json
import math
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

import numpy as np


def relative(parent, child):
    return np.linalg.inv(parent) @ child


def angle(a, b):
    value = (np.trace(a[:3, :3].T @ b[:3, :3]) - 1) / 2
    return float(np.arccos(np.clip(value, -1, 1)))


def peer(commit, out):
    from kinematics import validate
    paths = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', commit,
                                     'docs/rig-v2/handoff/v1/'], text=True).splitlines()
    records = []
    for path in paths:
        if not path.endswith('.packet.json'):
            continue
        raw = subprocess.check_output(['git', 'show', f'{commit}:{path}'])
        data = json.loads(raw)
        issues = validate(data)
        if issues:
            raise ValueError(issues)
        lf = raw.replace(b'\r\n', b'\n')
        records.append({'path': path, 'rawGitBlobSha256': hashlib.sha256(raw).hexdigest(),
                        'byteCount': len(raw), 'rawCRLFCount': raw.count(b'\r\n'),
                        'lfRenderingSha256': hashlib.sha256(lf).hexdigest(),
                        'crlfRenderingSha256': hashlib.sha256(lf.replace(b'\n', b'\r\n')).hexdigest(),
                        'samples': len(data['samples']), 'nodes': len(data['nodes']), 'issues': issues})
    if len(records) != 7:
        raise ValueError('Expected actual seven Mac packets')
    original = subprocess.check_output(['git', 'show',
                                       'fd1701fc87ab00787056cb24f4e398d1f04c26c7:research/opensim/results/shoulder.packet.json'])
    lf = original.replace(b'\r\n', b'\n')
    result = {'peerCommit': commit, 'packetRecords': records,
              'windowsPacketPublishedLfSha256': hashlib.sha256(lf).hexdigest(),
              'windowsPacketCrLfExportSha256': hashlib.sha256(lf.replace(b'\n', b'\r\n')).hexdigest(),
              'scope': 'Exact bytes and schema; not anatomical or continuous motion approval'}
    out.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')


def execute(path, output):
    import opensim as osim
    from opensim_experiment import transform
    model = osim.Model(str(path))
    model.setUseVisualizer(False)
    xml = ET.parse(path).getroot()
    pc = xml.find('.//ConstraintSet/objects/PointConstraint')
    names = [pc.findtext(f'socket_body_{i}').split('/')[-1] for i in (1, 2)]
    points = [np.fromstring(pc.findtext(f'location_body_{i}'), sep=' ') for i in (1, 2)]
    rows = []
    experiments = [('shoulder_elv', [0, 15, 30, 45, 60], False),
                   ('scapula_upward_rot', [0, 3, 6, 9, 12], False),
                   ('elbow_flexion', [0, 30, 60, 90], True)]
    for coordinate, targets, unlock in experiments:
        reference = None
        for degree in targets:
            model.getCoordinateSet().get("elbow_flexion").setDefaultLocked(not unlock)
            state = model.initSystem()
            coords = model.getCoordinateSet()
            target = coords.get(coordinate)
            if unlock:
                target.setLocked(state, False)
            target.setValue(state, math.radians(degree), False)
            model.assemble(state)
            model.realizePosition(state)
            worlds = {name: transform(model.getBodySet().get(name), state)
                      for name in ['thorax', 'clavicle', 'scapula', 'humerus', 'ulna', 'radius', 'hand']}
            relatives = {'scapulaInThorax': relative(worlds['thorax'], worlds['scapula']),
                         'humerusInScapula': relative(worlds['scapula'], worlds['humerus']),
                         'ulnaInHumerus': relative(worlds['humerus'], worlds['ulna'])}
            if reference is None:
                reference = relatives
            residual = [(worlds[n] @ np.append(p, 1))[:3] for n, p in zip(names, points)]
            rows.append({'experiment': coordinate, 'operatorCommandDegrees': degree,
                         'actualRadians': target.getValue(state), 'elbowExplicitlyUnlocked': unlock,
                         'elbowLockedAtObservation': coords.get('elbow_flexion').getLocked(state),
                         'allActualCoordinatesRadiansOrMetres': {coords.get(i).getName(): coords.get(i).getValue(state)
                                                                  for i in range(coords.getSize())},
                         'acResidualMetres': (residual[0] - residual[1]).tolist(),
                         'acResidualNormMetres': float(np.linalg.norm(residual[0] - residual[1])),
                         'relativeMatricesColumnMajor': {k: v.reshape(16, order='F').tolist() for k, v in relatives.items()},
                         'relativeOrientationChangeFromFirstSampleRadians': {k: angle(reference[k], v) for k, v in relatives.items()}})
    result = {'modelSha256': hashlib.sha256(path.read_bytes()).hexdigest(),
              'scriptSha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'producerGitCommit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
              'opensimVersion': osim.GetVersionAndDate(), 'rows': rows,
              'jointDefinitionsModelProvided': [{'name': j.get('name'), 'type': j.tag,
                                                 'xml': ET.tostring(j, encoding='unicode')}
                                                for j in xml.findall('.//JointSet/objects/*')],
              'verdict': 'INCONCLUSIVE', 'mayApproveMotion': False,
              'limitations': ['Artificial independent pose sweeps, not recorded pulldown or temporal trajectory',
                              'Assemble can alter commanded coordinates; actual values retained',
                              'Unlocked elbow is an explicit experimental override of model default lock',
                              'No calibrated Mac anatomical axes, subject-specific parameters, joint loads or EMG',
                              'Rotation deltas are coordinate-free engineering descriptors, not clinical angle thresholds']}
    output.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'rows': len(rows), 'maxAcResidualM': max(r['acResidualNormMetres'] for r in rows),
                      'elbowRows': [r['actualRadians'] for r in rows if r['elbowExplicitlyUnlocked']]}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('output', type=Path)
    parser.add_argument('--model', type=Path)
    parser.add_argument('--peer-commit')
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    if args.peer_commit:
        peer(args.peer_commit, args.output)
    else:
        execute(args.model, args.output)
