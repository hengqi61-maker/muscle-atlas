import { Bone, Matrix4, Object3D, Quaternion, Vector3 } from "three";
export const DIGITS = ["Thumb", "Index", "Middle", "Ring", "Little"] as const;
export type Digit = (typeof DIGITS)[number];
export type Side = "Left" | "Right";
export const CHAIN: Record<Digit, string[]> = {
  Thumb: ["CMC", "MCP", "IP"],
  Index: ["MCP", "PIP", "DIP"],
  Middle: ["MCP", "PIP", "DIP"],
  Ring: ["MCP", "PIP", "DIP"],
  Little: ["MCP", "PIP", "DIP"],
};
export type Pose = Record<string, number>;
export interface Joint {
  bone: Bone;
  reference: Quaternion;
  flex: Vector3;
  opposition: Vector3;
  length: number;
  tip: Vector3;
  min: number;
  max: number;
  digit: Digit;
  index: number;
}
export class HandRigAdapter {
  readonly joints: Joint[] = [];
  readonly hand: Bone;
  readonly socket: Bone;
  readonly axisProvenance =
    "GLB authored local basis, build.py align_roll; NOT calibrated anatomical axes";
  constructor(
    readonly root: Object3D,
    readonly side: Side,
  ) {
    const bone = (name: string) => {
      const b = root.getObjectByName(name);
      if (!(b instanceof Bone)) throw Error(`MISSING_BONE:${name}`);
      return b;
    };
    this.hand = bone(`${side}Hand`);
    this.socket = bone(`${side}FingerSocket`);
    for (const digit of DIGITS) {
      let parent: Bone = this.socket;
      const bones = CHAIN[digit].map((j) => bone(`${side}${digit}${j}`));
      bones.forEach((b, index) => {
        if (b.parent !== parent) throw Error(`INVALID_HIERARCHY:${b.name}`);
        parent = b;
        if (
          ![...b.quaternion.toArray(), ...b.position.toArray()].every(
            Number.isFinite,
          ) ||
          Math.abs(b.quaternion.length() - 1) > 1e-4
        )
          throw Error(`INVALID_REFERENCE:${b.name}`);
        const offset =
          bones[index + 1]?.position.clone() ?? bones[index].position.clone();
        // Distal tail is not stored in glTF: inherited equal-segment authored length, explicitly a proxy.
        if (index === 2) offset.set(0, bones[1].position.length(), 0);
        const length = offset.length();
        if (length < 1e-6) throw Error(`ZERO_LENGTH:${b.name}`);
        this.joints.push({
          bone: b,
          reference: b.quaternion.clone(),
          flex: new Vector3(1, 0, 0),
          opposition: new Vector3(0, 1, 0),
          length,
          tip: offset,
          min: 0,
          max:
            digit === "Thumb"
              ? [0.35, 1.15, 1.05][index]
              : [1.15, 1.25, 0.85][index],
          digit,
          index,
        });
      });
    }
    if (!this.socket.parent || this.socket.parent !== this.hand)
      throw Error("INVALID_SOCKET_PARENT");
  }
  clamp(pose: Pose): Pose {
    return Object.fromEntries(
      this.joints.map((j) => [
        j.bone.name,
        Math.max(
          j.min,
          Math.min(
            j.max,
            Number.isFinite(pose[j.bone.name]) ? pose[j.bone.name] : 0,
          ),
        ),
      ]),
    );
  }
  apply(pose: Pose, opposition = 0) {
    const bounded = this.clamp(pose);
    for (const j of this.joints) {
      const q = new Quaternion().setFromAxisAngle(j.flex, bounded[j.bone.name]);
      if (j.digit === "Thumb" && j.index === 0)
        q.premultiply(
          new Quaternion().setFromAxisAngle(
            j.opposition,
            Math.max(0, Math.min(0.55, opposition)) *
              (this.side === "Left" ? 1 : -1),
          ),
        );
      j.bone.quaternion.copy(j.reference).multiply(q);
    }
    this.socket.updateWorldMatrix(true, true);
    return bounded;
  }
  reset() {
    for (const j of this.joints) j.bone.quaternion.copy(j.reference);
    this.root.updateMatrixWorld(true);
  }
  frame() {
    this.root.updateMatrixWorld(true);
    return this.hand.matrixWorld.clone();
  }
  convert(point: Vector3, from: Matrix4, to: Matrix4) {
    return point.clone().applyMatrix4(from).applyMatrix4(to.clone().invert());
  }
  axisWorld(j: Joint) {
    return j.flex.clone().transformDirection(j.bone.matrixWorld);
  }
  segments() {
    return this.joints.map((j) => ({
      name: j.bone.name,
      digit: j.digit,
      index: j.index,
      from: j.bone.getWorldPosition(new Vector3()),
      to: j.bone.localToWorld(j.tip.clone()),
      radius: 0.004,
    }));
  }
  mirror(pose: Pose): Pose {
    return Object.fromEntries(
      Object.entries(pose).map(([k, v]) => [
        k.replace(/^Left|^Right/, this.side),
        v,
      ]),
    );
  }
  preset(amount: number): Pose {
    return Object.fromEntries(
      this.joints.map((j) => [
        j.bone.name,
        j.max * Math.max(0, Math.min(1, amount)),
      ]),
    );
  }
}
