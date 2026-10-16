# Independent actual-GLB numerical screen

Reproduce: `node scripts/quality/rig-v2-audit.mjs` (expected exit 1 for current candidate); calibration: `node --test tests/rig-v2/quality.node.mjs`.

The report hashes the actual candidate GLB, original source GLB, and linked independent full native base-geometry proof. It checks exported source IDs and source-name correspondence independently from the attachment registry. It samples actual skin/morph-evaluated mesh vertices and triangle edges at 121 poses in each authoring clip, with denser sampling for shoulder/cuff/axilla/elbow muscles.

Current result: AUTOFAIL. PulldownProbe exceeds the declared gross edge-elongation screen at every sampled pose (peak 3.98844 times rest edge length). CurlProbe has no sampled numerical violation; this is not anatomical or release approval. Finite sampling cannot establish absence of unsampled defects. Segment length, orientation, continuity measurements and deformation screens do not establish anatomical calibration, collision freedom or acceptable exercise motion. All anatomical attachment proxies remain INCONCLUSIVE. Native CurlProbe/PulldownProbe are authoring test poses only.

No workaround or model edit was introduced. This evidence author does not approve final release.
