import { Bone, Euler, Matrix4, Object3D, Quaternion, Vector3 } from "three";
import type { HandRigAdapter } from "./HandRigAdapter";
/** Bounded reference-relation constraint, separate from finger/tissue contact acceptance.
 * Limits bound correction relative to the animated pose, not anatomical ROM claims.
 */
export class GripAnchor {
  private relation: Matrix4 | null = null;
  private animation: Quaternion[] = [];
  private chain: Bone[];
  constructor(
    readonly rig: HandRigAdapter,
    readonly correctionLimit = 0.35,
  ) {
    this.chain = ["Humerus", "Forearm", "Wrist"].map((s) => {
      const b = rig.root.getObjectByName(`${rig.side}${s}`);
      if (!(b instanceof Bone)) throw Error("MISSING_ARM_CHAIN");
      return b;
    });
  }
  capture(handleWorld: Matrix4) {
    this.relation = handleWorld.clone().invert().multiply(this.rig.frame());
  }
  release() {
    this.relation = null;
  }
  beforeMixer() {
    this.chain.forEach((b, i) => {
      if (this.animation[i]) b.quaternion.copy(this.animation[i]);
    });
  }
  update(handleWorld: Matrix4, maxSweeps = 8) {
    this.animation = this.chain.map((b) => b.quaternion.clone());
    if (!this.relation) return { status: "RELEASED" };
    if (!Number.isInteger(maxSweeps) || maxSweeps < 1 || maxSweeps > 16)
      throw Error("INVALID_ARM_BUDGET");
    const desired = handleWorld.clone().multiply(this.relation),
      goal = new Vector3().setFromMatrixPosition(desired),
      goalQ = new Quaternion().setFromRotationMatrix(desired),
      angles = Array(9).fill(0);
    let evaluations = 0;
    const apply = () => {
      this.chain.forEach((b, i) =>
        b.quaternion
          .copy(this.animation[i])
          .multiply(
            new Quaternion().setFromEuler(
              new Euler(
                angles[i * 3],
                angles[i * 3 + 1],
                angles[i * 3 + 2],
                "ZYX",
              ),
            ),
          ),
      );
      this.chain[0].updateWorldMatrix(true, true);
    };
    const score = () => {
      apply();
      evaluations++;
      const p = this.rig.hand.getWorldPosition(new Vector3()),
        q = this.rig.hand.getWorldQuaternion(new Quaternion());
      return p.distanceToSquared(goal) + q.angleTo(goalQ) ** 2 * 0.0025;
    };
    let best = score();
    for (let n = 0; n < maxSweeps; n++) {
      const step = 0.16 * Math.pow(0.65, n);
      for (let i = 0; i < angles.length; i++) {
        const old = angles[i];
        let chosen = old;
        for (const d of [-step, step]) {
          angles[i] = Math.max(
            -this.correctionLimit,
            Math.min(this.correctionLimit, old + d),
          );
          const value = score();
          if (value < best) {
            best = value;
            chosen = angles[i];
          }
        }
        angles[i] = chosen;
      }
    }
    apply();
    const positionResidualM = this.rig.hand
        .getWorldPosition(new Vector3())
        .distanceTo(goal),
      rotationResidualRad = this.rig.hand
        .getWorldQuaternion(new Quaternion())
        .angleTo(goalQ);
    return {
      status:
        positionResidualM < 0.001 && rotationResidualRad < 0.01
          ? "REFERENCE_HELD"
          : "REFERENCE_UNREACHABLE",
      positionResidualM,
      rotationResidualRad,
      evaluations,
      correctionBoundRad: this.correctionLimit,
      scope: "animated arm delta bound, not physiological ROM or grasp PASS",
    };
  }
}
