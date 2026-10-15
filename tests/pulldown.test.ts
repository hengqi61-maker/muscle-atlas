import {describe,it,expect} from 'vitest';
import {latPulldownFrame,latPulldownPhase} from '../src/three/pulldownMotion';
import {latPulldownAnatomyRelations} from '../src/data/latPulldown';
describe('lat pulldown equipment',()=>{
 it('returns to starting pose after one rep',()=>{
  expect(latPulldownFrame(0).barY).toBeCloseTo(latPulldownFrame(1).barY);
  expect(latPulldownFrame(0).weightY).toBeCloseTo(latPulldownFrame(1).weightY);
  expect(latPulldownPhase(NaN)).toBe(0);
 });
 it('moves bar and stack in opposite directions by equal distances',()=>{
  const top=latPulldownFrame(0),bottom=latPulldownFrame(.5);
  expect(top.barY-bottom.barY).toBeCloseTo(.44);
  expect(bottom.weightY-top.weightY).toBeCloseTo(.44);
 });
 it('maps the real Z-Anatomy lats without conflating bilateral anatomy IDs',()=>{
  const lats=latPulldownAnatomyRelations.filter(m=>m.role==='primary');
  expect(lats).toHaveLength(2);
  expect(new Set(lats.map(m=>m.anatomyId)).size).toBe(2);
 });
});
