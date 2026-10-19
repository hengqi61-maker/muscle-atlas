"""Own disposable GLB QA fixture, not anatomical content."""
import bpy, json, pathlib, sys
out=pathlib.Path(sys.argv[sys.argv.index('--')+1]);out.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.context.scene.unit_settings.system='METRIC'
for name,loc,scale in [('PilotBase',(0,0,1),(1,1,1)),('PilotFloater',(4,0,1),(.25,.25,.25))]:
 bpy.ops.mesh.primitive_cube_add(size=2,location=loc); o=bpy.context.object;o.name=name
 # Bake only our new fixture scale, never a project source asset.
 for v in o.data.vertices:v.co.x*=scale[0];v.co.y*=scale[1];v.co.z*=scale[2]
 o.data.materials.append(bpy.data.materials.new('M_'+name))
bpy.ops.wm.save_as_mainfile(filepath=str(out/'fixture.blend'))
print('@@JSON@@'+json.dumps({'ok':True,'fixture':'two closed cubes, intentionally detached; no anatomical claims','blender':bpy.app.version_string,'build':bpy.app.build_hash.decode()}))
