import {test} from 'node:test';import assert from 'node:assert/strict';import {Vector3,Box3} from 'three';import {triangleBox} from '../../../scripts/quality/motion-quality-geometry.mjs';
test('SAT finds crossing triangle with all vertices outside box',()=>{const box=new Box3(new Vector3(-1,-1,-1),new Vector3(1,1,1));assert(triangleBox(new Vector3(-2,0,0),new Vector3(2,0,0),new Vector3(0,2,0),box));assert(!triangleBox(new Vector3(2,2,2),new Vector3(3,2,2),new Vector3(2,3,2),box))});
import {area} from '../../../scripts/quality/motion-quality-geometry.mjs';
test('area detects flattening independently of translation and initial posture',()=>{const a=new Vector3(0,0,0),b=new Vector3(1,0,0),c=new Vector3(0,1,0);assert.equal(area(a,b,c),.5);assert.equal(area(a,b,new Vector3(.5,0,0)),0);const shift=new Vector3(2,3,4);assert.equal(area(a.clone().add(shift),b.clone().add(shift),c.clone().add(shift)),.5)});
import {severeCollapse} from '../../../scripts/quality/motion-quality-geometry.mjs';
test('collapse alarms use either absolute or relative affected-triangle count',()=>{assert(severeCollapse(4,1000));assert(severeCollapse(2,100));assert(!severeCollapse(1,1000))});
