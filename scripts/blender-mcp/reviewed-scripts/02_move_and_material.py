import bpy
cube = bpy.data.objects.get("MCP_TEST_CUBE")
assert cube is not None, "MCP_TEST_CUBE missing"
cube.location = (1.5, -0.5, 2.0)
mat = bpy.data.materials.get("MCP_TEST_MAT") or bpy.data.materials.new("MCP_TEST_MAT")
mat.use_nodes = True
bsdf = mat.node_tree.nodes.get("Principled BSDF")
if bsdf:
    bsdf.inputs["Base Color"].default_value = (0.1, 0.55, 0.95, 1.0)
if cube.data.materials:
    cube.data.materials[0] = mat
else:
    cube.data.materials.append(mat)
print("UPDATED", cube.name, tuple(cube.location), mat.name)
