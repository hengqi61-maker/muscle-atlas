import {chromium} from 'playwright';
import {writeFileSync} from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const out = path.join(root, 'artifacts/grasp-v1/g2');
const url = process.env.GRASP_PANEL_URL || 'http://127.0.0.1:8766/src/grasp-v1/panel.html';

const browser = await chromium.launch({headless: true, channel: 'chrome'});
const page = await browser.newPage({viewport: {width: 1280, height: 800}});
const errors = [];
page.on('pageerror', (e) => errors.push(String(e)));
page.on('console', (m) => { if (m.type() === 'error' && !/favicon|File not found/i.test(m.text())) errors.push(m.text()); });
await page.goto(url, {waitUntil: 'networkidle', timeout: 60000});
await page.waitForFunction(() => window.__grasp && window.__grasp.state().bones >= 50, {timeout: 30000});

const shots = [];
async function shot(name, fn) {
  if (fn) await fn();
  await page.waitForTimeout(250);
  const file = path.join(out, `panel-${name}.png`);
  await page.screenshot({path: file, fullPage: true});
  shots.push(name);
}

await shot('open', () => page.evaluate(() => window.__grasp.applyPreset('open')));
await shot('closed', () => page.evaluate(() => window.__grasp.applyPreset('closed')));
await shot('pulldown-bar', () => page.evaluate(() => window.__grasp.applyPreset('pulldown-bar')));
await shot('left-digits', () => page.evaluate(() => { window.__grasp.setCamera('left-digits'); window.__grasp.applyPreset('closed'); }));
await page.evaluate(() => { window.__grasp.setCamera('left-palm'); window.__grasp.seek(0); window.__grasp.play(); });
await page.waitForTimeout(800);
const playing = await page.evaluate(() => window.__grasp.state().playing);
await shot('playing');
await page.evaluate(() => window.__grasp.pause());
const paused = await page.evaluate(() => window.__grasp.state());
await shot('paused');
await page.evaluate(() => window.__grasp.seek(0.5));
const mid = await page.evaluate(() => window.__grasp.state());
await shot('scrub-mid');
await page.evaluate(() => window.__grasp.seek(1));
const end = await page.evaluate(() => window.__grasp.state());
await shot('scrub-end');
await page.evaluate(() => { document.getElementById('loop').click(); });
const loopOff = await page.evaluate(() => window.__grasp.state().loop === false);

const report = {
  url,
  errors,
  bones: paused.bones,
  handMeshes: paused.handMeshes,
  playingObserved: playing,
  pausedT: paused.t,
  midT: mid.t,
  endT: end.t,
  midLeftCurl: mid.left.curl,
  endLeftCurl: end.left.curl,
  loopOff,
  shots,
  verdict: errors.length === 0 && playing && Math.abs(mid.t - 0.5) < 1e-6 && Math.abs(end.left.curl) < 1e-6 ? 'PANEL_TRANSPORT_PASS' : 'PANEL_TRANSPORT_FAIL',
};
writeFileSync(path.join(out, 'panel-playwright.json'), JSON.stringify(report, null, 2));
console.log(report);
await browser.close();
if (report.verdict !== 'PANEL_TRANSPORT_PASS') process.exit(1);
