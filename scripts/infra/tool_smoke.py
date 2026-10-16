"""Exercise installed executables without requiring a compiler or desktop."""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import imageio_ffmpeg


def run():
    bindir = Path(sys.executable).parent
    suffix = ".exe" if sys.platform == "win32" else ""
    with tempfile.TemporaryDirectory(prefix="atlas-tools-") as temporary:
        root = Path(temporary)
        (root / "CMakeLists.txt").write_text(
            'cmake_minimum_required(VERSION 3.20)\nproject(AtlasSmoke NONE)\n'
            'add_custom_target(smoke ALL COMMAND ${CMAKE_COMMAND} -E echo ATLAS_NINJA_OK)\n')
        subprocess.run([str(bindir / f"cmake{suffix}"), "-S", str(root), "-B", str(root / "build"),
                        "-G", "Ninja", f"-DCMAKE_MAKE_PROGRAM={bindir / ('ninja' + suffix)}"], check=True)
        subprocess.run([str(bindir / f"cmake{suffix}"), "--build", str(root / "build")], check=True)
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    subprocess.run([ffmpeg, "-v", "error", "-f", "lavfi", "-i", "color=c=black:s=16x16:d=0.1",
                    "-f", "null", "-"], check=True)
    return {"cmake_ninja": "PASS: configure and execute a compiler-free custom target",
            "ffmpeg": "PASS: synthetic video decode/process to null", "ffmpeg_path": ffmpeg,
            "cpp_compiler": "not installed or verified by this test"}


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
