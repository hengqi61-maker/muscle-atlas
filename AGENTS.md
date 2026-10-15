# Muscle Atlas engineering rules
Local-first personal macOS application. No registration, billing, server requirement or fabricated training history.
Use React/TypeScript/R3F; keep anatomy IDs, material states, motion and training data separate.
Plan and actual completion are different entities. Participation roles are qualitative, never invented stimulus percentages.
Keep sourced model provenance, version and license separate from source-code licensing. Never equate static meshes with skinning or anatomical deformation.
Label procedural prototype clearly. Do not silently replace failed model loading with it.
Run build, unit tests and real browser checks before claims of working functionality; update docs/roadmap.md.
Record workarounds immediately in .codex/workaround-debt.md. Apply user recurring-failure policy: compare durable routes, verify original path, end task debt RESOLVED, DEFERRED or user-approved ACCEPTED_RISK.
OAuth, paid assets and destructive operations require user authorization. Calendar writes only to managed or explicitly linked events.

Use the original source anatomical hand meshes in motion scenes. The user rejected procedural hands and skin surfaces; do not reintroduce them or fold source hand vertices without an explicit request. Preserve the upgraded dumbbell and pulldown linkage.

## Motion quality pilot (milestone-controlled)
For any new exercise animation, IK/rig, skeletal muscle deformation, equipment-grip change, or claimed muscle role, follow `docs/quality/motion-workflow.md` and the applicable exercise contract (first: `docs/quality/lat-pulldown-acceptance.md`).
When the user requests milestone review, the orchestrator should delegate **independent** reviews to `biomechanics_reviewer`, `visual_reviewer`, `exercise_science_reviewer`, and `software_qa_reviewer` using a frozen candidate commit and the same evidence bundle. Reviewers do not edit the implementation; their instructions are behavioral, not a sandbox boundary. No visual PASS without real frames, no kinematics PASS based on grip position alone.
Implementation agent may fix defects on a work branch and rerun validation, but cannot mark a milestone approved or merge it without the user's explicit review of actual footage and unresolved limitations. If custom subagent spawning is unavailable, perform separate sequential review sessions; record this limitation rather than pretend independent agents ran.
CI passing proves build/unit test status only. Require separately recorded browser/GPU and motion-domain review evidence before high-fidelity animation claims.
