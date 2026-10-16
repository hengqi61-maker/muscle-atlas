"""Clip-independent pose-space correction primitives.
A corrective is a geometric skinning approximation, never a tissue/activation model.
No automatic application: a scoped correction must be registered, sampled and reviewed.
"""
import numpy as np
from mathutils import Vector, Quaternion

def blended_skin_matrix(transforms, binding):
 return sum((np.asarray(transforms[name],dtype=float)*weight for name,weight in binding),np.zeros((4,4)))

def dual_quaternion_target(point, transforms, binding):
 real=np.zeros(4);dual=np.zeros(4);reference=None
 for name,weight in binding:
  m=transforms[name];q=m.to_quaternion();t=m.translation;d=Quaternion((0,t.x,t.y,t.z))@q
  if reference is None:reference=q.copy()
  sign=1 if reference.dot(q)>=0 else -1
  real+=np.array(tuple(q))*weight*sign;dual+=np.array(tuple(d))*.5*weight*sign
 length=np.linalg.norm(real)
 if length<1e-8:raise ValueError('Ambiguous quaternion blend')
 real/=length;dual/=length;dual-=real*np.dot(real,dual)
 q=Quaternion(tuple(real));d=Quaternion(tuple(dual));translation=d@q.conjugated()
 return q@Vector(point)+Vector((2*translation.x,2*translation.y,2*translation.z))

def inverse_lbs_delta(point, transforms, binding, minimum_determinant=1e-5):
 matrix=blended_skin_matrix(transforms,binding);det=float(np.linalg.det(matrix[:3,:3]))
 if abs(det)<minimum_determinant:raise ValueError(f'Singular inverse skin matrix: {det}')
 target=dual_quaternion_target(point,transforms,binding)
 preskin=np.linalg.solve(matrix[:3,:3],np.array(target)-matrix[:3,3])
 return preskin-np.array(point), {'determinant':det,'deltaMagnitudeM':float(np.linalg.norm(preskin-np.array(point)))}
