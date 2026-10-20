import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parents[2] / 'scripts/biomechanics'))
from mac_rig_reference import basis_axis


def test_rest_removed_before_basis_axis():
    # Rest Z90 composed with basis X60, explicit Hamilton product.
    z = np.sqrt(.5)
    angle, axis = basis_axis([0, 0, z, z], [.5*z, .5*z, np.sqrt(3)*z/2, np.sqrt(3)*z/2])
    assert abs(angle-np.pi/3) < 1e-12
    np.testing.assert_allclose(axis, [1, 0, 0], atol=1e-12)
    assert basis_axis([0, 0, z, z], [0, 0, z, z])[1] is None


def test_frozen_actual_bind_and_clip_identity():
    data = json.loads((Path(__file__).parents[2] / 'research/phase2/shoulder/mac-pr12-bind-axes.json').read_bytes())
    assert data['assetSha256'] == 'ef803a4bbb3c644504c124519e39ba0b3b760ec139eaf60d277ef7f7f5d23274'
    assert data['jointCount'] == 27
    assert len({f['nodeIndex'] for f in data['frames']}) == 27
    # Frozen numeric observation, not a quality/medical threshold.
    observed = max(f['worldDefaultTimesInverseBindResidualToIdentity'] for f in data['frames'])
    assert abs(observed - 1.1942543084997221e-6) < 1e-15
    assert {c['name'] for c in data['clips']} == {'CurlProbe', 'PulldownProbe'}
    for clip in data['clips']:
        for side in ['Left', 'Right']:
            track = next(t for t in clip['tracks'] if t['name'] == side+'Forearm')
            assert len(track['samples']) == 121
            assert track['samples'][-1]['timeSeconds'] == 4
