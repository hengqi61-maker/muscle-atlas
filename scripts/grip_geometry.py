"""Original closed-grip surface and detailed hex equipment. Metres, Blender Z-up.
Surface hand is a presentation layer, not a replacement anatomical dataset.
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

def sphere(name,position,scale,parts):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=16,location=position)
 o=bpy.context.object;o.name=name;o.scale=scale;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);parts.append(o);return o

def tube(name,points,radius,parts):
 c=bpy.data.curves.new(name,'CURVE');c.dimensions='3D';c.bevel_depth=radius;c.bevel_resolution=3;c.resolution_u=3;c.use_fill_caps=True
 spline=c.splines.new('POLY');spline.points.add(len(points)-1)
 for p,v in zip(spline.points,points):p.co=(*v,1)
 o=bpy.data.objects.new(name,c);bpy.context.collection.objects.link(o);bpy.context.view_layer.objects.active=o;o.select_set(True);bpy.ops.object.convert(target='MESH');o=bpy.context.object;parts.append(o);return o

def create_grip_hand(center,rig,bone,side=1,name='GripHand'):
 center=Vector(center);parts=[]
 def at(x,y,z):return center+Vector((side*x,y,z))
 sphere('Palm',at(0,.032,.011),(.041,.019,.032),parts)
 sphere('ThenarPad',at(-.024,.018,.024),(.020,.020,.024),parts)
 sphere('WristBridge',at(0,.028,.048),(.026,.019,.029),parts)
 # Four separate arcs wrap a 28mm handle; inner finger surface meets its radius.
 for index,x in enumerate([-.027,-.009,.009,.027]):
  r=.0235;end=-224+(index==3)*9
  pts=[at(x,r*math.cos(math.radians(a)),r*math.sin(math.radians(a))) for a in [(-20+(end+20)*i/32) for i in range(33)]]
  tube(f'Finger{index}',pts,.0084 if index<3 else .0076,parts)
  sphere(f'FingerTip{index}',pts[-1],(.0082,.0082,.0082),parts)
 # Opposing thumb crosses the finger pads rather than protruding away from the grip.
 points=[at(-.030,.022,.035),at(-.045,.004,.026),at(-.041,-.018,.017),at(-.023,-.026,.014),at(-.007,-.024,.013)]
 tube('OpposingThumb',points,.010,parts);sphere('ThumbTip',points[-1],(.010,.009,.009),parts)
 bpy.ops.object.select_all(action='DESELECT')
 for o in parts:o.select_set(True)
 bpy.context.view_layer.objects.active=parts[0];bpy.ops.object.join();hand=bpy.context.object;hand.name=name
 # Union the palm, thumb and finger roots into one closed surface; retain finger channels.
 hand.data.remesh_voxel_size=.00135;bpy.ops.object.voxel_remesh()
 smooth=hand.modifiers.new('SurfaceRelax','SMOOTH');smooth.factor=.35;smooth.iterations=3;bpy.ops.object.modifier_apply(modifier=smooth.name)
 hand.data.materials.clear();hand.data.materials.append(material('HandSurfaceWarm',(.50,.34,.24),0,.58))
 # Subtle fingernails make finger orientation readable without a texture dependency.
 nail_material=material('NailNatural',(.62,.46,.36),0,.38)
 for index,x in enumerate([-.027,-.009,.009,.027]):
  a=math.radians(-224+(index==3)*9);normal=Vector((0,math.cos(a),math.sin(a)))
  nail_parts=[];nail=sphere(f'{name}_Nail{index}',at(x,.0313*math.cos(a),.0313*math.sin(a)),(.0056,.0066,.0008),nail_parts)
  nail.rotation_mode='QUATERNION';nail.rotation_quaternion=Vector((0,0,1)).rotation_difference(normal);nail.data.materials.clear();nail.data.materials.append(nail_material);nail['visualLayer']='grip-skin';bind(nail,rig,bone)
 hand['visualLayer']='grip-skin';hand['description']='Original posed skin surface; source anatomy retained separately';bind(hand,rig,bone)
 return hand

def fold_source_hand(o,center,wrist_height):
 """Place animation-only distal source tissue inside the closed surface; raw atlas unchanged."""
 center=Vector(center)
 for v in o.data.vertices:
  if v.co.z<wrist_height-.010:
   t=max(0,min(1,(wrist_height-.010-v.co.z)/.065))
   target=Vector((center.x+max(-.031,min(.031,v.co.x-center.x)),center.y+.028,center.z+.013+.013*math.cos(t*math.pi)))
   blend=min(1,t*4);v.co=v.co.lerp(target,blend)
 if max(v.co.z for v in o.data.vertices)<wrist_height+.015:o['coveredByGripSkin']=True
 o.data.update()

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
