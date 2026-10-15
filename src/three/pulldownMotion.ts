/** One deterministic rep, independent from the rendering loop.
 * 0 = overhead, 0.5 = pulled to upper chest, 1 = overhead again.
 * Measurements in metres in the machine's local Y-up coordinate frame.
 */
export function latPulldownPhase(progress: number): number {
  const p = Number.isFinite(progress) ? Math.min(1, Math.max(0, progress)) : 0;
  return (1 - Math.cos(2 * Math.PI * p)) / 2;
}
export function latPulldownFrame(progress: number) {
  const phase = latPulldownPhase(progress);
  const barY = 1.96 - 0.49 * phase;
  const weightY = 0.42 + 0.49 * phase;
  return {
    phase, barY, weightY,
    leftGrip: [-0.525, barY - 0.055, 0.54] as const,
    rightGrip: [0.525, barY - 0.055, 0.54] as const
  };
}
