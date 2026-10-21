import { Quaternion } from "three";
import { HandRigAdapter, type Pose } from "./HandRigAdapter";
/** Single owner: call after AnimationMixer.setTime and before skeleton/bounds updates. */
export class HandPoseLayer {
  private target: Pose;
  private current: Pose;
  private opposition = 0;
  private currentOpposition = 0;
  private released = false;
  private animation = new Map<string, Quaternion>();
  constructor(readonly rig: HandRigAdapter) {
    this.target = rig.preset(0);
    this.current = { ...this.target };
  }
  set(pose: Pose, opposition = 0) {
    this.target = this.rig.clamp(pose);
    this.opposition = opposition;
    this.released = false;
  }
  release() {
    this.released = true;
  }
  reset() {
    this.target = this.rig.preset(0);
    this.current = { ...this.target };
    this.opposition = 0;
    this.currentOpposition = 0;
    this.released = false;
    this.rig.reset();
  }
  /** Restore pre-layer animation first, even if mixer does not key a finger. Prevents accumulation. */
  beforeMixer() {
    for (const j of this.rig.joints) {
      const q = this.animation.get(j.bone.name);
      if (q) j.bone.quaternion.copy(q);
    }
  }
  captureAnimation() {
    for (const j of this.rig.joints)
      this.animation.set(j.bone.name, j.bone.quaternion.clone());
  }
  afterMixer(delta: number, snap = false, capture = true) {
    if (capture) this.captureAnimation();
    if (this.released) return;
    const alpha = snap
      ? 1
      : 1 - Math.exp(-Math.max(0, Math.min(delta, 0.1)) * 16);
    for (const k of Object.keys(this.target)) {
      this.current[k] += (this.target[k] - this.current[k]) * alpha;
      if (Math.abs(this.current[k] - this.target[k]) < 1e-6)
        this.current[k] = this.target[k];
    }
    this.currentOpposition +=
      (this.opposition - this.currentOpposition) * alpha;
    if (Math.abs(this.currentOpposition - this.opposition) < 1e-6)
      this.currentOpposition = this.opposition;
    this.rig.apply(this.current, this.currentOpposition);
  }
  get transitioning() {
    return (
      !this.released &&
      (Object.keys(this.target).some(
        (k) => Math.abs(this.current[k] - this.target[k]) > 1e-6,
      ) ||
        Math.abs(this.currentOpposition - this.opposition) > 1e-6)
    );
  }
  get pose() {
    return { ...this.current };
  }
}
