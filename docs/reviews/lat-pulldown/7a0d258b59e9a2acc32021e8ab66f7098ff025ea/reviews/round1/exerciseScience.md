# Independent exercise-science review — FIRST REPORT FROZEN

Candidate: `7a0d258b59e9a2acc32021e8ab66f7098ff025ea`. GLB SHA256 independently checked: `56b3ca231dda14100d64233758da2116282547b472afd4fc9b24160f345fee05`.
Workspace: `/Users/qi-heng/Documents/ChatGPT/muscle-atlas-baseline-7a0d258`.

## Independence and scope
Read only runtime `src/` and the new candidate packet/protocol. No historical reviews, README, debt, other worktrees, or other reviewers’ conclusions viewed. This report freezes before historical comparison. Only this report file was written. No EMG, force, stimulus percentage, or hypertrophy conclusion is inferred from color, mesh motion, or joint trajectories.

## Verdict by scope
- **K08 qualitative color semantics: PASS (high confidence)**. `src/data/latPulldown.ts:3–14`, `src/three/Scene.tsx:19–23,40–46`, `src/three/materials.ts:2–7` trace original names to source anatomy IDs and fixed role colors. Tendons excluded. Main UI `src/main.tsx:23–24` explicitly calls colors participation roles, says they are not instant activation/training volume, and distinguishes blue selection. Actual front/back frames agree with green lats, amber upper-arm contributors and purple scapular-control regions in both styles. No fabricated intensity value is displayed in inspected pulldown frames.
- **K08 exact scientific classification: PASS as a limited representative map, with P2 documentation gaps (moderate confidence)**. Latissimus primary and teres major/biceps/brachialis assistance are reasonable. Rhomboid and middle/lower trapezius as “stability and control” is defensible as broad control terminology; it must not mean they remain isometric or never contribute scapular motion. The UI explicitly says motion amplitude cannot determine force. Neither coaching guidance nor the cited EMG study establishes an exclusive three-bin taxonomy for every source submesh.
- **Written exercise advice: PASS (high confidence)**. `latPulldown.ts:18–19` specifies thigh fixation, upper-chest anterior pull, elbows down, controlled return and avoiding major trunk momentum. This agrees with ACE and NASM institutional coaching guidance. “Avoid obvious backward lean” is reasonably read as avoiding excessive lean, not prohibiting all slight stable lean. Behind-neck entry is an error for this front-pulldown variant; it is not presented here as a universal clinical contraindication.
- **Rendered exercise variant: PASS only for seated bilateral anterior-to-upper-chest intent (moderate confidence)**. Inspected top and bottom front frames plus bottom side show that broad variant. **INCONCLUSIVE for a valid full-repetition demonstration, grip closure, ROM, scapulohumeral mechanics, loading, and temporal control**. These require the complete video and dedicated biomechanical/visual review. The inspected grip frame shows extended source finger geometry rather than an unambiguously closed grip; this is an observation referred to K02 review, not evidence of muscle recruitment or a new science diagnosis.
- **Overall science gate: PASS for K08 qualitative labeling and advice; INCONCLUSIVE for full motion-technique endorsement.** This is not medical validation or full milestone acceptance.

## Actual visual evidence inspected
Packet prefix: `artifacts/blind-review/7a0d258b59e9a2acc32021e8ab66f7098ff025ea/`.
Individually viewed `frames/front/0.png`, `frames/front/50.png`, `frames/side/50.png`, `frames/back/50.png`, `frames/grip/50.png`, and `frames-real/back/50.png`. Labels report 0/4 and 2/4 seconds. I have not watched the full video and do not claim to have inspected the remaining frames. Bottom chest bar location and qualitative colors are visibly supported; continuous tempo and exact grip mechanics are not certified.

## Exact role IDs
All below are derived using the production catalogue sanitizer (`src/data/catalogue.ts:4`) from original names, not approximate display groups.

Primary:
- `z-anatomy:unmapped:left_latissimus_dorsi`
- `z-anatomy:unmapped:right_latissimus_dorsi`

Secondary:
- `bp3d:BP8287:left_teres_major`, `bp3d:BP4789:right_teres_major`
- `bp3d:BP8684:left_brachialis`, `bp3d:BP4807:right_brachialis`
- `bp3d:BP8816:long_head_of_left_biceps_brachii`, `bp3d:BP5566:long_head_of_right_biceps_brachii`
- `bp3d:BP9153:short_head_of_left_biceps_brachii`, `bp3d:BP5558:short_head_of_right_biceps_brachii`

Stability/control:
- `bp3d:BP8225:ascending_part_of_left_trapezius`, `bp3d:BP5638:ascending_part_of_right_trapezius`
- `bp3d:BP8252:transverse_part_of_left_trapezius`, `bp3d:BP5610:transverse_part_of_right_trapezius`
- `bp3d:BP9245:left_rhomboid_major`, `bp3d:BP4780:right_rhomboid_major`
- `bp3d:BP8585:left_rhomboid_minor`, `bp3d:BP4784:right_rhomboid_minor`

The lats’ original-name/source identity remains traceable, but `unmapped` honestly reflects empty FMA/BP fields (`mesh_mapping.json:3211–3224`), not an independently verified anatomical ontology identifier.

## Findings
No science-scope P0 or P1 established by the inspected evidence.

**P2 SCI-01 — map coverage and evidence rationale are undocumented.** `latPulldown.ts:4–8` omits the existing elbow-flexor meshes `bp3d:BP8244:left_brachioradialis` and `bp3d:BP4833:right_brachioradialis` (`mesh_mapping.json:491–496,1795–1800`). NASM identifies brachioradialis assistance; the runtime map is visibly selective. Reproduce by matching these original names against the pulldown regex: no role is returned; Scene leaves their default material. Expected: either explicitly describe the map as selected representative contributors or document/add the intended contributor coverage after review. This is not a proved false role because the UI never promises an exhaustive list. Confidence: high for omission, moderate for educational impact.

**P2 SCI-02 — source provenance of roles is absent from runtime data.** `latPulldown.ts:3` says source-verified IDs; its map contains no role evidence or variant-specific rationale. The exact middle/lower trapezius and rhomboid source subdivisions are assigned one broad control bin without distinguishing dynamic scapular contribution. Reproduce: inspect map and UI source text; there are no citations or confidence metadata. Expected: retain qualitative caveat and attach references/rationale for these selected classifications, acknowledging overlapping roles. Confidence: high for missing documentation; no claim that a different exclusive bin is scientifically proven.

## References browsed during this review
1. American Council on Exercise. **Seated Lat Pulldown**, Exercise Library, undated; accessed live in this review. https://www.acefitness.org/resources/everyone/exercise-library/158/seated-lat-pulldown/ . Primary institutional instruction: fixed thighs, stable slight lean, anterior chest-directed pull, elbow-down cue and controlled return. Coaching consensus guidance, not an experimental force model.
2. Brian Sutton / NASM. **The Biomechanics of the Lat Pulldown: Muscles, Grips, and Form**, published 2021; live page states updated July 21, 2026. https://www.nasm.org/resource-center/blog/training/the-biomechanics-of-the-lat-pulldown-muscles-grip-and-form . Primary institutional coaching source: lats primary; elbow flexor assistance and scapular control contributors; stable torso and upper-chest path. This broad guidance does not validate exact submesh bins or individual anatomy.
3. Lusk SJ, Hale BD, Russell DM. **Grip width and forearm orientation effects on muscle activity during the lat pull-down**. *Journal of Strength and Conditioning Research* 2010;24(7):1895–1900. DOI 10.1519/JSC.0b013e3181ddb0ab. https://pubmed.ncbi.nlm.nih.gov/20543740/ . Primary experimental abstract retrieved in live search: 12 healthy men, anterior pulldown, surface EMG of latissimus, middle trapezius, biceps under specified grips/load. It supports participation of those measured structures and variant specificity; it does not validate this animation or justify force/size/intensity rankings from its colors.

A fetched NSCA PTQ PDF returned HTTP 403; it was not used as evidentiary support. The initial direct PubMed page returned only its disclosure shell; the live search result subsequently exposed the primary abstract. No full-text access or hidden unavailable evidence is assumed. At least two independent institutional primary coaching sources and one primary experiment were actually available.

## Completion, workarounds, debt, remaining evidence
Primary review completed and frozen with the limited verdicts above. No runtime workaround or code/assets change introduced; no project fix or permanently resolved debt claimed. No debt was accepted on the owner’s behalf. The unavailable PDF is explicitly excluded, not silently substituted for a required source. Remaining evidence: full-repetition video and biomechanics/visual judgments for K02–K07; documented rationale for selective map coverage and source subdivisions. No historical comparison performed.
