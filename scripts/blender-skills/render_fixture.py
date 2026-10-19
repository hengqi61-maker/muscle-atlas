"""Own CPU-only visualization, no upstream render helper or scene mutation persisted."""
import bpy, pathlib,sys
from mathutils import Vector
src,out=sys.argv[sys.argv.index('--')+1:];bpy.ops.wm.open_mainfile(filepath=src,load_ui=False)
sc=bpy.context.scene;sc.render.engine='CYCLES';sc.cycles.device='CPU';sc.cycles.samples=4
sc.render.resolution_x=640;sc.render.resolution_y=320;sc.render.resolution_percentage=100
camera=bpy.data.objects.new('PilotCamera',bpy.data.cameras.new('PilotCamera'));sc.collection.objects.link(camera);camera.location=(7,-11,7);camera.rotation_euler=(Vector((1.5,0,1))-camera.location).to_track_quat('-Z','Y').to_euler();sc.camera=camera
light=bpy.data.objects.new('PilotLight',bpy.data.lights.new('PilotLight','AREA'));sc.collection.objects.link(light);light.location=(2,-4,8);light.data.energy=1200;light.data.shape='DISK';light.data.size=5
sc.render.filepath=out;bpy.ops.render.render(write_still=True)
