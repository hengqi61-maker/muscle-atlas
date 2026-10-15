"""Portable attachment DQ target -> inverse-LBS relative pose correctives.
Selected cuff/palmaris base geometry, skeleton and weights stay unchanged;
all unselected meshes stay unchanged. No digit articulation is introduced.
This is an illustrative digital skinning correction, not a tissue strain model.
"""
import numpy as np
from mathutils import Quaternion,Vector

def dq_point(point, matrices, weights):
 real=None;dual=None;reference=None
 for matrix,weight in zip(matrices,weights):
  q=matrix.to_quaternion();t=matrix.translation;d=Quaternion((0,t.x,t.y,t.z))@q;d=Quaternion(tuple(.5*x for x in d))
  if reference is None:reference=q.copy()
  sign=1 if reference.dot(q)>=0 else -1
  qr=np.array(tuple(q))*weight*sign;qd=np.array(tuple(d))*weight*sign
  real=qr if real is None else real+qr;dual=qd if dual is None else dual+qd
 length=np.linalg.norm(real);real/=length;dual/=length;dual-=real*np.dot(real,dual)
 q=Quaternion(tuple(real));d=Quaternion(tuple(dual));translation=d@q.conjugated()
 return q@point+Vector((2*translation.x,2*translation.y,2*translation.z))

def geometry_stats(rest,posed,triangles):
 ra=rest[triangles[:,1]]-rest[triangles[:,0]];rb=rest[triangles[:,2]]-rest[triangles[:,0]]
 pa=posed[triangles[:,1]]-posed[triangles[:,0]];pb=posed[triangles[:,2]]-posed[triangles[:,0]]
 baseline=np.linalg.norm(np.cross(ra,rb),axis=1);area=np.linalg.norm(np.cross(pa,pb),axis=1);ratios=area[baseline>2e-12]/baseline[baseline>2e-12]
 return {'minimumAreaRatio':float(ratios.min()),'areaRatioQuantiles':dict(zip(['p01','p05','p50','p95','p99'],map(float,np.quantile(ratios,[.01,.05,.5,.95,.99])))),'collapsedTriangles':int((ratios<.05).sum()),'eligibleTriangles':len(ratios)}

def prepare(scene,rig,objects,knot_step=6):
 result={};knots=list(range(0,121,knot_step))
 for o in objects:
  rest=np.array([tuple(v.co) for v in o.data.vertices]);o.data.calc_loop_triangles();tri=np.array([tuple(t.vertices) for t in o.data.loop_triangles]);groups={g.index:g.name for g in o.vertex_groups}
  bindings=[[(groups[g.group],g.weight) for g in v.groups if g.weight>0] for v in o.data.vertices]
  corrections=[];minimum_det=1.;maximum_correction=0.;dq_stats=[]
  for frame in knots:
   scene.frame_set(frame);transforms={name:rig.pose.bones[name].matrix@rig.data.bones[name].matrix_local.inverted() for name in rig.data.bones.keys()};delta=[];desired=[]
   for i,binding in enumerate(bindings):
    ms=[transforms[n] for n,w in binding];ws=[w for n,w in binding];matrix=sum((np.array(m)*w for m,w in zip(ms,ws)),np.zeros((4,4)));det=abs(float(np.linalg.det(matrix[:3,:3])));minimum_det=min(minimum_det,det)
    assert det>1e-5,('near singular LBS inverse',o.name,frame,i,det)
    target=dq_point(Vector(rest[i]),ms,ws);pre=np.linalg.solve(matrix[:3,:3],np.array(target)-matrix[:3,3]);delta.append(pre-rest[i]);desired.append(tuple(target))
   correction=np.array(delta);corrections.append(correction);maximum_correction=max(maximum_correction,float(np.linalg.norm(correction,axis=1).max()));dq_stats.append({'frame':frame,**geometry_stats(rest,np.array(desired),tri)})
  # Evaluate actual linearly-interpolated correction + changing skin matrices at every frame.
  actual=[]
  for frame in np.arange(0,120.001,.5):
   scene.frame_set(int(frame),subframe=float(frame-int(frame)));index=min(int(frame//knot_step),len(knots)-2);alpha=(frame-knots[index])/knot_step;delta=corrections[index]*(1-alpha)+corrections[index+1]*alpha
   transforms={name:np.array(rig.pose.bones[name].matrix@rig.data.bones[name].matrix_local.inverted()) for name in rig.data.bones.keys()};posed=[]
   for i,binding in enumerate(bindings):
    matrix=sum((transforms[n]*w for n,w in binding),np.zeros((4,4)));posed.append((matrix@np.append(rest[i]+delta[i],1))[:3])
   actual.append({'frame':frame,**geometry_stats(rest,np.array(posed),tri)})
  result[o.name]={'knots':knots,'corrections':corrections,'report':{'minimumLbsDeterminant':minimum_det,'maximumPreskinCorrectionM':maximum_correction,'dqKnotSurfaces':dq_stats,'portableInterpolatedSurfaces':actual}}
 return result

def install(objects,prepared):
 for o in objects:
  info=prepared[o.name];o.shape_key_add(name='Basis',from_mix=False)
  for i,(frame,delta) in enumerate(zip(info['knots'],info['corrections'])):
   key=o.shape_key_add(name=f'CuffDQ_{frame:03}',from_mix=False)
   for v,d in zip(key.data,delta):v.co+=Vector(d)
   for knot in info['knots']:
    key.value=1.0 if knot==frame else 0.0;key.keyframe_insert(data_path='value',frame=knot)
  # Linear morph interpolation is essential for the checked convex adjacent pair contract.
  action=o.data.shape_keys.animation_data.action
  for layer in action.layers:
   for strip in layer.strips:
    for slot in action.slots:
     bag=strip.channelbag(slot)
     if bag:
      for curve in bag.fcurves:
       for key in curve.keyframe_points:key.interpolation='LINEAR'
