import {describe,it,expect} from 'vitest';
import {advance,elbowAngle,togglePlayback,DURATION} from '../src/three/animation';
import {resolveState,appearance} from '../src/three/materials';
import {completedCounts} from '../src/data/db';
describe('joint playback',()=>{it('moves elbow through a full cycle',()=>{expect(elbowAngle(2)).toBeCloseTo(-2.05);expect(elbowAngle(4)).toBeCloseTo(elbowAngle(0));});it('stops or wraps correctly',()=>{expect(advance(3.9,.2,1,false)).toBe(4);expect(advance(3.9,.2,1,true)).toBeCloseTo(.1);});});
describe('independent material states',()=>{it('keeps hidden and selection precedence',()=>{expect(resolveState('a','a','a',['a'],'primary')).toBe('hidden');expect(resolveState('a','a','a',[],'primary')).toBe('selected');expect(resolveState('b','a',null,[])).toBe('dimmed');});it('shares states across styles',()=>{expect(appearance('selected','real').color).toBe(appearance('selected','clean').color);});});
it('counts actual sets only',()=>{expect(completedCounts([{id:'s',date:'2026-10-15',sets:[{id:'1',exerciseId:'dumbbell-curl',weight:8,reps:10,rir:2}],notes:''}])).toBe(1);});

import {catalogue} from '../src/data/catalogue';
it('preserves distinct mesh identity when ontology IDs are shared',()=>{expect(catalogue).toHaveLength(467);expect(new Set(catalogue.map(r=>r.anatomyId)).size).toBe(467);expect(new Set(catalogue.map(r=>r.meshName)).size).toBe(467);});

it('restarts a finished clip while preserving pause and resume positions',()=>{
 expect(togglePlayback(DURATION,false)).toEqual({time:0,playing:true});
 expect(togglePlayback(1.7,false)).toEqual({time:1.7,playing:true});
 expect(togglePlayback(1.7,true)).toEqual({time:1.7,playing:false});
});
