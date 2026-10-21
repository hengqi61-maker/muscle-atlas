# Cursor independent review request

Review `codex/grasp-controller-v2` against `codex/pulldown-grasp-continuation` (PR24, not merged). Do not merge main or alter production assets.

Focus on reference capture vs AnimationMixer order; per-hand independence and neutral parity; coordinate spaces and no scaled handles; solve iteration/evaluation bounds; finite capsule minimization and actual triangle clipping; source mesh ownership and inversion witnesses; packet-v1.1 provenance; idle invalidation, seek, loop, release and arm reference constraint. Verify source buffer preservation and reproducible assembly on a fresh checkout.

Read `README.md`, `acceptance.md`, evidence manifest and `.codex/workaround-debt.md`. Independently reproduce tests and inspect actual videos/screenshots. Report bone proxy results separately from tissue geometry. Missing calibrated axes, missing pad surfaces and 14 unweighted joints are known limitations, not a request to modify weights or synthesize skin. Do not equate `REFERENCE_HELD` or `PROXY_CONTACT` with tissue grasp PASS.

Codex does not claim Cursor approval. No Cursor execution/review interface was available in this session; this handoff is prepared for the assigned independent reviewer.
