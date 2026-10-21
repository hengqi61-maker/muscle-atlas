import { Vector3 } from "three";
import { HandRigAdapter, type Pose } from "./HandRigAdapter";
import {
  ContactValidator,
  capsuleGap,
  prepareCylinder,
  validateHandle,
  type Handle,
} from "./ContactValidator";
export class GraspSolver {
  readonly validator = new ContactValidator();
  constructor(readonly rig: HandRigAdapter) {}
  solve(
    handle: Handle,
    seed: Pose = this.rig.preset(0.45),
    opposition = 0.3,
    maxSweeps = 12,
  ) {
    validateHandle(handle);
    if (!Number.isInteger(maxSweeps) || maxSweeps < 1 || maxSweeps > 32)
      throw Error("INVALID_BUDGET");
    let pose = this.rig.clamp(seed),
      evaluations = 0;
    opposition = Math.max(0, Math.min(0.55, opposition));
    const center = new Vector3().setFromMatrixPosition(handle.matrix);
    const reach = this.rig.segments().map((s) => s.from.distanceTo(center));
    const sdf = prepareCylinder(handle);
    const objective = (p: Pose) => {
      this.rig.apply(p, opposition);
      evaluations++;
      const gaps: Record<string, number> = {};
      let penalty = 0;
      for (const segment of this.rig.segments()) {
        const gap = capsuleGap(
          segment.from,
          segment.to,
          segment.radius,
          handle,
          sdf,
        );
        gaps[segment.digit] = Math.min(gaps[segment.digit] ?? Infinity, gap);
        penalty += Math.min(0, gap) ** 2 * 10000;
      }
      return (
        penalty +
        Object.values(gaps).reduce((sum, gap) => sum + Math.max(0, gap) ** 2, 0)
      );
    };
    let best = objective(pose),
      sweeps = 0;
    for (; sweeps < maxSweeps; sweeps++) {
      let improved = false;
      const step = 0.35 * Math.pow(0.72, sweeps);
      for (const j of this.rig.joints) {
        const old = pose[j.bone.name];
        let chosen = old;
        for (const delta of [-step, step]) {
          const value = Math.max(j.min, Math.min(j.max, old + delta));
          const trial = { ...pose, [j.bone.name]: value },
            score = objective(trial);
          if (score < best - 1e-14) {
            best = score;
            chosen = value;
            improved = true;
          }
        }
        pose[j.bone.name] = chosen;
      }
      const oldOpp = opposition;
      let chosenOpp = oldOpp;
      for (const delta of [-step, step]) {
        opposition = Math.max(0, Math.min(0.55, oldOpp + delta));
        const score = objective(pose);
        if (score < best - 1e-14) {
          best = score;
          chosenOpp = opposition;
          improved = true;
        }
      }
      opposition = chosenOpp;
      if (!improved && step < 0.015) break;
    }
    this.rig.apply(pose, opposition);
    const contact = this.validator.proxy(this.rig, handle, pose);
    const residualM = Math.sqrt(best / 5);
    const targets = this.rig
      .segments()
      .filter((s) => s.index === 2)
      .map((s) => {
        const local = s.to.clone().applyMatrix4(handle.matrix.clone().invert()),
          radial = Math.hypot(local.x, local.z);
        local.y = Math.max(
          -handle.halfLength,
          Math.min(handle.halfLength, local.y),
        );
        if (radial > 1e-12) {
          local.x *= handle.radius / radial;
          local.z *= handle.radius / radial;
        } else local.x = handle.radius;
        return {
          digit: s.digit,
          world: local.applyMatrix4(handle.matrix).toArray(),
          kind: "finite-cylinder-surface-proxy",
        };
      });
    return {
      pose,
      targets,
      opposition,
      evaluations,
      sweeps: Math.min(sweeps + 1, maxSweeps),
      residualM,
      status:
        Math.min(...reach) > handle.halfLength + handle.radius + 0.1
          ? "UNREACHABLE"
          : contact.status === "PROXY_CONTACT"
            ? "PROXY_CONTACT"
            : contact.status === "PENETRATION"
              ? "PENETRATION"
              : "NOT_CONVERGED",
      contact,
    };
  }
}
