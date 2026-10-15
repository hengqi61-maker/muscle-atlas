# Muscle Atlas
Local-first personal 3D training console. First engineering delivery, not a medical simulator.

## Start
Requires Node 22+.
```sh
npm ci
npm run dev
```
Open http://127.0.0.1:5173. `npm run build`, `npm test`, `npx playwright test` verify the application.

Real anatomy uses locally bundled upstream static meshes. Joint prototype is an explicitly labelled procedural model with elbow hierarchy motion, not skinned anatomical deformation. Switch model in the left panel; selecting exercise loads the joint prototype. Styles share geometry and IDs. Training records are entered by you and stored in IndexedDB; export JSON for backup. Browser data is tied to origin/profile; use stable port and export before clearing storage. Import restore and migrations beyond schema v1 are future work.

See docs/roadmap.md for verified status and docs/assets-and-licenses.md for third-party asset terms.
