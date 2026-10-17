"""Read frozen peer packets without changing peer assets or importing Blender."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

import numpy as np
from kinematics import matrix, validate


def execute(commit, output):
    prefix = 'docs/rig-v2/handoff/v1/'
    paths = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', commit, prefix], text=True).splitlines()
    packets = {}
    report = {'peerCommit': commit, 'packets': {}, 'limits': [
        'Five clip samples cannot establish between-sample continuity',
        'Proper matrix handedness does not calibrate anatomical left/right labels',
        'Length variation is numeric description, not a physiological rejection threshold']}
    archive = Path('artifacts/v2/mac-v1')
    archive.mkdir(parents=True, exist_ok=True)
    for path in paths:
        if not path.endswith('.packet.json'):
            continue
        raw = subprocess.check_output(['git', 'show', f'{commit}:{path}'])
        name = Path(path).name
        (archive / name).write_bytes(raw)
        packet = json.loads(raw)
        issues = validate(packet)
        if issues:
            raise ValueError(f'{name}: {issues}')
        packets[name] = packet
        nodes = {n['id']: n for n in packet['nodes']}
        lengths = {key: [] for key in nodes if nodes[key]['parentId'] is not None}
        steps = []
        for sample in packet['samples']:
            for key, values in lengths.items():
                values.append(float(np.linalg.norm(matrix(sample['transforms'][key]['localMatrix'])[:3, 3])))
        for before, after in zip(packet['samples'], packet['samples'][1:]):
            for key in nodes:
                a = matrix(before['transforms'][key]['worldMatrix'])
                b = matrix(after['transforms'][key]['worldMatrix'])
                steps.append(float(np.linalg.norm(b[:3, 3] - a[:3, 3])))
        report['packets'][name] = {'sha256': hashlib.sha256(raw).hexdigest(),
                                   'jointCount': len(nodes), 'samples': len(packet['samples']),
                                   'issues': issues, 'coordinates': packet['coordinates'],
                                   'referencePose': packet['referencePose'],
                                   'segmentLengthRangeM': {key: [min(v), max(v)] for key, v in lengths.items() if v},
                                   'maxSampledJointTranslationStepM': max(steps, default=0)}
    a, b = [packets[f'gltf-{name}.packet.json'] for name in ['CurlProbe', 'PulldownProbe']]
    signatures = [{(n['id'], n['parentId'], n['side']) for n in p['nodes']} for p in [a, b]]
    report['sameClipSkeletonTopology'] = signatures[0] == signatures[1]
    if not report['sameClipSkeletonTopology'] or len(packets) != 7:
        raise ValueError('Missing handoff packets or mismatched clip topology')
    output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'packets': len(packets), 'sameClipSkeletonTopology': True}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('commit')
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    execute(args.commit, args.output)
