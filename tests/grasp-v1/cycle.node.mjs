import test from 'node:test';
import assert from 'node:assert/strict';
import {poseFor, lerpPose, cyclePose, boneName} from '../../src/grasp-v1/controller.mjs';

test('open-closed-open returns to open and peaks at mid', () => {
  const open = poseFor('open', 'Left');
  const closed = poseFor('closed', 'Left');
  const k = boneName('Left', 'Index', 'MCP');
  const a = cyclePose('Left', 0);
  const mid = cyclePose('Left', 0.5);
  const end = cyclePose('Left', 1);
  assert.equal(a[k].x, open[k].x);
  assert.equal(end[k].x, open[k].x);
  assert.ok(Math.abs(mid[k].x - closed[k].x) < 1e-12);
  const q = cyclePose('Left', 0.25);
  assert.ok(q[k].x > a[k].x && q[k].x < mid[k].x);
});

test('cycle is time-symmetric around 0.5', () => {
  const k = boneName('Right', 'Thumb', 'CMC');
  const a = cyclePose('Right', 0.2);
  const b = cyclePose('Right', 0.8);
  assert.ok(Math.abs(a[k].x - b[k].x) < 1e-12);
  assert.ok(Math.abs(a[k].y - b[k].y) < 1e-12);
});

test('lerp endpoints survive panel-style merge', () => {
  const pose = {...poseFor('pulldown-bar', 'Left'), ...poseFor('pulldown-bar', 'Right')};
  assert.equal(Object.keys(pose).length, 30);
  const mid = lerpPose(poseFor('open', 'Left'), poseFor('closed', 'Left'), 0.5);
  assert.ok(mid[boneName('Left', 'Little', 'DIP')].x > 0);
});
