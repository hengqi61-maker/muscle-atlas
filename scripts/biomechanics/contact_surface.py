"""Actual triangle-surface intersection for nonconvex equipment; no volume claim."""
from itertools import product

import numpy as np


def triangle_pair(a, b, tolerance):
    """Separating-axis theorem including coplanar in-plane axes."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    ea, eb = np.roll(a, -1, axis=0) - a, np.roll(b, -1, axis=0) - b
    na, nb = np.cross(ea[0], ea[1]), np.cross(eb[0], eb[1])
    if np.linalg.norm(na) < 1e-16 or np.linalg.norm(nb) < 1e-16:
        return {'classification': 'unknown', 'reason': 'degenerate actual triangle'}
    na, nb = na / np.linalg.norm(na), nb / np.linalg.norm(nb)
    da, db = (a - b[0]) @ nb, (b - a[0]) @ na
    if (da.min() > tolerance or da.max() < -tolerance
            or db.min() > tolerance or db.max() < -tolerance):
        return {'classification': 'disjoint'}
    crossing = da.min() < -tolerance and da.max() > tolerance and db.min() < -tolerance and db.max() > tolerance
    # Witness is an actual edge/triangle-plane intersection inside the other triangle.
    for tri, other, normal in [(a, b, nb), (b, a, na)]:
        signed = (tri - other[0]) @ normal
        for i in range(3):
            j = (i + 1) % 3
            if abs(signed[i] - signed[j]) <= 1e-15:
                continue
            fraction = signed[i] / (signed[i] - signed[j])
            if not 0 <= fraction <= 1:
                continue
            point = tri[i] + fraction * (tri[j] - tri[i])
            cross = [np.dot(np.cross(other[(k + 1) % 3] - other[k], point - other[k]), normal)
                     / np.linalg.norm(other[(k + 1) % 3] - other[k]) for k in range(3)]
            if min(cross) >= -tolerance or max(cross) <= tolerance:
                return {'classification': 'surface-crossing' if crossing else 'surface-contact',
                        'positionM': point.tolist()}
    if np.linalg.norm(np.cross(na, nb)) > 1e-10:
        for axis in [np.cross(x, y) for x in ea for y in eb]:
            length = np.linalg.norm(axis)
            if length < 1e-14:
                continue
            pa, pb = a @ (axis / length), b @ (axis / length)
            if max(pa.min() - pb.max(), pb.min() - pa.max()) > tolerance:
                return {'classification': 'disjoint'}
        return {'classification': 'unknown', 'reason': 'near-plane tolerance band without exact witness'}
    # Parallel/coplanar case needs the in-plane separating axes as well.
    for edge in [*ea, *eb]:
        axis = np.cross(na, edge)
        axis /= np.linalg.norm(axis)
        pa, pb = a @ axis, b @ axis
        if max(pa.min() - pb.max(), pb.min() - pa.max()) > tolerance:
            return {'classification': 'disjoint'}
    return {'classification': 'surface-contact', 'positionM': None,
            'reason': 'coplanar/tolerance-band overlap; exact unique witness unavailable'}


def scan_surface(vertices, triangles, prop_vertices, prop_triangles, tolerance):
    """Broad-phase AABBs reject only provably separated triangle pairs."""
    prop = np.asarray(prop_vertices, float)[np.asarray(prop_triangles, int)]
    lower, upper = prop.min(axis=1), prop.max(axis=1)
    root_lower, root_upper = lower.min(axis=0), upper.max(axis=0)
    cell = np.maximum((root_upper - root_lower) / 16, tolerance * 4)
    cells = {}

    def keys(lo, hi):
        start = np.clip(np.floor((lo - root_lower) / cell).astype(int), 0, 15)
        stop = np.clip(np.floor((hi - root_lower) / cell).astype(int), 0, 15)
        return product(*(range(int(a), int(b) + 1) for a, b in zip(start, stop)))

    for face, (lo, hi) in enumerate(zip(lower, upper)):
        for key in keys(lo - tolerance, hi + tolerance):
            cells.setdefault(key, set()).add(face)
    prop_normals = np.cross(prop[:, 1] - prop[:, 0], prop[:, 2] - prop[:, 0])
    areas = np.linalg.norm(prop_normals, axis=1)
    valid = areas > 1e-16
    prop_normals[valid] /= areas[valid, None]
    for index, triangle in enumerate(np.asarray(vertices, float)[np.asarray(triangles, int)]):
        lo, hi = triangle.min(axis=0), triangle.max(axis=0)
        if np.any(root_upper < lo - tolerance) or np.any(root_lower > hi + tolerance):
            yield index, []
            continue
        ids = set()
        for key in keys(lo - tolerance, hi + tolerance):
            ids.update(cells.get(key, ()))
        candidates = np.array(sorted(ids), dtype=int)
        if len(candidates):
            candidates = candidates[np.all(upper[candidates] >= lo - tolerance, axis=1)
                                    & np.all(lower[candidates] <= hi + tolerance, axis=1)]
        normal = np.cross(triangle[1] - triangle[0], triangle[2] - triangle[0])
        area = np.linalg.norm(normal)
        if area < 1e-16:
            yield index, [{'classification': 'unknown', 'reason': 'degenerate source triangle'}]
            continue
        normal /= area
        if len(candidates):
            # Identical necessary plane tests to triangle_pair, batched before exact witnesses.
            faces = prop[candidates]
            da = np.einsum('nvc,nc->nv', triangle[None, :, :] - faces[:, :1, :], prop_normals[candidates])
            db = (faces - triangle[0]) @ normal
            keep = ((da.min(axis=1) <= tolerance) & (da.max(axis=1) >= -tolerance)
                    & (db.min(axis=1) <= tolerance) & (db.max(axis=1) >= -tolerance))
            candidates = candidates[keep | ~valid[candidates]]
        matches = []
        for candidate in candidates:
            result = triangle_pair(triangle, prop[candidate], tolerance)
            if result['classification'] != 'disjoint':
                matches.append({'propTriangleIndex': int(candidate), **result})
        yield index, matches
