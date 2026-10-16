"""Run independent checks and preserve any preexisting tracked test evidence."""
import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--browser", action="store_true")
    parser.add_argument("--opensim-prefix", type=Path)
    parser.add_argument("--conda", default="C:/ProgramData/Anaconda3/Scripts/conda.exe")
    parser.add_argument("--out", type=Path, default=Path("artifacts/windows/checks"))
    parser.add_argument("--only", nargs="+", help="Rerun selected check names; use a separate --out to preserve prior logs")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    out = root / args.out
    out.mkdir(parents=True, exist_ok=True)
    node = shutil.which("node")
    npm = shutil.which("npm.cmd" if sys.platform == "win32" else "npm")
    if not node or not npm:
        raise RuntimeError("Node/npm missing; audit before installing")
    commands = [
        ("health", [sys.executable, "scripts/infra/health.py"]),
        ("ruff", [sys.executable, "-m", "ruff", "check", "scripts/infra", "tests/infra"]),
        ("python-infra", [sys.executable, "-m", "pytest", "tests/infra", "-q"]),
        ("python-assets", [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"]),
        ("build", [npm, "run", "build"]),
        ("unit", [npm, "test"]),
        ("quality", [npm, "run", "test:quality"]),
        ("asset-negative-tests", [node, "--test", "tests/infra/assets.node.mjs"]),
        ("derived-assets", [node, "scripts/infra/validate-assets.mjs", "public/models/anatomy-curl.glb", "public/models/anatomy-pulldown.glb"]),
        ("curl", [npm, "run", "test:rig"]),
        ("pulldown", [npm, "run", "test:pulldown"]),
        ("mujoco", [sys.executable, "scripts/infra/mujoco_smoke.py"]),
        ("tools", [sys.executable, "scripts/infra/tool_smoke.py"]),
    ]
    if args.opensim_prefix:
        commands.append(("opensim", [args.conda, "run", "-p", str(args.opensim_prefix), "python", "scripts/infra/opensim_smoke.py"]))
    if args.browser:
        commands.append(("chrome", [npm, "run", "test:e2e"]))
    if args.only:
        unknown = set(args.only) - {name for name, _ in commands}
        if unknown:
            parser.error(f"Unknown checks: {sorted(unknown)}")
        commands = [(name, command) for name, command in commands if name in args.only]
    tracked = subprocess.run(["git", "ls-files", "docs/evidence", "docs/anatomy-browser.png", "docs/rigged-browser.png"],
                             cwd=root, check=True, capture_output=True, text=True).stdout.splitlines()
    saved = {name: (root / name).read_bytes() for name in tracked if (root / name).is_file()}
    results = []
    try:
        for name, command in commands:
            with (out / f"{name}.log").open("wb") as log:
                try:
                    result = subprocess.run(command, cwd=root, check=False, stdout=log, stderr=subprocess.STDOUT, timeout=600)
                    code = result.returncode
                except (OSError, subprocess.TimeoutExpired) as exc:
                    log.write(str(exc).encode())
                    code = -1
            results.append({"name": name, "command": command, "exit": code, "log": f"{name}.log"})
            print(f"{name}: exit {code}", flush=True)
    finally:
        restored = []
        for name, content in saved.items():
            file = root / name
            if file.read_bytes() != content:
                dest = out / "generated" / name
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(file, dest)
                file.write_bytes(content)
                restored.append(name)
        (out / "results.json").write_text(json.dumps({"checks": results, "preservedHistoricalEvidence": restored}, indent=2))
    return int(any(r["exit"] for r in results))


if __name__ == "__main__":
    raise SystemExit(main())
