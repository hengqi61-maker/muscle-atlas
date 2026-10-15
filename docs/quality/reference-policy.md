# Exercise reference policy

Reference authoring precedes implementation and final release review. Select the exercise variant and evidence before assessing the existing animation; do not infer a standard from convenient current poses.

## Reusable package

Each `docs/exercises/<exercise>/` package contains `reference.md` (variant, setup, phase narrative, exclusions and limits), `anatomy.md` (bilateral muscle roles/attachments), `kinematics.json` (coordinate convention, normalized phase targets, uncertainty), and `sources.json` (provenance). Reference authoring is not a PASS report for M2 or any other implementation. Final reviewers must freeze source SHA, model hash, animation version and machine config separately.

A source record must contain `id`, `title`, `authors`, `publisher`, `url`, `publicationDate` (null when unknown), `accessDate`, `license`, `evidenceType`, `variant`, `retrievalStatus`, `supports`, and `limitations`. Add retrieval URL, method, HTTP/content result, local capture hash and locator when available. Captures may remain local; a hash does not license redistribution. Do not invent author/date from domain identity or convert a search result title into verified full-text guidance.

## Evidence and confidence

Keep four claim classes separate: LITERATURE_SUPPORTED, VIDEO_OBSERVED, ANATOMY_DERIVED and UNCALIBRATED_ANIMATION_ASSUMPTION. Each claim needs source IDs, a precise source locator, scope, confidence and limitations. Confidence is categorical and explained; never a fabricated probability.

Retrieval states: `verified-full-text`, `verified-indexed-abstract`, `verified-indexed-metadata`, and `INCONCLUSIVE`. HTTP200 with CAPTCHA, login, challenge or empty application shell is INCONCLUSIVE. Index metadata verifies bibliographic identity, not methods/results. An abstract supports only what is actually present there. A review is not reclassified as a primary experiment. General arm elevation is not resisted pulldown motion capture. EMG does not measure a muscle's stimulus percentage or validate a displayed participation intensity.

Professional institutional guidance (prefer ACE/NASM or comparable exercise/clinical institutions) supports setup and observable movement cues; primary anatomy/biomechanics supports anatomy and bounded mechanisms. Seek independent corroboration and state conflicts. If preferred sites are inaccessible, preserve failed retrieval and compare credible alternatives without bypassing access controls. Do not call an unavailable source verified or treat a source-count target as a substitute for quality.

## Video and licensing

External exercise videos are link-only unless an explicit license permits download and redistribution. Record publisher, title, URL, date, access date, exact variant and timestamps when actually viewed. A page transcript is guidance evidence, not proof that its video was viewed or measured. Never label a prose-derived pose VIDEO_OBSERVED. Cite visible camera and occlusion limits; do not infer a hidden wrist, scapula or depth coordinate from one view. Keep video/model/image/text licenses distinct from repository source-code licensing. Never assume “free access,” PMC hosting, or a historical textbook license implies present redistribution rights.

## Threshold rules

A physiological angle/range/timing threshold requires a cited matching population/task and operational definition, or must be explicitly marked an uncalibrated authoring target with no physiological PASS authority. No universal 2:1 scapulohumeral rhythm, mandatory torso lean, fixed wrist tolerance, or forced chest contact is assumed. Digital numerical tolerances may test deterministic seek, transforms or continuity only; label them engineering checks and justify precision independently of human anatomy.

Report orientation and position separately. Use metres/degrees/seconds with explicit axis, handedness, local/world convention, scaling and sign. Five phase samples at 0/25/50/75/100 are minimum review views; continuous trajectories and more samples are needed to catch between-frame errors. Endpoints alone cannot prove smoothness. State whether equal phases are authored or measured. Muscle roles remain qualitative; plan and actual completion remain separate training entities.

## Completion and debt

Unverified evidence yields INCONCLUSIVE for the affected claim/gate. A provisional reference can be delivered with visible limitations; it cannot certify those gates. Network workaround debt follows project AGENTS.md and the global/project debt register. Record original failure, reproduction, alternative route, remaining cause and next action; conclude task-associated debt RESOLVED, DEFERRED or user-approved ACCEPTED_RISK. Reference authoring, runtime validation and final independent review have separate completion claims.
