import { create } from "zustand";
import type { Side, Digit } from "./HandRigAdapter";
export interface HandControl {
  amount: number;
  joints: Record<string, number>;
  digits: Record<Digit, number>;
  opposition: number;
  auto: boolean;
  released: boolean;
  anchor: boolean;
}
const initial = (): HandControl => ({
  joints: {},
  amount: 0.45,
  digits: { Thumb: 0.45, Index: 0.45, Middle: 0.45, Ring: 0.45, Little: 0.45 },
  opposition: 0.25,
  auto: false,
  released: false,
  anchor: false,
});
interface State {
  enabled: boolean;
  side: Side;
  kind: "bar" | "dumbbell" | "rope";
  radius: number;
  offset: number;
  axes: boolean;
  revision: number;
  hands: Record<Side, HandControl>;
  report: Record<string, unknown>;
  set: (patch: Partial<State>) => void;
  hand: (side: Side, patch: Partial<HandControl>) => void;
  reset: () => void;
}
export const useGrasp = create<State>((set) => ({
  enabled: false,
  side: "Left",
  kind: "bar",
  radius: 0.024,
  offset: 0,
  axes: true,
  revision: 0,
  hands: { Left: initial(), Right: initial() },
  report: {},
  set: (patch) => set((s) => ({ ...patch, revision: s.revision + 1 })),
  hand: (side, patch) =>
    set((s) => ({
      hands: { ...s.hands, [side]: { ...s.hands[side], ...patch } },
      revision: s.revision + 1,
    })),
  reset: () =>
    set((s) => ({
      hands: { Left: initial(), Right: initial() },
      offset: 0,
      revision: s.revision + 1,
    })),
}));
