import {it,expect} from 'vitest';
import * as THREE from 'three';
import {createSkinnedBounds} from '../src/three/skinnedBounds';

it('encloses every actual blended vertex under changing bone transforms and mesh bind transforms',()=>{
 const geometry=new THREE.BufferGeometry();
 const positions=[-.6,.2,.1,.4,.9,-.2,.8,-.4,.3,-.1,.5,-.7];
 geometry.setAttribute('position',new THREE.Float32BufferAttribute(positions,3));
 geometry.setAttribute('skinIndex',new THREE.Uint16BufferAttribute([0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0],4));
 geometry.setAttribute('skinWeight',new THREE.Float32BufferAttribute([.25,.75,0,0,.5,.5,0,0,1,0,0,0,.1,.9,0,0],4));
 const bones=[new THREE.Bone(),new THREE.Bone()];bones[0].add(bones[1]);bones[1].position.y=.4;
 const mesh=new THREE.SkinnedMesh(geometry,new THREE.MeshBasicMaterial());mesh.add(bones[0]);
 mesh.position.set(.3,-.2,.5);mesh.rotation.y=.25;mesh.updateMatrixWorld(true);mesh.bind(new THREE.Skeleton(bones));
 const update=createSkinnedBounds(mesh),point=new THREE.Vector3();
 for(let i=0;i<30;i++){
  bones[0].rotation.set(Math.sin(i)*.8,Math.cos(i*.3),i*.1);
  bones[1].rotation.set(i*.23,Math.cos(i),Math.sin(i*.7));bones[1].position.x=Math.sin(i)*.3;
  mesh.updateMatrixWorld(true);update();
  for(let vertex=0;vertex<4;vertex++){
   mesh.getVertexPosition(vertex,point);
   expect(mesh.boundingBox!.containsPoint(point)).toBe(true);
   expect(point.distanceTo(mesh.boundingSphere!.center)).toBeLessThanOrEqual(mesh.boundingSphere!.radius+1e-6);
  }
 }
});
