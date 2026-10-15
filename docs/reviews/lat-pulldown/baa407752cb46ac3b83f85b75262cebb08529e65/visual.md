# Independent visual review

Candidate: `baa407752cb46ac3b83f85b75262cebb08529e65`  
GLB SHA256: `44109e516dc44ee1767beec7a5cb61504c804c83b952fee92e9d1120c9021cea`  
Verdict: **INCONCLUSIVE — visual gate cannot PASS; P1 evidence/representation blockers below.** Owner approval remains pending.

Read-only review of production captures. No historical defect reports or other reviewer conclusions read. No production/asset changes. Contract: AGENTS.md, docs/quality/motion-workflow.md, docs/quality/lat-pulldown-acceptance.md.

## Evidence actually viewed

Viewed full-resolution PNGs with view_image: clean grip 0/50, right-grip 50, back 0/50, side 50/100, front 25; real grip 0/25/50, right-grip 75, back 25/50, side 0, front 50. Also viewed recorded-video contact sheet and full-size video-frames/frame-02.png (4 s), frame-04.png (12 s), frame-08.png (28 s). Source is full-rep.webm; metadata and video-timeline.json read. This is actual frame inspection, not uninterrupted video playback. Four-second video sampling aliases the four-second exercise cycle, so those samples do not establish temporal smoothness. Deterministic 0/25/50/75/100 images cover the pose phases; only listed images were personally viewed.

Read source-contacts.json method/topology excerpt and motion-quality/motion-quality.json rules as supporting diagnostics, not proof of visual correctness. Original source hand topology preservation is supported by the former; no procedural skin hand was observed.

## Findings

### VR-01 — P1 — grasp is not visually established (K02/V01)

Evidence: frames/grip/0.png and 50.png; frames/right-grip/50.png; frames-real/grip/0.png, 25.png, 50.png; frames-real/right-grip/75.png; frames-real/front/50.png. Mesh region: original bilateral hand/digit/palm bundles, exact individual source IDs not visually labelled. Confidence: high in visible open/draped appearance, moderate in grasp interpretation, low in exact palm-normal/thumb orientation.

The hand structures remain elongated/open beside and over the black handles. Several thin digit/tendon structures project below the handles in front view. Opposed thumb placement and fingers wrapping around the handle cannot be traced from these views; handle occlusion hides the contact surface. Apparent positional overlap is not a demonstrated load-bearing grasp. I cannot verify reversed palms, dislocation, or total contact loss and do not assign a P0 for those claims.

Reproduce: frozen production build, pulldown, seek 0/1/2/3 s, use both hand camera presets and both styles. Required verification: labelled original thenar/hypothenar/thumb landmarks plus underside and dorsal close-ups showing actual surface contact/orientation throughout the repetition. Preserve original hand vertices; do not fix this by silently introducing a procedural hand or folding source geometry. If the source cannot represent grasp under that constraint, declare that limitation and obtain an owner scope decision. K02 remains INCONCLUSIVE.

### VR-02 — P1 — visible strand/attachment continuity requires attribution (K07/V01)

Evidence: frames/grip/0.png (screen-right inner arm/axillary region, approximately x635–746/y518–662), frames/grip/50.png (x632–751/y510–653), frames-real/grip/0.png and 50.png, mirrored strands in frames/right-grip/50.png. Mesh region: medial upper-arm/axillary/chest-adjacent bundles; exact source IDs unconfirmed. Confidence: high in visible long separated strips and background gaps; low in anatomical identity and whether this is source geometry, rigging or intentional open anatomy.

Long narrow tissue strips run through open background space between torso/axilla and raised or lowered arm. This prevents a confident continuity assessment at the anatomical shoulder/arm boundary. A skinless source legitimately has separate muscles and tendons; separation alone does not prove tearing, floating origin/insertion, or wrong deformation. Consequently this is a must-resolve attribution/evidence blocker, not a verified torn-muscle assertion.

Required verification: same-view source-rest versus rigged comparison, mesh-isolated ID-labelled capture and attachment landmarks for these strips, plus dense motion sampling. If source-rest has the same exposed anatomy and correct attachments, document it and re-review; if rig-induced, repair the bindings and repeat the exact captures.

### VR-03 — P2 — current framing limits visual checks

Evidence: frames/front/25.png and frames-real/front/50.png cut off feet; back frames show a small body and intentionally hidden machine; recorded grip frame-08 at 28 s loses the near hand behind the bottom playback panel. Confidence: high. The deterministic tracked grip images and side view help, but a full-rep hand recording that tracks the moving hands and a closer back/scapular capture would make the evidence reviewable across all phases. Do not infer missing geometry correctness from this recording.

## Other observations and limits

Side 0/50/100 samples show seated pelvis and feet positioned plausibly at the seat/platform at screenshot resolution; no obvious gross seat/platform penetration or hovering was verified. Thigh-pad contact is partly occluded, so absence of persistent collision is not established. Back 0/25/50 shows bilateral raised-to-lowered arm motion and retained highlighted lat/trapezius regions; the small camera scale does not establish valid scapular mechanics. No source-ID swapping is visually apparent. No obvious bar/hand positional divergence was verified in the inspected samples; this is not a numerical or orientation PASS.

The supplied surface diagnostic reports severe-collapse source IDs left/right palmaris longus. That requires the software/biomechanics reviewers' geometric analysis; I cannot identify those meshes from these unlabelled RGB screenshots and do not independently confirm an exact collapse location here.

## Completion and debt accounting

Completed: independent review of actual both-style keyframes and recorded-video frames; report written only here. Workarounds introduced to production: none. Permanently resolved debt: none. Deferred/accepted production debt: none approved by this reviewer. An inline image-pipe display attempt was unreadable; parent supplied ordinary extracted video frames, which were actually inspected. Remaining evidence: palm/thumb/underside views, labelled axillary strip source-rest comparison, clearer moving-hand/back recording and dense temporal inspection. **No visual PASS and no milestone approval.**
