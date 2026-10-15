# High-pulldown pilot · start here

## Initial stage: M0 / independent audit (no animation rewrites)
Review the **current** seated high-pulldown animation and machine before another makeover. Do not re-introduce procedural fingers: the user requested original anatomy hands.

### Owner-facing milestones
- **M0: Baseline freeze.** Exact commit SHA, `anatomy-pulldown.glb` SHA256, existing tests, baseline full-rep video, frame sheets. User receives summary. No behavior changes yet.
- **M1: Motion audit.** biomechanical, visual, exercise-science and software-QA reviewers independently assess M0 evidence. Output ranked K/V/S findings; user approves priority and next scope. Missing evidence must be INCONCLUSIVE.
- **M2: Targeted repairs.** one implementation owner fixes only accepted P0/P1 issues. Re-run measurement and rendered evidence, re-review new SHA. Two cycles max before returning to owner.
- **M3: Sign-off.** four reports, original vs changed recording and limitations. User explicitly approves before Ready/merge.

### First audit questions
1. Are both palms and original source finger structures oriented plausibly across the rep? Are hands actually attached to bar after applying both GLB/model and machine transforms? Positional IK targets are not enough.
2. Does scapulothoracic motion occur, with no clipping/abrupt loss of muscle continuity as arms transition overhead to pulldown? Identify actual rig bones/mesh weights and what is stylized.
3. Does shoulder/elbow kinematics preserve plausible segment length and avoid unexpected posterior elbow bend? Do not force a fixed scapulohumeral ratio.
4. Do the machine's bar/stack/cables agree with the baked Blender clip at all sampled times, even after seek, loop and speed changes?
5. Does the user-visible muscle role color update on real `anatomyId` structures, without implying muscle activation simulation?
6. Are there new browser or GLB regressions (click target, origin scale, material switch, scene FPS)?

### Exact initial prompt to the Codex orchestrator
In the Muscle Atlas working tree, read AGENTS.md, docs/quality/motion-workflow.md and docs/quality/lat-pulldown-acceptance.md. This is M0+M1 **read-only audit** of current lat pulldown, not authorization to rebuild hands or change production assets. Freeze commit/GLB SHA and run existing build/unit/browser/GLB checks where available. Generate production-rendered full-rep video, 0/25/50/75/100% front/side/back/hand close-up frames, and 21+ sampled joint/hand-bar/stack/cable trajectories with units. If subagents are supported, spawn the four named review agents (biomechanics_reviewer, visual_reviewer, exercise_science_reviewer, software_qa_reviewer) with separate instructions to independently review the SAME frozen SHA and evidence bundle; do not share verdicts before they are complete, and do not let reviewers edit. If subagents fail to spawn, disclose and run separate read-only review sessions. Synthesize P0/P1/P2 defect log, exact evidence locations, unresolved uncertainties. Return to user to approve repair scope. Do not claim real physiological muscle-force or 'percentage stimulation' from coloration. Do not merge main.

### Evidence package
Recommended directory in local working copy (usually not tracked):
`artifacts/reviews/lat-pulldown/<commit>/` with `manifest.json`, `full-rep.mp4`, `joint-trajectories.csv`, and `frames/{front,side,back,grip}/{0,25,50,75,100}.png`; plus four review reports.
Use `node scripts/quality/validate-review-bundle.mjs path/to/manifest.json` to check completeness. This does not judge whether reports are correct.

Minimal manifest data model:
```json
{
  "commit":"40_lowercase_hex_chars",
  "anatomyGlbSha256":"64_lowercase_hex_chars",
  "exercise":"lat-pulldown",
  "variant":"seated-front-pulldown",
  "video":"full-rep.mp4",
  "trajectoryCsv":"joint-trajectories.csv",
  "frames":{"front":{"0":"frames/front/0.png","25":"frames/front/25.png","50":"frames/front/50.png","75":"frames/front/75.png","100":"frames/front/100.png"}},
  "reviews":{"biomechanics":{"file":"biomechanics.md","verdict":"INCONCLUSIVE"}},
  "userApproval":"pending",
  "readyForMerge":false
}
```
The snippet above is intentionally partial; provide all four views and four reviews before running the validator.
