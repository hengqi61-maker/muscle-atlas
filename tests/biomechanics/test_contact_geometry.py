import importlib.util
from pathlib import Path

import numpy as np
import pytest

spec = importlib.util.spec_from_file_location(
    "contact_geometry", Path(__file__).parents[2] / "scripts/biomechanics/contact_geometry.py")
geometry = importlib.util.module_from_spec(spec)
spec.loader.exec_module(geometry)
V = np.array([[-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],
              [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]], float)
T = [[0, 1, 2], [0, 2, 3], [4, 6, 5], [4, 7, 6], [0, 4, 5], [0, 5, 1],
     [1, 5, 6], [1, 6, 2], [2, 6, 7], [2, 7, 3], [3, 7, 4], [3, 4, 0]]


@pytest.mark.parametrize("triangle,expected", [
    ([[-2, 0, 0], [2, 0, 0], [0, 2, 0]], "penetration-candidate"),
    ([[0, 0, 0], [.5, 0, 0], [0, .5, 0]], "penetration-candidate"),
    ([[1, 0, 0], [1, .5, 0], [1, 0, .5]], "surface-contact"),
    ([[2, 0, 0], [2, .5, 0], [2, 0, .5]], "disjoint"),
    ([[0, 0, .5], [0, .5, 2], [.5, 0, 2]], "penetration-candidate"),
    ([[0, 0, 2], [0, .5, 2], [.5, 0, 2]], "disjoint"),
])
def test_truth_and_rotated_frame(triangle, expected):
    triangle = np.array(triangle)
    for angle in [0., .731]:
        c, s = np.cos(angle), np.sin(angle)
        rotation = np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])
        offset = np.array([3., -2., 7.])
        planes = geometry.convex_planes(V @ rotation.T + offset, T)
        result = geometry.triangle_contact(triangle @ rotation.T + offset, planes)
        assert result["classification"] == expected


def test_invalid_geometry():
    with pytest.raises(ValueError, match="closed manifold"):
        geometry.convex_planes(V, T[:-1])
    with pytest.raises(ValueError, match="invalid source"):
        geometry.triangle_contact([[float('nan'), 0, 0]] * 3, [])


def test_finite_rotated_rod_caps_and_endpoint_touch():
    # Independent long rectangular rod, not an infinite line/cylinder approximation.
    vertices = V * [0.1, 2., 0.1]
    rotation = np.array([[0., -1., 0.], [1., 0., 0.], [0., 0., 1.]])
    planes = geometry.convex_planes(vertices @ rotation.T, T)
    for tri, expected in [
        ([[0, 1.9, 0], [.05, 2.1, 0], [-.05, 2.1, 0]], 'penetration-candidate'),
        ([[0, 2., 0], [.05, 2.1, 0], [-.05, 2.1, 0]], 'surface-contact'),
        ([[0, 2.01, 0], [.05, 2.1, 0], [-.05, 2.1, 0]], 'disjoint'),
    ]:
        assert geometry.triangle_contact(np.array(tri) @ rotation.T, planes)['classification'] == expected


def test_concave_surface_rejected():
    vertices = V.copy()
    vertices[6] = [0., 0., 0.]
    with pytest.raises(ValueError, match='nonconvex'):
        geometry.convex_planes(vertices, T)
