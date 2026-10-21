import fs from "node:fs";
import Ajv from "ajv/dist/2020.js";
import { build } from "esbuild";
import { execFileSync } from "node:child_process";
await build({
  entryPoints: ["scripts/grasp-v2/export-contact.ts"],
  bundle: true,
  platform: "node",
  format: "esm",
  packages: "external",
  outfile: "artifacts/grasp-v2/contact-run.mjs",
});
execFileSync(process.execPath, ["artifacts/grasp-v2/contact-run.mjs"], {
  stdio: "inherit",
});
const ajv = new Ajv(),
  validate = ajv.compile(
    JSON.parse(fs.readFileSync("schemas/contact/packet-v1.1.schema.json")),
  ),
  valid = validate(
    JSON.parse(fs.readFileSync("artifacts/grasp-v2/contact-v1.1.json")),
  );
fs.writeFileSync(
  "artifacts/grasp-v2/contact-schema.json",
  JSON.stringify(
    {
      status: valid ? "PASS" : "FAIL",
      upstream: "a8247a4ff121c94b038ceccb77f729d30a85073c",
      errors: validate.errors,
    },
    null,
    2,
  ),
);
if (!valid) throw Error(JSON.stringify(validate.errors));
console.log("Windows v1.1 schema PASS");
