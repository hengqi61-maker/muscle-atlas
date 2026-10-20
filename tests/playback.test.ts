import {describe, expect, it} from 'vitest';
import {diagnosticPatch, exerciseEntry, exerciseButtonLabel, isDiagnostic, sceneLabel, trainingPatch} from '../src/motion/playback';

describe('playback kinds', () => {
  it('training pulldown never selects a diagnostic clip or unified probe', () => {
    const p = trainingPatch('lat-pulldown');
    expect(p.playbackKind).toBe('training-unverified');
    expect(p.motionVersion).toBe('original');
    expect(p.model).toBe('pulldown');
    expect(isDiagnostic(p.playbackKind)).toBe(false);
    expect(exerciseButtonLabel('lat-pulldown')).toBe('高位下拉');
    expect(sceneLabel(p.playbackKind, 'lat-pulldown').title).toContain('实验预览');
    expect(sceneLabel(p.playbackKind, 'lat-pulldown').detail).toContain('未通过验收');
    expect(sceneLabel(p.playbackKind, 'lat-pulldown').title).not.toContain('DIAGNOSTIC');
  });

  it('diagnostic patch is explicit and does not reuse the training title', () => {
    const p = diagnosticPatch('PulldownProbe');
    expect(p.playbackKind).toBe('diagnostic');
    expect(p.diagnosticClip).toBe('PulldownProbe');
    expect(sceneLabel(p.playbackKind, p.exerciseId).title).toContain('DIAGNOSTIC');
    expect(sceneLabel(p.playbackKind, p.exerciseId).detail).toContain('不是高位下拉');
  });

  it('training curl button label stays 哑铃弯举 even after a diagnostic visit', () => {
    diagnosticPatch('CurlProbe');
    expect(exerciseButtonLabel('dumbbell-curl')).toBe('哑铃弯举');
    expect(trainingPatch('dumbbell-curl').motionVersion).toBe('original');
  });
});

it('direct exercise links always restore the seated production scene instead of a probe',()=>{
  expect(exerciseEntry('?exercise=lat-pulldown')).toMatchObject({mode:'exercise',model:'pulldown',motionVersion:'original',playbackKind:'training-unverified',diagnosticClip:null});
  expect(exerciseEntry('?exercise=PulldownProbe')).toBeNull();
});
