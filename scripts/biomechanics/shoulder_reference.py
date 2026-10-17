"""Extract immutable model definitions; estimate local constraint rank numerically."""
import argparse
import hashlib
import json
import xml.etree.ElementTree as ET
from pathlib import Path

import numpy as np
import opensim as osim


def execute(path, output):
    root = ET.parse(path).getroot()
    model = osim.Model(str(path))
    model.setUseVisualizer(False)
    state = model.initSystem()
    model.assemble(state)
    model.realizePosition(state)
    coords = model.getCoordinateSet()
    free = [coords.get(i) for i in range(coords.getSize()) if not coords.get(i).getLocked(state)]
    constraint = root.find('.//ConstraintSet/objects/PointConstraint')
    body_names = [constraint.findtext('socket_body_1').split('/')[-1],
                  constraint.findtext('socket_body_2').split('/')[-1]]
    points = [np.fromstring(constraint.findtext(f'location_body_{i}'), sep=' ') for i in [1, 2]]

    def residual():
        model.realizePosition(state)
        locations = []
        for name, point in zip(body_names, points):
            t = model.getBodySet().get(name).getTransformInGround(state)
            rotation = np.array([[t.R().get(i, j) for j in range(3)] for i in range(3)])
            locations.append(rotation @ point + np.array([t.p().get(i) for i in range(3)]))
        return locations[0] - locations[1]

    baseline = residual()
    rank_checks = []
    for step in [1e-5, 1e-6, 1e-7]:
        columns = []
        for coord in free:
            value = coord.getValue(state)
            coord.setValue(state, value + step, False)
            plus = residual()
            coord.setValue(state, value - step, False)
            minus = residual()
            coord.setValue(state, value, False)
            columns.append((plus - minus) / (2 * step))
        jacobian = np.array(columns).T
        singular = np.linalg.svd(jacobian, compute_uv=False)
        rank = int(np.linalg.matrix_rank(jacobian, tol=1e-8))
        rank_checks.append({'step': step, 'jacobian': jacobian.tolist(),
                            'singularValues': singular.tolist(), 'rankAtTolerance1eMinus8': rank,
                            'localTangentDimension': len(free) - rank})
    joints = []
    for joint in root.findall('.//JointSet/objects/*'):
        joints.append({'name': joint.get('name'), 'type': joint.tag,
                       'definitionXml': ET.tostring(joint, encoding='unicode'),
                       'evidence': 'model-provided'})
    cuff = []
    for muscle in root.findall('.//ForceSet/objects/*'):
        if not muscle.get('name', '').startswith(('Supraspinatus', 'Infraspinatus', 'Subscapularis', 'TeresMinor')):
            continue
        paths = muscle.findall('.//PathPointSet/objects/*')
        cuff.append({'muscleId': muscle.get('name'), 'evidence': 'model-provided',
                     'points': [{'name': p.get('name'), 'type': p.tag,
                                 'role': 'first-path-endpoint' if i == 0 else 'last-path-endpoint' if i == len(paths)-1 else 'intermediate-path-point',
                                 'definitionXml': ET.tostring(p, encoding='unicode')}
                                for i, p in enumerate(paths)]})
    result = {'modelSha256': hashlib.sha256(path.read_bytes()).hexdigest(),
              'opensim': osim.GetVersionAndDate(), 'coordinateCount': coords.getSize(),
              'unlockedCoordinates': [c.getName() for c in free],
              'lockedCoordinates': [coords.get(i).getName() for i in range(coords.getSize()) if coords.get(i).getLocked(state)],
              'constraintXml': ET.tostring(constraint, encoding='unicode'),
              'assembledConstraintResidualM': baseline.tolist(), 'localRankChecks': rank_checks,
              'joints': joints, 'rotatorCuffPaths': cuff,
              'limits': ['Local finite-difference tangent rank at assembled default only, not global mobility proof',
                         'Path endpoints are model references, not calibrated 467-mesh anatomical attachments',
                         'XML rotation axes/functions retain their original OpenSim definition; no Euler-to-Mac equivalence asserted']}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: result[k] for k in ['coordinateCount', 'lockedCoordinates', 'unlockedCoordinates', 'localRankChecks']}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('model', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    execute(args.model, args.output)
