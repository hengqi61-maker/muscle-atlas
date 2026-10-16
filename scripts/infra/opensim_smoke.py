"""Use an official model shipped inside the isolated OpenSim package."""
import hashlib
import json
import sys
from pathlib import Path

import opensim as osim


def run():
    source = Path(osim.__file__).parent / "tests" / "arm26.osim"
    if not source.is_file():
        raise FileNotFoundError(f"Official arm26 fixture missing: {source}")
    model = osim.Model(str(source))
    print("OPENSIM_STAGE loaded", file=sys.stderr, flush=True)
    model.setUseVisualizer(False)
    analysis = osim.BodyKinematics(model)
    # Model owns analyses. A separately owned SWIG Analysis can outlive its Model
    # during function-local teardown and dereference a freed native model.
    model.addAnalysis(analysis)
    assert not analysis.thisown
    state = model.initSystem()
    print("OPENSIM_STAGE initialized", file=sys.stderr, flush=True)
    model.equilibrateMuscles(state)
    print("OPENSIM_STAGE equilibrated", file=sys.stderr, flush=True)
    model.realizeDynamics(state)
    mass_center = model.calcMassCenterPosition(state)
    coordinates = model.getCoordinateSet()
    import math
    assert coordinates.getSize() > 0 and model.getMuscles().getSize() > 0
    assert all(math.isfinite(mass_center.get(i)) for i in range(3))
    analysis.setRecordCenterOfMass(True)
    analysis.begin(state)
    analysis.step(state, 1)
    analysis.end(state)
    positions = analysis.getPositionStorage()
    assert positions.getSize() > 0
    print("OPENSIM_STAGE analyzed", file=sys.stderr, flush=True)
    return {"version": osim.GetVersionAndDate(), "model": source.name,
            "model_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
            "coordinates": coordinates.getSize(), "muscles": model.getMuscles().getSize(),
            "mass_center_m": [mass_center.get(i) for i in range(3)],
            "body_kinematics_rows": positions.getSize(),
            "scope": "Official generic arm26 model loading, equilibrium and BodyKinematics; no individual force/activation estimation."}


if __name__ == "__main__":
    print(json.dumps(run(), indent=2), flush=True)
