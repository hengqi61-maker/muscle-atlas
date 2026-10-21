import { build } from "esbuild";
import { spawnSync } from "node:child_process";
await build({
  entryPoints: ["scripts/grasp-v2/numeric.ts"],
  bundle: true,
  platform: "node",
  format: "esm",
  packages: "external",
  outfile: "artifacts/grasp-v2/numeric-run.mjs",
});
const r = spawnSync(process.execPath, ["artifacts/grasp-v2/numeric-run.mjs"], {
  stdio: "inherit",
});
process.exitCode = r.status ?? 1;
