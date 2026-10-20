import test from 'node:test';
import assert from 'node:assert/strict';
import { poseFor, lerpPose, PRESETS, boneName } from '../../src/grasp-v1/controller.mjs';

test('presets are finite and left/right independent', () => {
  const L = poseFor('closed', 'Left');
  const R = poseFor('closed', 'Right');
  assert.equal(Object.keys(L).length, 15);
  assert.equal(L[boneName('Left','Index','MCP')].x > 0, true);
  assert.equal(R[boneName('Right','Index','MCP')].x > 0, true);
  assert.equal(Math.sign(L[boneName('Left','Thumb','CMC')].y), 1);
  assert.equal(Math.sign(R[boneName('Right','Thumb','CMC')].y), -1);
});

test('lerp open to closed is monotonic on Index MCP flex', () => {
  const a = poseFor('open','Left');
  const b = poseFor('closed','Left');
  const mid = lerpPose(a,b,0.5);
  const k = boneName('Left','Index','MCP');
  assert.ok(mid[k].x > a[k].x && mid[k].x < b[k].x);
});

test('all five presets exist', () => {
  for (const name of Object.keys(PRESETS)) poseFor(name,'Left');
});
