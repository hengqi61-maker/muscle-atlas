"""Machine-readable non-admin environment probe; failed commands remain visible."""
import importlib.metadata
import json
import platform
import shutil
import subprocess
import sys


def run(command):
    try:
        p = subprocess.run(command, check=False, capture_output=True, text=True, timeout=30,
                           encoding="utf-8", errors="replace")
        return {"exit": p.returncode, "output": (p.stdout + p.stderr).strip()}
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"exit": None, "error": str(exc)}


if __name__ == "__main__":
    result = {"platform": platform.platform(), "python": sys.version,
              "executable": sys.executable, "packages": {}, "commands": {}}
    for package in ["mujoco", "numpy", "pytest", "ruff", "cmake", "ninja", "imageio-ffmpeg"]:
        try:
            result["packages"][package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            result["packages"][package] = "MISSING"
    for command in [["git", "--version"], ["git", "lfs", "version"], ["node", "--version"],
                    ["npm.cmd" if sys.platform == "win32" else "npm", "--version"],
                    ["nvidia-smi", "--query-gpu=name,memory.total,driver_version", "--format=csv"],
                    ["nvcc", "--version"]]:
        key = "git-lfs" if command[:2] == ["git", "lfs"] else command[0]
        result["commands"][key] = {"path": shutil.which(command[0]), **run(command)}
    result["requiredFailures"] = [name for name, version in result["packages"].items() if version == "MISSING"]
    if sys.version_info[:2] != (3, 11):
        result["requiredFailures"].append("Dedicated Python 3.11 required")
    for name in ["git", "node"]:
        if result["commands"][name]["exit"] != 0:
            result["requiredFailures"].append(f"{name} unavailable")
    node_output = result["commands"]["node"].get("output", "")
    if node_output.startswith("v") and int(node_output[1:].split(".")[0]) < 22:
        result["requiredFailures"].append("Node >=22 required")
    print(json.dumps(result, indent=2))
    raise SystemExit(bool(result["requiredFailures"]))
