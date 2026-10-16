import importlib.util
from pathlib import Path


def test_mujoco_mechanics():
    file = Path(__file__).resolve().parents[2] / "scripts/infra/mujoco_smoke.py"
    spec = importlib.util.spec_from_file_location("smoke", file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert module.run()["dof"] == 2
