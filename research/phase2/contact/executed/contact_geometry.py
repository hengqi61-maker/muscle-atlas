"""Triangle/closed convex polyhedron intersection. No palm or IK proxies."""
import numpy as np


def convex_planes(vertices, triangles, tolerance=1e-9):
    """Validate supplied convex surface, weld coincident vertices for manifold check."""
    v = np.asarray(vertices, dtype=float)
    t = np.asarray(triangles, dtype=int)
    if v.ndim != 2 or v.shape[1] != 3 or not np.isfinite(v).all():
        raise ValueError("invalid vertices")
    if t.ndim != 2 or t.shape[1] != 3 or t.min() < 0 or t.max() >= len(v):
        raise ValueError("invalid triangles")
    _, welded = np.unique(np.round(v / tolerance).astype(np.int64), axis=0,
                          return_inverse=True)
    edges = {}
    planes = []
    center = v.mean(axis=0)
    for face in t:
        a, b, c = v[face]
        n = np.cross(b - a, c - a)
        size = np.linalg.norm(n)
        if size <= tolerance ** 2:
            raise ValueError("degenerate face")
        n /= size
        if np.dot(n, center - a) > 0:
            n = -n
        d = np.dot(n, a)
        if np.max(v @ n - d) > tolerance:
            raise ValueError("nonconvex prop")
        if not any(np.allclose(n, other, atol=tolerance, rtol=0)
                   and abs(d - distance) <= tolerance for other, distance in planes):
            planes.append((n, d))
        ids = welded[face]
        for i in range(3):
            edge = tuple(sorted((int(ids[i]), int(ids[(i + 1) % 3]))))
            edges[edge] = edges.get(edge, 0) + 1
    if any(count != 2 for count in edges.values()):
        raise ValueError("prop must be closed manifold")
    if np.linalg.matrix_rank(v - center) != 3:
        raise ValueError("prop must enclose volume")
    return planes


def triangle_contact(triangle, planes, tolerance=1e-9):
    """Clip actual triangle. Depth is a lower bound at a witness, not MTV."""
    poly = np.asarray(triangle, dtype=float)
    if poly.shape != (3, 3) or not np.isfinite(poly).all():
        raise ValueError("invalid source triangle")
    gap = max(float(np.min(poly @ n - d)) for n, d in planes)
    if gap > tolerance:
        return {"classification": "disjoint", "gapLowerBoundM": gap}
    for n, d in planes:
        if len(poly) == 0:
            break
        output = []
        for a, b in zip(poly, np.roll(poly, -1, axis=0)):
            da, db = np.dot(n, a) - d, np.dot(n, b) - d
            if da <= tolerance:
                output.append(a)
            if (da <= tolerance) != (db <= tolerance):
                # Clip against tolerance-expanded surface; report that uncertainty.
                output.append(a + (b - a) * ((tolerance - da) / (db - da)))
        poly = np.asarray(output)
    if len(poly) == 0:
        return {"classification": "disjoint", "gapLowerBoundM": max(0., gap)}
    witness = poly.mean(axis=0)
    depth = min(float(d - np.dot(n, witness)) for n, d in planes)
    return {"classification": "penetration-candidate" if depth > tolerance else "surface-contact",
            "positionM": witness.tolist(), "depthLowerBoundM": max(0., depth),
            "toleranceM": tolerance}
