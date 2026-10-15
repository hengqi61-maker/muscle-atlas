# Independent exercise science review

Verdict: **INCONCLUSIVE** for M2 science/representative exercise fidelity. K08's narrow qualitative-highlight semantics are acceptable; this does not approve anatomy deformation, grip mechanics, or release.

Candidate: `baa407752cb46ac3b83f85b75262cebb08529e65`.
GLB SHA256: `44109e516dc44ee1767beec7a5cb61504c804c83b952fee92e9d1120c9021cea`.
Reviewer: independent exercise science reviewer; 2026-10-15.

## Inputs and checks actually performed

Read AGENTS.md; docs/quality/{motion-workflow,lat-pulldown-acceptance,reference-policy,blind-review}.md; docs/exercises/lat-pulldown/{reference,anatomy,biomechanical-notes}.md and {sources,kinematics}.json; src/data/{latPulldown,catalogue}.ts, mesh_mapping.json; role/material path in src/three/{Scene,materials}.tsx/ts and src/main.tsx. Checked HEAD against supplied candidate; inspected freeze.json, capture metadata and source-contact evidence structure. Recomputed role regex expansion from source mapping: 2 primary latissimus meshes; 8 secondary meshes (bilateral teres major, brachialis, both biceps heads); 8 stabilizer meshes (bilateral rhomboid major/minor and ascending/transverse trapezius); tendons excluded. This is a source-data audit, not an independent GPU picking test.

Viewed production captures frames/front/50.png, frames/back/0.png, frames/grip/50.png, frames-real/right-grip/0.png in this packet. Capture metadata identifies both styles and production rendering. Did not watch full-rep video, inspect every frame, rerun browser/tests/build, or read historical reviews/other reviewer conclusions. No external exercise video observed or downloaded. No prior memory consulted.

Independently opened the following current original pages using web tool on 2026-10-15:

- [Andersen et al. 2014 PubMed abstract](https://pubmed.ncbi.nlm.nih.gov/24662157/), abstract paragraphs (web lines 237–241): actual experiment in 15 men, three pronated widths, phase-specific EMG comparisons. Supports bounded variant distinctions, not a universal activation hierarchy or rendered motion validation. Full paper not inspected.
- [ACE Seated Lat Pulldown](https://www.acefitness.org/resources/everyone/exercise-library/158/seated-lat-pulldown/), Steps 1–4 (web lines 104–119): thigh restraint, controlled anterior pull/downward elbow movement and return. Its coaching scapular cue is not calibrated skeletal kinematics.
- [Mayo Clinic transcript](https://www.mayoclinic.org/healthy-lifestyle/fitness/multimedia/lat-pull-down/vid-20084683): official page/transcript retrieved; this is textual guidance and not observation of its moving video.

## Findings

### ES-01 — P1 evidence gap: representative shoulder/tissue motion cannot receive science signoff

Evidence: docs/exercises/lat-pulldown/reference.md:3, 13–17, 32–37, 49, 55; kinematics.json `currentUncalibratedAssumptions` and `nextEvidenceNeeded`; anatomy.md attachment verification table. External multi-view video calibration and detailed source attachment landmarks remain absent. The source package explicitly distinguishes general elevation research from loaded pulldown trajectories and records null calibrated joint/tissue precision. The 4-second equal-phase timing, scapular constants and tissue behavior are authored assumptions. No count of frames, source URLs, stable bone lengths, or grip-marker agreement fills this gap.

Expected: documented matching-variant observations with timestamps/cameras/uncertainty plus reviewed attachment/local-frame evidence before high-fidelity or anatomical-deformation claims. Actual: supported qualitative setup, explicit uncertainty, and representative digital motion, without that calibration. Confidence high in the evidence gap; no claim that one numerical human trajectory is universally required. K04/K07 fidelity remains INCONCLUSIVE in this domain. Repair/verification: supply bounded variant-matched evidence and independently compare actual mesh movement; preserve current uncertainty labels meanwhile.

### ES-02 — P2: reference participation scope exceeds the runtime subset without explicit omission semantics

Evidence: src/data/latPulldown.ts:4–13 versus reference.md:39–41. Runtime highlights omit cuff, serratus anterior and brachioradialis despite reference discussion. Existing mapped roles are anatomically plausible qualitative summaries. A static 'stabilizer' label for scapular positioning/control must not mean immobility, no force, or only isometric contraction. Runtime main.tsx:25 correctly says amplitude does not determine force and color is not instantaneous activation/training volume.

Expected: tell users the map is a selected subset and uncolored does not mean uninvolved, or provide reviewed source-ID relations for further muscles. Actual: a subset with no explicit uncolored-muscle explanation in the inspected callout. Confidence high in omission, moderate in user interpretation. This is not proof that omitted muscles must be assigned one universal role or that every participating muscle must be highlighted. Verify by matching an explicit coverage statement or traceable expanded map to bilateral source IDs.

### ES-03 — P2: participation claim traceability is less precise than cuff attachment traceability

Evidence: reference.md:41 gives a useful bounded participation narrative; anatomy.md concentrates on eight cuff attachment records. Role data src/data/latPulldown.ts:4–13 has no per-relation source locator/confidence/evidence-class record. sources.json identifies retrieved sources and limitations but does not make the role-to-source connection machine-explicit. Primary/secondary labels should remain ANATOMY_DERIVED authoring summaries; EMG abstracts cannot alone establish force contribution or recruitment rank. Add a small role/source/locator/confidence table and state these labels are non-exhaustive. No fabricated percentage or direct EMG measurement was found.

### ES-04 — original-hand limitation, cross-domain observation

Evidence: frames/grip/50.png and frames-real/right-grip/0.png show preserved open source anatomical digit structures near the handle, without an encircling closed-finger grasp. Original geometry identity and an IK contact target cannot certify functional grip, forearm pronation, or loading. Reference.md:33 explicitly acknowledges this distinction; runtime footer main.tsx:26 still says '双手握杆'. This review does not assign an independent geometric collision severity from four stills; K02/contact verdict belongs to full visual/biomechanics evidence. Do not repair this by procedural skin or folded original vertices without explicit user authorization. Present the retained-hand approximation plainly and validate actual source surfaces/orientation separately.

## Bounded positive conclusions

K08: source originalName is retained in catalogue, bilateral role expansion is traceable to anatomy IDs, tendon records are excluded, and role/material resolution is separate from skeleton animation. Highlights are static qualitative roles, not time-varying EMG, force, stimulus percentages, hypertrophy predictions or training completion. The UI makes that distinction and declares shoulder/tissue motion uncalibrated. The chosen anterior seated variant and controlled return have independent professional guidance; no requirement to force chest contact or fixed scapulohumeral ratio is justified. General source-hand preservation is compatible with identity protection and does not prove an actual grip.

## Completion and limits

Completed: independent read-only science review and current source-page verification; only this own review artifact written. No product acceptance, release approval, merge, clinical validation, or claim of full functional correctness.

Workarounds introduced: none. Permanently resolved debt: none. Deferred/accepted debt: none created by this review; existing historical debt not inspected to preserve independence. Remaining evidence: variant-matched observed motion, calibrated skeletal/attachment frames, actual contact and full tissue review; explicit highlight coverage/claim locators. No verified P0 science defect identified. Overall INCONCLUSIVE reflects missing fidelity evidence, not a claim that qualitative participation highlighting is invalid.
