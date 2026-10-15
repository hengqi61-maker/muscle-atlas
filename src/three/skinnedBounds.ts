import * as THREE from 'three';

/** A conservative enclosure of linear-blend skinning, without visiting vertices per pose.
 * Every positively weighted bone receives the vertex in that bone's bind space.
 * A union AABB contains every transformed influence and therefore its convex blend.
 * This applies to normalized nonnegative skin weights and geometry without morphs.
 */
export function createSkinnedBounds(mesh:THREE.SkinnedMesh){
 const positions=mesh.geometry.getAttribute('position');
 const indices=mesh.geometry.getAttribute('skinIndex');
 const weights=mesh.geometry.getAttribute('skinWeight');
 if(!positions||!indices||!weights||Object.keys(mesh.geometry.morphAttributes).length)throw new Error('Conservative skin bounds require unmorphed linear-blend geometry');
 const boxes=new Map<number,THREE.Box3>(),vertex=new THREE.Vector3(),point=new THREE.Vector3();
 for(let i=0;i<positions.count;i++){
  vertex.fromBufferAttribute(positions,i).applyMatrix4(mesh.bindMatrix);
  let total=0;
  for(let j=0;j<4;j++){
   const weight=weights.getComponent(i,j),bone=indices.getComponent(i,j);
   if(!Number.isFinite(weight)||weight<0)throw new Error('Skin bounds require nonnegative finite weights');
   total+=weight;if(weight===0)continue;
   const inverse=mesh.skeleton.boneInverses[bone];if(!inverse)throw new Error('Skin bound references a missing bone');
   let box=boxes.get(bone);if(!box){box=new THREE.Box3();boxes.set(bone,box);}
   box.expandByPoint(point.copy(vertex).applyMatrix4(inverse));
  }
  if(Math.abs(total-1)>1e-5)throw new Error('Skin bounds require normalized weights');
 }
 const union=new THREE.Box3(),transformed=new THREE.Box3(),matrix=new THREE.Matrix4();
 return ()=>{
  union.makeEmpty();
  for(const [bone,box] of boxes){
   matrix.multiplyMatrices(mesh.bindMatrixInverse,mesh.skeleton.bones[bone].matrixWorld);
   transformed.copy(box).applyMatrix4(matrix);union.union(transformed);
  }
  // Tiny expansion absorbs floating-point accumulation at the enclosure boundary.
  union.expandByScalar(1e-6);
  mesh.boundingBox??=new THREE.Box3();mesh.boundingBox.copy(union);
  mesh.boundingSphere??=new THREE.Sphere();union.getBoundingSphere(mesh.boundingSphere);
 };
}
