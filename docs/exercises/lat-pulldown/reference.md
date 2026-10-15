# Lat pulldown reference · authoring baseline

Status: **PROVISIONAL / INCONCLUSIVE for video calibration and attachment landmark calibration**, accessed 2026-10-15. This package defines a target independently of the current rig. It does not certify a rendered repetition, an implementation, or medical safety. See [source register](sources.json), [anatomy](anatomy.md), [kinematics](kinematics.json), and [reference policy](../../quality/reference-policy.md).

## Variant and scope

Seated, bilateral, front-of-head cable lat pulldown, straight bar, comfortable pronated grip, pull toward the upper chest, controlled return. The baseline excludes behind-neck, supinated, neutral-handle, unilateral, momentum-assisted, and standing variants. Grip width is a recorded subject/model parameter; “wider is better” is not an evidence-supported universal rule. Andersen et al. studied three pronated widths in 15 men; Lusk et al. compared width and forearm orientation in 12 healthy men. Their indexed abstracts support variant distinctions, not a universal joint-angle prescription or personalized training outcomes.

Evidence labels used throughout:

- **LITERATURE_SUPPORTED**: claim is bounded by the retrieved source's population, task and evidence level.
- **VIDEO_OBSERVED**: visible event measured in a named video with timestamps, camera and uncertainty. No such observations have yet been verified for this baseline.
- **ANATOMY_DERIVED**: qualitative consequence of attachments/actions; not direct measurement of this exercise.
- **UNCALIBRATED_ANIMATION_ASSUMPTION**: authoring choice awaiting matching video or motion data. It cannot become a pass threshold by repetition in code.

## Independent target sequence

The following five samples are normalized **authoring phases**, not measurements from video. Zero and 100 are the same returned top pose, not two different anatomical configurations. The equal split and smooth timing are UNCALIBRATED_ANIMATION_ASSUMPTION. Record actual video timing separately; neither the bottom nor reversal must occur at 50% in a real repetition.

| Phase | Event | Qualitative target | Evidence class / limit |
|---|---|---|---|
| 0% | Start/top | Seated pelvis supported; feet supported; thighs restrained by adjusted pad; bar overhead in front; arms raised; grip maintained. | Setup is provisional professional-guidance target; exact height, elbow extension and pad position uncalibrated. |
| 25% | Pull | Bar descends in front; elbows flex and move down; humeri lower relative to thorax. Trunk remains controlled. | Gross pull action anatomy-derived; precise bar path, scapular coupling and speed uncalibrated. |
| 50% | Bottom/reversal | Bar approaches upper chest without forcing head/neck forward or changing wrist shape to fake reach. Elbows are lower than at start. | Front variant literature-supported; exact chest contact and bottom angles uncalibrated, not mandatory universal anatomy. |
| 75% | Return | Elbows extend while arms elevate; controlled bar ascent, grip and support preserved. | Anatomy-derived direction; exact eccentric duration and coupling uncalibrated. |
| 100% | Returned top | Return to the same support/contact configuration as 0%; no teleport, dislocation or cable discontinuity. | Animation closure/continuity requirement, not measured physiology. |

## Segment and contact review

| Region | Review target | Do not infer |
|---|---|---|
| Grip / forearm | Both forearms pronated for this variant. Define palm normal, thumb side and local wrist axes per hand; compare bar contact at all five samples and between them. | “Palm faces forward” in screen coordinates is insufficient; camera, forearm rotation and handedness change appearance. A left mesh is not validated by mirroring the right transform. |
| Wrist / hand | Hand-to-bar orientation and position evaluated separately; wrist remains visually aligned with the forearm and grip does not slip. Preserve original source hand geometry. | A numerical IK target at the bar does not establish palm/finger contact; static source fingers are not evidence of an anatomical grip. No invented wrist angle tolerance. |
| Shoulder / scapula | Humeral lowering during pull and raising during return; scapular orientation is reviewed independently, with room for upward rotation/posterior tilt during elevation. | General arm-elevation evidence does not specify loaded pulldown scapular timing, fixed 2:1 rhythm, or mandatory maximal depression/retraction. |
| Torso / pelvis | Stable seat contact, controlled torso orientation and head clearance; any slight lean must be recorded as an authoring assumption until calibrated. | A specific lean angle, universal “perfect posture,” or repeated rocking derived from convenience of reaching the bar. |
| Seat / pad / legs | Seat supports pelvis, pad restrains thighs without deep penetration, feet have a plausible supporting surface, knees/hips fit the machine. | Machine dimensions are not human anthropometry; no fabricated participant height or leg lengths. |
| Elbows | Flex on pull, extend on return; preserve segment length and avoid abrupt rotation or apparent separation. | Fixed bone length alone does not prove correct joint placement, shoulder mechanics, or muscle deformation. |

## Qualitative participation map

Latissimus dorsi: principal shoulder adduction/extension contributor for this chosen task (ANATOMY_DERIVED; exercise studies provide bounded EMG evidence). Teres major: shoulder adduction/extension assistant (ANATOMY_DERIVED). Biceps brachii and brachialis: elbow-flexion contributors; brachioradialis contribution depends on forearm orientation (ANATOMY_DERIVED). Rotator cuff: humeral-head stabilization and rotation control; trapezius, serratus anterior and rhomboids: scapular positioning/control, with phase- and task-dependent roles (ANATOMY_DERIVED). These labels describe participation, not measured force, stimulus, recruitment rank, hypertrophy, injury risk, or EMG percentages. Do not label all cuff muscles prime movers simply because their meshes move.

## Verification status and next evidence

Verified retrieval: PubMed MEDLINE abstracts for Andersen 2014 and Lusk 2010; full PMC review Ludewig/Reynolds 2009 (retrieved by collaborating biomechanics author). Primary cuff-study metadata are separately registered at their actual evidence level. The primary studies and general scapular review do not replace verified professional exercise setup guidance or a viewed motion demonstration.

**Preferred institutional exercise guidance remains unverified.** ACE and NASM were searched/attempted; candidate official requests returned HTTP403, both web search transports failed, and generic search results did not establish the official titles/URLs. These are candidates, not verified references. Publication dates and individual authors remain null. NCBI Books returned a CAPTCHA page despite HTTP200. UAMS anatomy candidate failed certificate validation; TLS verification was preserved. Task-associated global network debt is coordinated by the main author under `WD-GLOBAL-2026-10-15-DOCS`.

Next: obtain accessible official ACE/NASM, Mayo Clinic or equivalent institutional exercise guidance with authors/title/date and an authorized front/side video. Link videos only unless an explicit redistribution license permits copying; no video was downloaded or redistributed here. Record timestamps for start/pull/bottom/return, camera, variant, bar/grip type and uncertainty. Resolve affected guidance/calibration gates before claiming the package is source-complete or using it to pass M2. Current model/rig corrections and release review are separate work.

## Resumed-source verification — 2026-10-15

The original web search/open path now returned both official pages; earlier failures remain recorded, with no demonstrated network root-cause repair. [Mayo Clinic](https://www.mayoclinic.org/healthy-lifestyle/fitness/multimedia/lat-pull-down/vid-20084683), dated2025-11-21, supports a seated anterior pull and controlled return; chest contact is not mandatory. Its transcript was read, not its moving video. [ACE](https://www.acefitness.org/resources/everyone/exercise-library/158/seated-lat-pulldown/) supports thigh restraint, controlled elbow lowering and a brief reversal before return. No page publication date was observed.

These are LITERATURE/INSTITUTIONAL-GUIDANCE observations, not measured video facts. The authoring target uses supported seating, a stable torso, an anterior bar path and a controlled return. ACE's scapular coaching cue must not become a rigid bone lock or fixed rhythm; general scapular research still limits such inference. Preserve both institutional variations on endpoint, rather than force chest contact or an unsupported medical angle. Video calibration and source attachment landmarks remain INCONCLUSIVE. The older access notes above describe the earlier attempt, not current page-text availability. No external footage, figures or transcript is redistributed.
