# Hand topology limit (G2) and minimal overlay proposal

## Limit — do not hide this

The frozen 467-identity source has **muscle and tendon sets**, not a palmar skin shell and not five finger pads. G2 close-ups and class isolation shots make this visible:

- Thenar / hypothenar / adductor are bulk pads around the bar.
- Lumbricals and interossei are thin disconnected slips.
- Long pollicis tendons are forearm-to-thumb cords.
- No MCP / PIP / DIP pulp, no nail, no palmar crease surface.

G1’s 30 additive bones can move those existing vertices (lumbricals ~45 mm closed vs open). That is **tissue displacement**, not a recognizable five-finger grasp. Weight retuning cannot invent missing phalanx surfaces.

Therefore G2 contact vs the pulldown-diameter bar is `PERSISTENT_INTERSECTION` of palmar muscle through a rest-height cylinder. It is not a wrap formed by digits.

## Minimal enhancement that keeps source identities

Proposed next experiment only — **not implemented in this PR**, not a production GLB, not Owner anatomy approval.

1. New isolated object `grasp-v1-skin-shell` in the experimental worktree only.
2. Six islands: one palm disk + five digit chains (three capsules each: proximal / middle / distal; thumb CMC/MCP/IP).
3. Bind 100% to the existing 30 additive bones. Do not edit the 467 source POSITION bytes, names, FMA/BP IDs, or faces.
4. Keep source meshes visible in every contact packet. Overlay wrap and source-muscle intersection are reported **side by side**. Never hide source to make a still look clean.
5. Status: `disposable geometric proxy`. Not BP3D / Z-Anatomy. Not clinical ROM.

If overlay wrap later PASSes while source muscle still intersects, the packet stays FAIL for source contact. Overlay is a visibility/control surface, not a substitute hand.

## Rejected shortcuts

- Re-weighting lumbricals until they “look like fingers”
- Deleting or merging source sets
- Claiming pulldown/curl PASS from a local bar fixture
- Starting Face Pull as a way to avoid this gap
