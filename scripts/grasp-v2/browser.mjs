import { chromium } from "@playwright/test";
import fs from "node:fs";
const out = "artifacts/grasp-v2/browser";
fs.mkdirSync(out, { recursive: true });
const browser = await chromium.launch({ channel: "chrome", headless: true }),
  context = await browser.newContext({
    viewport: { width: 1600, height: 1100 },
    recordVideo: { dir: out, size: { width: 1600, height: 1100 } },
  }),
  page = await context.newPage();
const errors = [];
page.on("pageerror", (e) => errors.push(String(e)));
await page.goto("http://127.0.0.1:5186/");
await page.getByText("Grasp Controller v2 · 实验", { exact: true }).click();
await page.getByRole("checkbox", { name: "启用抓握 v2" }).check();
await page
  .getByTestId("grasp-report")
  .filter({ hasText: "GEOMETRY_INSUFFICIENT" })
  .waitFor({ timeout: 60000 });
await page.screenshot({ path: out + "/front.png" });
console.log(await page.getByTestId("grasp-report").innerText());
fs.writeFileSync(
  out + "/initial.json",
  await page.getByTestId("grasp-report").innerText(),
);
await page.getByLabel("抓握器械").selectOption("dumbbell");
await page.getByRole("checkbox", { name: "自动抓握" }).check();
await page.waitForTimeout(1500);
await page.getByRole("button", { name: "手部特写", exact: true }).click();
await page.waitForTimeout(200);
await page.screenshot({ path: out + "/hand.png" });
await page.getByRole("button", { name: "侧面", exact: true }).click();
await page.screenshot({ path: out + "/side.png" });
const report = await page.getByTestId("grasp-report").innerText();
fs.writeFileSync(
  out + "/report.json",
  JSON.stringify(
    { browser: browser.version(), errors, report: JSON.parse(report) },
    null,
    2,
  ),
);
const video = page.video();
await context.close();
await browser.close();
console.log("video", await video.path());
if (errors.length) throw Error(errors.join("\n"));
