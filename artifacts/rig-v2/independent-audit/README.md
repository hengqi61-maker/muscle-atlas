# Independent actual-GLB numerical screen

Reproduce: `node scripts/quality/rig-v2-audit.mjs` (expected exit 1 for current candidate); calibration: `node --test tests/rig-v2/quality.node.mjs`.

The report hashes the actual candidate GLB, original source GLB, and linked independent full native base-geometry proof. It checks exported source IDs and source-name correspondence independently from the attachment registry. It samples actual skin/morph-evaluated mesh vertices and triangle edges at 121 poses in each authoring clip, with denser sampling for shoulder/cuff/axilla/elbow muscles.

Current result: AUTOFAIL. PulldownProbe exceeds the declared gross edge-elongation screen at every sampled pose (peak 3.98844 times rest edge length). CurlProbe has no sampled numerical violation; this is not anatomical or release approval. Finite sampling cannot establish absence of unsampled defects. Segment length, orientation, continuity measurements and deformation screens do not establish anatomical calibration, collision freedom or acceptable exercise motion. All anatomical attachment proxies remain INCONCLUSIVE. Native CurlProbe/PulldownProbe are authoring test poses only.

No workaround or model edit was introduced. This evidence author does not approve final release.

The unchanged M2 area-ratio screen (<0.05, severe if count >3 OR >1% of eligible triangles per mesh) is also evaluated separately from the near-zero <0.0001 screen. Across all poses, Curl has 110 triangle-pose <0.05 observations (maximum 8 per pose across meshes), with no per-mesh severe alarm. Pulldown has 1084 (maximum 32 per pose), with severe per-mesh alarms in 42 poses. Frame 0 includes left/right supraspinatus, 5/878 each, source IDs FMA32545/BP8376 and FMA32544/BP4791; the absolute-count arm of the unchanged OR rule triggers. Near-zero counts are zero for both probes. These are engineering deformation alarms, not medical findings. Full pose/source-ID details are in report.json. Calibration includes both absolute-only 4/4000 and fraction-only 1/20 cases; 5/5 tests pass.
