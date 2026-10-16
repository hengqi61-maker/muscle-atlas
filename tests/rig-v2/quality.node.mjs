import {test} from 'node:test';
import assert from 'node:assert/strict';
import {Vector3,Matrix4} from 'three';
import {determinant,triangleMetrics} from '../../scripts/quality/rig-v2-audit.mjs';
test('determinant detects reflection independently of translation',()=>{assert.equal(determinant(new Matrix4().makeTranslation(5,-3,2).toArray()),1);assert.equal(determinant(new Matrix4().makeScale(-1,1,1).toArray()),-1)});
test('triangle collapse screen catches area loss despite finite vertices',()=>{const p=(x,y)=>new Vector3(x,y,0);assert.equal(triangleMetrics(p(0,0),p(1,0),p(0,1),.5).ratio,1);assert.equal(triangleMetrics(p(0,0),p(1,0),p(.5,0),.5).collapsed,true);assert.equal(triangleMetrics(p(0,0),p(1,0),p(0,1e-5),.5).collapsed,true)});
test('uniform rotation preserves triangle area',()=>{const v=[new Vector3(),new Vector3(1,0,0),new Vector3(0,1,0)].map(p=>p.applyMatrix4(new Matrix4().makeRotationY(.73)));assert.ok(Math.abs(triangleMetrics(...v,.5).ratio-1)<1e-12)});

test('known fold triggers unchanged M2 severe area alarm while above numeric zero threshold',()=>{const p=(x,y)=>new Vector3(x,y,0);const m=triangleMetrics(p(0,0),p(1,0),p(0,.02),.5);assert.ok(m.ratio<.05);assert.ok(m.ratio>1e-4);assert.equal(m.collapsed,false)});
import {severeCollapse} from '../../scripts/quality/motion-quality-geometry.mjs';
test('existing M2 OR alarm retains absolute-only and fraction-only detection',()=>{assert.equal(severeCollapse(4,4000),true);assert.equal(severeCollapse(1,20),true);assert.equal(severeCollapse(3,4000),false)});
