/** Training vs diagnostic playback. Diagnostic clips must never own the lat-pulldown entry. */
export type PlaybackKind = 'training-unverified' | 'diagnostic';
export type ExerciseId = 'dumbbell-curl' | 'lat-pulldown';
export type DiagnosticClip = 'PulldownProbe' | 'CurlProbe';

export function isDiagnostic(kind: PlaybackKind) {
  return kind === 'diagnostic';
}

export function trainingPatch(exerciseId: ExerciseId) {
  return {
    playbackKind: 'training-unverified' as const,
    motionVersion: 'original' as const,
    exerciseId,
    model: (exerciseId === 'lat-pulldown' ? 'pulldown' : 'rigged') as 'pulldown' | 'rigged',
    time: 0,
    playing: false,
    selected: null,
    focus: (exerciseId === 'lat-pulldown' ? 'full' : 'arm') as 'full' | 'arm',
  };
}

export function diagnosticPatch(clip: DiagnosticClip) {
  return {
    playbackKind: 'diagnostic' as const,
    motionVersion: 'unified' as const,
    exerciseId: (clip === 'PulldownProbe' ? 'lat-pulldown' : 'dumbbell-curl') as ExerciseId,
    model: (clip === 'PulldownProbe' ? 'pulldown' : 'rigged') as 'pulldown' | 'rigged',
    diagnosticClip: clip,
    time: 0,
    playing: false,
    selected: null,
    focus: 'full' as const,
  };
}

export function sceneLabel(kind: PlaybackKind, exerciseId: ExerciseId) {
  if (kind === 'diagnostic') {
    return {
      title: exerciseId === 'lat-pulldown' ? 'DIAGNOSTIC · 肩肘活动测试' : 'DIAGNOSTIC · 肘部活动测试',
      detail: '无坐姿、无横杆、无抓握。不是高位下拉 / 弯举教学示范。',
    };
  }
  if (exerciseId === 'lat-pulldown') {
    return {
      title: '高位下拉 · 实验预览',
      detail: '坐姿器械联动 · 抓握与组织形变未通过验收',
    };
  }
  return {
    title: '哑铃弯举 · 实验预览',
    detail: '真实解剖 · 原始手部网格 · 肘窝形变仍待精修',
  };
}

export function exerciseButtonLabel(exerciseId: ExerciseId) {
  return exerciseId === 'lat-pulldown' ? '高位下拉' : '哑铃弯举';
}
