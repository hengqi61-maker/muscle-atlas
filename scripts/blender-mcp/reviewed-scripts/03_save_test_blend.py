import bpy
from pathlib import Path
out = Path(bpy.path.abspath("//")) / "mcp-connectivity-test.blend"
# if no blend path yet, use absolute from env
import os
ws = os.environ.get("BLENDER_MCP_WORKSPACE")
if ws:
    out = Path(ws) / "mcp-connectivity-test.blend"
bpy.ops.wm.save_as_mainfile(filepath=str(out))
print("SAVED", out)
