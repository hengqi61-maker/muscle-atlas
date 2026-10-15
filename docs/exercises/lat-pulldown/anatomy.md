# Anatomical attachment reference · bilateral rotator cuff

Status: anatomical authoring specification, **not a measured deformation model**. General cuff membership and scapula-to-humerus connection are verified against [OpenStax, Anatomy and Physiology 2e §11.5](https://openstax.org/books/anatomy-and-physiology-2e/pages/11-5-muscles-of-the-pectoral-girdle-and-upper-limbs) (Betts et al., 2022; accessed 2026-10-15). Its current page license is CC BY-NC-SA 4.0; no figures or textbook text are copied here. Detailed attachment regions below are conventional anatomical targets requiring a detailed accessible atlas or full primary anatomical paper before attachment-level signoff. PubMed metadata alone does not verify footprint geometry.

## Eight explicit attachment records

“Left” and “right” are the subject's sides. Every origin below belongs to the ipsilateral scapula and every insertion to the ipsilateral humerus. No cuff origin is a free point in world space or a thoracic anchor.

| Side | Muscle / stable logical key | Scapular origin region | Humeral insertion region | Verification level |
|---|---|---|---|---|
| Left | Supraspinatus / cuff.supraspinatus.L | Supraspinous fossa | Superior facet region of greater tubercle | General origin side verified; precise footprint pending |
| Right | Supraspinatus / cuff.supraspinatus.R | Supraspinous fossa | Superior facet region of greater tubercle | General origin side verified; precise footprint pending |
| Left | Infraspinatus / cuff.infraspinatus.L | Infraspinous fossa | Middle facet region of greater tubercle | General origin side verified; precise footprint pending |
| Right | Infraspinatus / cuff.infraspinatus.R | Infraspinous fossa | Middle facet region of greater tubercle | General origin side verified; precise footprint pending |
| Left | Teres minor / cuff.teresMinor.L | Posterior upper/lateral scapular border region | Inferior facet region of greater tubercle | Conventional anatomy target; region-specific verification pending |
| Right | Teres minor / cuff.teresMinor.R | Posterior upper/lateral scapular border region | Inferior facet region of greater tubercle | Conventional anatomy target; region-specific verification pending |
| Left | Subscapularis / cuff.subscapularis.L | Subscapular fossa on anterior/costal surface | Lesser tubercle region | Anterior scapular origin verified; precise footprint pending |
| Right | Subscapularis / cuff.subscapularis.R | Subscapular fossa on anterior/costal surface | Lesser tubercle region | Anterior scapular origin verified; precise footprint pending |

These region names are simplified atlas descriptions, not disjoint numerical tendon footprints. Mochizuki et al. (2008, PMID18451386) specifically investigates supraspinatus/infraspinatus insertion anatomy; only indexed metadata was retrieved here, so its results are not paraphrased as verified. Arai et al. (2008, PMID18760206) concerns subscapularis anatomy/clinical investigation with the same limitation. Teres major is not a rotator-cuff muscle. The four cuff tendons and their capsule relationships do not justify rigidly moving an entire muscle with the humerus.

## Attachment and deformation semantics

A future model attachment record needs `logicalKey`, `side`, `sourceMeshId`, `originBone`, `originRegion`, `originLocalCoordinates`, `insertionBone`, `insertionRegion`, `insertionLocalCoordinates`, `units`, `coordinateFrame`, `sourceIds`, `evidenceClass`, `confidence`, `verificationStatus`, and `limitations`. Local coordinates remain null until derived and checked on the licensed source anatomy. A region label is not an estimated vertex index. Preserve original source IDs; these logical keys do not assert a mapping to present mesh IDs.

As the scapula moves, its origin region moves with the scapula; as the humerus moves, insertion regions move with the humerus. A plausible implementation must preserve both relationships while allowing muscle/tendon shape change. This anatomy-derived constraint is not permission to invent attachment points, divide motion by a fixed ratio, or equate a static mesh, skin weights, and anatomically validated deformation.

## Coordinate and handedness safeguards

Use the canonical frame in `kinematics.json` and explicitly record the model-to-anatomy transform. Document anatomical anterior/posterior, superior/inferior and subject left/right before comparing any coordinates. A front-view image places subject left on the viewer's right. Mirroring one coordinate component changes handedness; a reflected basis cannot be applied as a proper rotation without correction. Local wrist axes, palm normals and thumb sides must be validated separately on the two original hands. Blender/R3F axis conversion, scene display scaling and camera transforms are implementation conversions, not anatomy.

All attachment metrics must use a common unscaled anatomical frame with stated units. Missing bone landmarks, ambiguous region boundaries or unknown source mesh identity produce INCONCLUSIVE, not a fabricated coordinate or automatic pass. This reference does not modify the rig, hand vertices, GLB or source mesh licenses.
