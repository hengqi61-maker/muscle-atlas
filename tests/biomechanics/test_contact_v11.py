import copy
import json
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).parents[2] / 'scripts/biomechanics'))
from contact_surface import scan_surface, triangle_pair
from contact_v11 import geometry_hash, migrate_v10, run, validate


def fixture(actual=False):
    old = json.loads((Path(__file__).parents[2] / 'research/contact/example.contact.json').read_bytes())
    value = migrate_v10(old)
    if actual:
        value['inputProvenance']['evidenceKind'] = 'actual-export'
        value['samples'][0]['prop']['geometryKind'] = 'actual-convex-mesh'
        hand = value['samples'][0]['hands'][0]
        hand['independentlyExported'] = True
        hand['sources'][0].update(geometryKind='actual-source-triangles', region='palm', originalTriangleIds=[901])
    return value


def test_migration_preserves_geometry_and_does_not_invent_provenance():
    packet = fixture()
    report = run(packet)
    assert report['results'][0]['classification'] == 'penetration-candidate'
    assert report['results'][0]['state'] == 'unknown'
    assert packet['inputProvenance']['evidenceKind'] == 'legacy-unverified'
    assert packet['samples'][0]['hands'][0]['sources'][0]['originalTriangleIds'] is None
    assert report['results'][0]['originalTriangleId'] is None
    packet['samples'][0]['hands'][0]['sources'][0]['geometryKind'] = 'actual-source-triangles'
    with pytest.raises(ValueError, match='verified original triangle'):
        validate(packet)


def test_actual_triangle_identity_and_proxy_uncertainty():
    packet = fixture(True)
    row = run(packet)['results'][0]
    assert row['state'] == 'penetration'
    assert row['originalTriangleId'] == 901
    assert row['signedWitnessBoundM'] < 0
    packet['samples'][0]['prop']['geometryKind'] = 'proxy-convex-mesh'
    assert run(packet)['results'][0]['state'] == 'unknown'


def test_independent_left_right_local_frames():
    packet = fixture(True)
    hand = packet['samples'][0]['hands'][0]
    hand['handWorldMatrix'] = [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 4, 0, 0, 1]
    source = hand['sources'][0]
    source['posedHandVertices'] = (np.array(source['posedWorldVertices']) - [4, 0, 0]).tolist()
    other = copy.deepcopy(hand)
    other['side'] = 'right'
    other['handWorldMatrix'][12] = -4
    other['sources'][0]['posedHandVertices'] = (np.array(source['posedWorldVertices']) + [4, 0, 0]).tolist()
    packet['samples'][0]['hands'].append(other)
    validate(packet)
    other['handWorldMatrix'][0] = -1
    with pytest.raises(ValueError, match='proper rigid'):
        validate(packet)


@pytest.mark.parametrize('failure', ['hash', 'timeline', 'triangle-id', 'local-frame'])
def test_corruption_and_missing_time_rejected(failure):
    packet = fixture(True)
    if failure == 'hash':
        packet['samples'][0]['prop']['geometrySha256'] = '0' * 64
    elif failure == 'timeline':
        packet['timeline']['expectedTimesSeconds'] = [0, 1]
    elif failure == 'triangle-id':
        packet['samples'][0]['hands'][0]['sources'][0]['originalTriangleIds'] = [1, 2]
    else:
        packet['samples'][0]['hands'][0]['sources'][0]['posedHandVertices'] = [[0, 0, 0]] * 3
    with pytest.raises(ValueError):
        validate(packet)


@pytest.mark.parametrize('other,expected', [
    ([[0, -.5, -1], [0, -.5, 1], [0, .5, 0]], 'surface-crossing'),
    ([[0, 0, 2], [1, 0, 2], [0, 1, 2]], 'disjoint'),
    ([[.1, .1, 0], [.3, .1, 0], [.1, .3, 0]], 'surface-contact'),
    ([[3, 3, 0], [4, 3, 0], [3, 4, 0]], 'disjoint'),
    ([[0, 0, 0], [1, 0, 1], [0, 1, 1]], 'surface-contact'),
])
def test_surface_known_truth_and_rotation(other, expected):
    a = np.array([[-1., -1, 0], [1, -1, 0], [0, 1, 0]])
    b = np.array(other, float)
    rotation = np.array([[0., -1, 0], [1, 0, 0], [0, 0, 1]])
    for r in [np.eye(3), rotation]:
        result = triangle_pair(a @ r.T + [4, 3, 1], b @ r.T + [4, 3, 1], 1e-9)
        assert result['classification'] == expected


def test_binary_geometry_hash_stable_and_sensitive():
    a = [[0., 0, 0], [1, 0, 0], [0, 1, 0]]
    assert geometry_hash(a, [[0, 1, 2]]) == geometry_hash(np.array(a), np.array([[0, 1, 2]]))
    assert geometry_hash(a, [[0, 1, 2]]) != geometry_hash(a, [[0, 2, 1]])


def test_review_near_parallel_tolerance_band_is_not_separation():
    a = [[-1, -1, 0], [1, -1, 0], [0, 1, 0]]
    b = [[-.5, -.5, 5e-9], [.5, -.5, 5e-9], [0, .5, 8e-9]]
    assert triangle_pair(a, b, 1e-8)['classification'] == 'unknown'


def test_review_surface_path_rejects_invalid_wrist_and_missing_palm():
    packet = fixture(True)
    packet['samples'][0]['prop']['geometryKind'] = 'actual-triangle-surface'
    hand = packet['samples'][0]['hands'][0]
    hand['frameStatus'] = 'provided'
    hand['wristWorldMatrix'] = [0] * 16
    with pytest.raises(ValueError, match='proper rigid'):
        run(packet)
    hand['wristWorldMatrix'] = None
    with pytest.raises(ValueError, match='must remain unknown'):
        run(packet)


def test_spatial_index_matches_independent_pair_enumeration():
    rng = np.random.default_rng(273)
    vertices = rng.normal(size=(60, 3))
    faces = np.arange(60).reshape((-1, 3))
    props = rng.normal(size=(30, 3))
    prop_faces = np.arange(30).reshape((-1, 3))
    for i, matches in scan_surface(vertices, faces, props, prop_faces, 1e-8):
        expected = {j: triangle_pair(vertices[faces[i]], props[face], 1e-8)['classification']
                    for j, face in enumerate(prop_faces)}
        expected = {j: state for j, state in expected.items() if state != 'disjoint'}
        actual = {r['propTriangleIndex']: r['classification'] for r in matches}
        assert actual == expected


def test_mixed_geometry_timeline_rejected_instead_of_wrong_kernel():
    packet = fixture(True)
    second = copy.deepcopy(packet['samples'][0])
    second['timeSeconds'] = 1
    second['prop']['geometryKind'] = 'actual-triangle-surface'
    packet['samples'].append(second)
    packet['timeline']['durationSeconds'] = 1
    packet['timeline']['expectedTimesSeconds'] = [0, 1]
    with pytest.raises(ValueError, match='mixed surface/convex'):
        run(packet)
