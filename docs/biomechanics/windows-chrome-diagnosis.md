# Windows Chrome support discovery race

Frozen runtime/test base: PR6 fd1701f, retaining M2 0914d4f production code. Node24.14.0, installed Chrome155.0.8059.40, Windows11; browser GPU previously observed Radeon780M ANGLE D3D11. No runtime, production asset or original assertion was edited.

Original command `npx playwright test tests/browser/supports.spec.ts --reporter=line` passed 1/1 in9.9s. Original command with `--repeat-each=5` failed 1/5 at the original supports.spec.ts:8 assertion, exactly `Production scene missing`; 4 passed in33.8s. Original logs are under research/contact/chrome-original.log and chrome-repeat.log. The pre-existing failure log remains under research/opensim/results/logs/chrome-baseline.log. A later pass does not erase the failure.

Independent harness `research/contact/chrome-diagnostic.spec.ts` retains the original store/controls discovery predicate and records its immediate result after the original loading-text condition, then polls actual store+controls+SeatPad readiness. No fixed wait, skipped assertion or runtime workaround is introduced. First10 runs passed, with3 initially missing SeatPad. Next20 passed; **5/20 initially had no controls**, **18/20 initially lacked SeatPad**. Each subsequently observed the actual production support object, with no page errors. Raw observations and console logs are committed beside the harness.

Conclusion: original loading-text absence is an insufficient readiness barrier. The exact discovery predicate can run before controls exists, explaining the observed thrown error; even controls readiness alone can precede production solids. This is a reproducible test initialization race rather than evidence that production scene is permanently missing. No claim is made that these checks exclude unrelated future runtime regressions.

Minimal suggested Mac-owned test patch: replace the immediate discovery `page.evaluate` with bounded `expect.poll` of the same discovery routine; return false until a live store has controls and `scene.getObjectByName('SeatPad')`. Assign supportScene only once these conditions hold. Preserve every subsequent geometry/config/visibility assertion and fail with observed state on timeout. Keep the original test unchanged on this branch; this report and independent harness are the reviewable suggested correction. Do not add an arbitrary sleep or increase the test's unrelated per-pose wait.

```powershell
npx playwright test tests/browser/supports.spec.ts --repeat-each=5 --reporter=line
npx playwright test --config research/contact/playwright.config.ts --repeat-each=20 --reporter=line
```

Concurrent load from independent numeric experiments can change race frequency. The diagnosis therefore relies on observed missing controls followed by actual readiness, not a claimed deterministic failure rate or a timing threshold. Full-suite results are recorded separately in the stage report; isolated diagnostic passes do not substitute for the original suite.
