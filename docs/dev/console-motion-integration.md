# Unified presentation in the original Muscle Atlas console

Branch `codex/console-motion-integration`, based on Phase2 after13ddb46 and preview limitation receipt. Presentation-only integration; no rig, weights, geometry, original hands, productionGLB or frozenR1 modifications.

The original `/` page remains the product entry: anatomy explorer, central rotatable/clickable human, exercise panel, local training journal and shared footer timeline. An explicit motion-version selector displays original equipment-linked clips, frozen shared-rig R1 clips, or rejected E03 as a local-only comparison. Changing version resets selection, hidden display state, playback and view. Diagnostic clips have no props/contact and are labeled accordingly; no equipment motion invented or uncalibrated linkage applied. E03 is never the default. Existing original-machine animation and props remain intact.

Experimental clips select CurlProbe/PulldownProbe by name and map the shared four-second timeline to actual clip duration. Source material roles/picking remain separate from geometry. Replay, pause, seek, speed and loop use the original store/player. Original left-arm-only angle/morph controls are shown only for original assets, never applied to shared rig. Bounds update uses actual skinned vertices for experimental poses. All source names/IDs are resolved from existing catalogue.

Research status, report links and actual native videos are available within an expandable panel rather than a separate required diagnostic page. Motion-quality FAIL remains explicit on unaccepted variants. The journal continues to save only explicit actual-completion records; no demonstration history/calendar was added. Calendar/plans/heatmap remain pending.

## Availability and scope

Start from this checkout with `npm run dev -- --host 127.0.0.1 --port 5173 --strictPort`. Frozen R1 is a tracked public experimental asset. E03 and its videos remain downloaded/generated local evidence under artifacts, **not production assets**. E03 option is disabled when HEAD does not return actual model/gltf-binary, preventing Vite SPA fallback HTML from being treated as a model. Local evidence is not copied into production dist or committed. Existing GitHub evidence links remain available when local media are absent. No main merge or anatomical release approval.

## Verification

Actual app build PASS (existing bundle-size warning), Vitest13/13, canonical asset reuse4/4. Real in-app browser observed original anatomy loading, sharedR1 both clip selection, E03 load with unaccepted label, live playback progression, pause and keyboard seek through end4.0s. Browser logs and integration screenshots recorded locally. Training form checked without saving fabricated records. These are frontend integration checks, not anatomy acceptance or a new121-frame asset review; unchanged diagnostic assets retain existing FAIL.

Separate prior diagnostic-page Vite module-loading debt remains DEFERRED; the normal product page works via its existing Vite entry. No network/security settings changed. No new workaround introduced for this integration.
