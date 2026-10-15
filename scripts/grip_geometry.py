"""Original detailed hex equipment and contact markers. Metres, Blender Z-up.
Anatomical hand geometry comes exclusively from the source atlas.
"""
import bpy,math
from mathutils import Vector,Quaternion

def material(name,color,metal=0,roughness=.5):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True
 node=m.node_tree.nodes.get('Principled BSDF');node.inputs['Base Color'].default_value=(*color,1);node.inputs['Metallic'].default_value=metal;node.inputs['Roughness'].default_value=roughness
 return m

def bind(o,rig,bone):
 if rig is None:
  for p in o.data.polygons:p.use_smooth=True
  return o
 group=o.vertex_groups.new(name=bone);group.add(list(range(len(o.data.vertices))),1,'REPLACE')
 mod=o.modifiers.new('GripAttachment','ARMATURE');mod.object=rig;o.parent=None
 for p in o.data.polygons:p.use_smooth=True
 return o

def contact_marker(center,rig,bone,name):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=8,ring_count=4,radius=.0005,location=center)
 o=bpy.context.object;o.name=name;o['visualLayer']='contact-marker';o['contactAnchor']=True;bind(o,rig,bone);return o

def create_hex_dumbbell(center,rig,bone):
 """Original detailed 310mm hex dumbbell, 28mm knurled handle, bevelled rubber heads."""
 center=Vector(center);steel=material('KnurledChrome',(.40,.46,.49),.92,.23);rubber=material('MouldedRubber',(.025,.032,.039),0,.72);badge=material('MouldedMarking',(.30,.34,.37),.05,.60)
 parts=[]
 # Knurl is geometry, so the offline GLB does not depend on a procedural shader.
 vertices=[];faces=[];rings=91;segments=64
 for i in range(rings):
  x=-.070+.140*i/(rings-1)
  radius=.014+.00035*(1 if i%2 else -1)
  for j in range(segments):
   a=2*math.pi*j/segments;rr=radius+.00025*((-1)**(j+i));vertices.append(tuple(center+Vector((x,rr*math.cos(a),rr*math.sin(a)))))
 for i in range(rings-1):
  for j in range(segments):a=i*segments+j;b=i*segments+(j+1)%segments;faces.append((a,b,b+segments,a+segments))
 faces.append(tuple(range(segments-1,-1,-1)));faces.append(tuple((rings-1)*segments+j for j in range(segments)))
 mesh=bpy.data.meshes.new('DiamondKnurlMesh');mesh.from_pydata(vertices,[],faces);mesh.update();handle=bpy.data.objects.new('Dumbbell_KnurledHandle',mesh);bpy.context.collection.objects.link(handle);handle.data.materials.append(steel);parts.append(handle)
 for side in [-1,1]:
  bpy.ops.mesh.primitive_cylinder_add(vertices=6,radius=.068,depth=.078,location=center+Vector((side*.116,0,0)),rotation=(0,math.pi/2,0))
  o=bpy.context.object;o.name=f'Dumbbell_HexHead_{side}';o.rotation_mode='QUATERNION';o.rotation_quaternion=Quaternion((0,1,0),math.pi/2)@Quaternion((0,0,1),math.pi/6);bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
  bevel=o.modifiers.new('RubberEdgeRadius','BEVEL');bevel.width=.005;bevel.segments=4;bpy.ops.object.modifier_apply(modifier=bevel.name);o.data.materials.append(rubber);parts.append(o)
  # Inset badge and moulded weight marking, not a fake copied brand logo.
  bpy.ops.mesh.primitive_cylinder_add(vertices=48,radius=.030,depth=.0015,location=center+Vector((side*.155,0,0)),rotation=(0,math.pi/2,0))
  o=bpy.context.object;o.name=f'Dumbbell_EndBadge_{side}';o.data.materials.append(badge);parts.append(o)
  for offset in [-.073,.073]:
   if side*offset<0:continue
   bpy.ops.mesh.primitive_cylinder_add(vertices=48,radius=.021,depth=.012,location=center+Vector((offset,0,0)),rotation=(0,math.pi/2,0))
   o=bpy.context.object;o.name=f'Dumbbell_Shoulder_{side}';o.data.materials.append(steel);parts.append(o)
  font=bpy.data.curves.new('8KG','FONT');font.body='8';font.align_x='CENTER';font.align_y='CENTER';font.size=.035;font.extrude=.0004;font.bevel_depth=.00015
  o=bpy.data.objects.new(f'Dumbbell_WeightMark_{side}',font);bpy.context.collection.objects.link(o);o.location=center+Vector((side*.156,0,0));o.rotation_euler=(math.pi/2,0,side*math.pi/2);bpy.context.view_layer.objects.active=o;o.select_set(True);bpy.ops.object.convert(target='MESH');o=bpy.context.object;o.data.materials.append(rubber);parts.append(o)
 for o in parts:
  o['equipment']='original-detailed-hex-dumbbell';bind(o,rig,bone)
  if 'HexHead' in o.name:
   for p in o.data.polygons:p.use_smooth=False
 return parts
