# PR21 exported-reference controller incident

The Three driver wrote absolute Euler angles over exported local quaternions. Ten of 30 finger joints have nonidentity references; zero input displaced joint origins by up to 37.7099636 mm. The fix composes cached exported-reference quaternion with a local delta, using Three ZYX for Blender XYZ equivalence. It deliberately preserves the imported quaternion norm so zero is exact. Alternative reorientation/reexport was rejected because source changes are unnecessary.

Actual native Blender import (BLENDER bone heuristic) and Three compare world origins and world deformation relative to each engine reference, rather than comparing incompatible raw local frames. Six poses plus 121 continuous samples agree within 0.580026 micrometres in joint origins; matrix-entry maximum1.44182e-6, tolerance64 float32 eps. These numerical tolerances do not alter motion-geometry/contact thresholds.

Initial wrong raw-frame comparison and failed normalization-neutral test remain in evidence. Repeated writes and left/right independence pass. Anatomical contact remains FAIL. See continuation-results.json and evidence package; no anatomy approval inferred.
