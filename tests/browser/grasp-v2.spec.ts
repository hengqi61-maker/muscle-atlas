import { test, expect } from "@playwright/test";
test.use({ video: "on" });
const rigSnapshot = async (page: any) =>
  page.evaluate(async () => {
    const path = "/src/grasp-v2/runtime.ts";
    const { activeRuntime: r } = await import(path);
    if (!r) throw Error("No live v2 rig");
    return Object.fromEntries(
      ["Left", "Right"].map((side) => [
        side,
        {
          q: r.rigs[side].joints.map((j: any) => j.bone.quaternion.toArray()),
          world: r.rigs[side].joints.map((j: any) =>
            j.bone.matrixWorld.toArray(),
          ),
          reference: r.rigs[side].joints.map((j: any) => j.reference.toArray()),
        },
      ]),
    );
  });
const settle = async (page: any) =>
  expect
    .poll(
      () =>
        page.evaluate(async () => {
          const path = "/src/grasp-v2/runtime.ts";
          const { activeRuntime: r } = await import(path);
          return (
            !!r && !Object.values(r.layers).some((l: any) => l.transitioning)
          );
        }),
      { timeout: 15000 },
    )
    .toBe(true);
test("v2 real main-page controls, two hands, moving geometry, seek and original scene regression", async ({
  page,
}) => {
  test.setTimeout(120000);
  const errors: string[] = [];
  page.on("pageerror", (e) => errors.push(e.message));
  await page.goto("/");
  await page.getByText("Grasp Controller v2 · 实验", { exact: true }).click();
  await page.getByLabel("启用抓握 v2").check();
  await expect(page.getByTestId("grasp-report")).toContainText(
    "GEOMETRY_INSUFFICIENT",
    { timeout: 60000 },
  );
  expect(await page.locator("canvas").count()).toBe(1);
  const slider = page.getByLabel("动画进度");
  const start = await rigSnapshot(page);
  await page.getByRole("button", { name: "张开", exact: true }).click();
  await settle(page);
  const open = await rigSnapshot(page);
  await page.getByRole("button", { name: "闭合", exact: true }).click();
  await settle(page);
  const closed = await rigSnapshot(page);
  expect(closed.Left.q).not.toEqual(open.Left.q);
  expect(closed.Right.q).toEqual(open.Right.q);
  await page.getByLabel("抓握侧").selectOption("Right");
  await page.getByRole("button", { name: "张开", exact: true }).click();
  await settle(page);
  const right = await rigSnapshot(page);
  expect(right.Left.q).toEqual(closed.Left.q);
  expect(right.Right.q).not.toEqual(closed.Right.q);
  await page.getByText("每根手指高级控制", { exact: true }).click();
  await page.getByLabel("Right Index", { exact: true }).fill("0.72");
  await settle(page);
  const individual = await rigSnapshot(page);
  expect(individual.Right.q[3]).not.toEqual(right.Right.q[3]);
  expect(individual.Right.q[6]).toEqual(right.Right.q[6]);
  await page.getByLabel("拇指对握", { exact: true }).fill("0.5");
  await page.getByLabel("抓握器械").selectOption("dumbbell");
  await page.getByLabel("自动抓握", { exact: true }).check();
  await page.getByLabel("握柄半径").fill("0.016");
  await page.getByLabel("保持器械参考").check();
  await page.getByLabel("握柄移动").fill("0.018");
  await settle(page);
  await expect(page.getByTestId("grasp-report")).toContainText("residualM");
  for (const time of [0, 2, 4, 1, 0]) {
    await slider.fill(String(time));
    await page.waitForTimeout(200);
    const snap = await rigSnapshot(page);
    expect(snap.Left.q.flat().every(Number.isFinite)).toBe(true);
  }
  await page.getByRole("button", { name: "手部特写", exact: true }).click();
  await page.screenshot({ path: "artifacts/grasp-v2/browser/hand-final.png" });
  await page.getByRole("button", { name: "侧面", exact: true }).click();
  await page.screenshot({ path: "artifacts/grasp-v2/browser/side-final.png" });
  await page.getByRole("button", { name: "正面", exact: true }).click();
  await page.screenshot({ path: "artifacts/grasp-v2/browser/front-final.png" });
  await page.getByRole("button", { name: "▶", exact: true }).click();
  await page.waitForTimeout(350);
  await page.getByRole("button", { name: "Ⅱ", exact: true }).click();
  const frozen = await slider.inputValue();
  await page.waitForTimeout(150);
  await expect(slider).toHaveValue(frozen);
  await slider.fill("3.98");
  await page.getByRole("button", { name: "▶", exact: true }).click();
  await expect
    .poll(async () => Number(await slider.inputValue()))
    .toBeLessThan(3);
  await page.getByRole("button", { name: "Ⅱ", exact: true }).click();
  await page.getByRole("button", { name: "释放", exact: true }).click();
  await page.getByRole("button", { name: "重置抓握", exact: true }).click();
  await page.getByRole("button", { name: "高位下拉", exact: true }).click();
  await expect(
    page.getByText("SEATED LAT PULLDOWN · UNVERIFIED"),
  ).toBeVisible();
  await expect(page.getByLabel("启用抓握 v2")).not.toBeChecked();
  await page.getByRole("button", { name: "哑铃弯举", exact: true }).click();
  await expect(
    page.getByRole("button", { name: "90°", exact: true }),
  ).toBeVisible();
  expect(errors).toEqual([]);
  expect(start.Left.q).toHaveLength(15);
});
