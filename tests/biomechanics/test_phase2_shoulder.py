"""Phase2 independent numeric regression checks; native producer runs separately."""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'scripts' / 'biomechanics'))
from phase2_shoulder import angle, relative

ROOT = Path(__file__).resolve().parents[2]


def test_relative_rotation_and_frame_invariance():
    a = np.eye(4)
    a[:3, 3] = [1, 2, 3]
    b = a.copy()
    b[:3, :3] = [[0, -1, 0], [1, 0, 0], [0, 0, 1]]
    assert np.isclose(angle(a, b), np.pi / 2)
    assert np.allclose(relative(a, b)[:3, 3], 0)
    assert np.allclose(relative(b @ a, b @ b), relative(a, b))


def test_actual_model_observations_and_explicit_unlock():
    result = json.loads((ROOT / 'research/phase2/shoulder/model-sweeps.json').read_text())
    assert result['modelSha256'] == '892bd333a1e1e6a2b77902b54218f12727eefd2306ca82bbda81621c926271fe'
    assert len(result['rows']) == 14
    assert max(r['acResidualNormMetres'] for r in result['rows']) < 1e-8
    elbow = [r for r in result['rows'] if r['elbowExplicitlyUnlocked']]
    assert all(not r['elbowLockedAtObservation'] for r in elbow)
    assert np.allclose([r['actualRadians'] for r in elbow], np.deg2rad([0, 30, 60, 90]))
    assert all(r['elbowLockedAtObservation'] for r in result['rows'] if not r['elbowExplicitlyUnlocked'])
    assert result['verdict'] == 'INCONCLUSIVE' and result['mayApproveMotion'] is False


def test_peer_raw_bytes_and_export_identity():
    report = json.loads((ROOT / 'research/phase2/shoulder/peer-byte-provenance.json').read_text())
    assert len(report['packetRecords']) == 7
    assert all(r['nodes'] == 27 and not r['issues'] for r in report['packetRecords'])
    assert report['windowsPacketPublishedLfSha256'] == '242fa6bd38b754e74de1acc32bbcd9fb9949080e9eaeb57d2115ffe6b153c9c5'
    assert report['windowsPacketCrLfExportSha256'] == '62e1f48249d78ad4811a2a8b83e420e0e38d3e21c11e9c01b89e73106124c0a8'
