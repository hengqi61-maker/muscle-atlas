import test from 'node:test';import assert from 'node:assert/strict';import {metrics,severeAlarm} from '../../scripts/rig-v2/attribution/analyze.mjs';
test('actual triangle area and edge metrics detect compression without centroid proxy',()=>{const m=metrics([0,0,0,1,0,0,0,.02,0],0,1,2,.5,[1,Math.sqrt(2),1]);assert.ok(Math.abs(m.areaRatio-.02)<1e-12);assert.ok(m.maxEdgeStretch>=1)});
test('unaltered severe OR rule detects absolute and fractional alarms',()=>{assert.equal(severeAlarm(4,4000),true);assert.equal(severeAlarm(1,20),true);assert.equal(severeAlarm(3,1000),false)});
test('degenerate immutable source triangle is excluded from area ratio',()=>assert.equal(metrics([0,0,0,1,0,0,2,0,0],0,1,2,0,[1,1,2]).areaRatio,null));
