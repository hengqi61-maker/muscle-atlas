# Muscle Atlas · Motion quality process (milestone control)

## Scope and decision authority
Local-first personal anatomy/training app. The user is Milestone Owner. No subagent may merge a PR, modify main, approve licensing purchases, OAuth, destructive actions, or label animation medically validated.

## Roles
- Orchestrator (root): writes a scoped acceptance contract, assigns one implementation owner, freezes a candidate commit, waits for independent reviews, collates defects, and presents evidence to owner.
- Developer / Animation engineer: may implement in a feature branch or isolated worktree, provide reproducible build and reference assets. Must not self-approve.
- biomechanics_reviewer: review-only joint/segment/contact/kinematic plausibility.
- visual_reviewer: review-only multi-view rendering, grip orientation, anatomical continuity and machine scale.
- exercise_science_reviewer: review-only exercise purpose, muscle role tags, confidence and citations.
- software_qa_reviewer: review-only tests, GLB structure, regression, data safety and perf.

## Sequence
1. **Scope gate / brief**: one exercise variant, source of truth reference(s), initial and bottom poses, machine/user scale assumptions, expected involvement, explicit exclusions. Freeze canonical coordinate system and candidate commit SHA.
2. **Build**: animation and R3F can proceed in separate worktrees but the integration owner alone combines them. Validate fresh build and source mesh IDs. Save generated files with documented asset provenance and checksums.
3. **Mechanical gate**: deterministic sample at 0/25/50/75/100% of a full rep (plus intermediate frames for joints) with hand contact, limb length, shoulder/scapula tracking, bar-weight-cable timing and collisions. Report measurements with units and algorithms; no arbitrary 'sub-millimetre grip error implies correct exercise'.
4. **Visual gate**: capture reproducible rendered front, side, back and hand-close-up at those timestamps, with camera/preset metadata, from production render (not illustration). Review both anatomy styles if changed.
5. **Science gate**: trace anatomyId muscle roles, distinguish role highlighting from skeletal motion, skinned deformation and model-based force; references for any exercise claims.
6. **Software gate**: npm ci, npm run build, npm test, npx playwright test; GLB validation, ID invariants and actual reload/picking/style/seek regression. These are necessary, NOT sufficient.
7. **Review gate**: reviewers get a frozen SHA and evidence bundle. They output independent JSON/Markdown reports; do not edit code or view each other's verdict before submission. Missing evidence -> INCONCLUSIVE, never PASS.
8. **Repair**: orchestrator merges sorted findings (P0 stop, P1 must-fix, P2 improvement), assigns owner; implement smallest change; regenerate affected evidence; reviewers re-review the new SHA. Maximum two automatic full review/rework cycles per milestone; then escalate unresolved issues.
9. **Owner gate**: present a 30–60 s actual screen recording, 4-angle contact sheet, test summary, known limits and exact build SHA. Only user approval authorizes mark Ready and manual merge.

## Failure taxonomy
- P0 blocker: lost source identity; nonfunctional controls; invalid GLB/major crashes; unsafe model claims; obvious reversed grips/joint dislocation; unlicensed assets.
- P1 blocker: wrong scapulohumeral pattern without explanation; persistent clipping at hands/seat/thigh pad; bar and hand diverge; missing evidentiary views; break in previously working anatomy interaction.
- P2: secondary visual polish (materials, proportions, subtle deformation) that does not conceal P0/P1.
Review judgment is falsifiable: file/mesh/frame/camera, expected vs actual, severity, reproduction, confidence, proposed verification. A review finding without evidence is an observation, not a verified blocker.

## Data and traceability
Do not confuse original BP3D/Z-Anatomy meshes with procedural grip overlays. Store source version and license separately. Keep `anatomyId` stable across rig/animation. A skill/prompt is not a sandbox: subagents inherit parent permission. Reviewers are instructed read-only and changes must be restricted by workflow, separate worktrees, and PR approval.

## Pilot
See `docs/quality/lat-pulldown-acceptance.md`. The current pulldown clips the model animation and the machine via a shared four-second playback clock, but that alone does not establish biomechanical fidelity.
