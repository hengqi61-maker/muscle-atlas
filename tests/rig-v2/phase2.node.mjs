import test from'node:test';import assert from'node:assert/strict';import fs from'node:fs';import crypto from'node:crypto';
const baseline=fs.readFileSync('public/experimental/rig-v2/unified-rig-prototype.glb');
for(const dir of ['E01-local-gradient','E02-elbow-axis-basis'])test(`${dir}: actual derivation changes only declared float bytes`,()=>{const b=fs.readFileSync(`artifacts/phase2/${dir}/motion.glb`),d=JSON.parse(fs.readFileSync(`artifacts/phase2/${dir}/derivation.json`));assert.equal(b.length,baseline.length);assert.equal(crypto.createHash('sha256').update(b).digest('hex'),d.outputSha256);const allowed=new Set(d.changes.flatMap(c=>[0,1,2,3].map(k=>c.offset+k)));let count=0;for(let i=0;i<b.length;i++)if(b[i]!==baseline[i]){count++;assert.ok(allowed.has(i));}assert.equal(count,d.differingBytes);assert.ok(count>0);if(dir.startsWith('E01')){assert.equal(d.singleVariable.selectedExportedVertices.length,22);assert.equal(new Set(d.changes.map(c=>c.accessor)).size,1);}else{assert.equal(d.singleVariable.modified.length,4);for(const c of d.singleVariable.modified){assert.equal(c.samples,121);assert.ok(c.maxAxisDeltaDegrees>4.68&&c.maxAxisDeltaDegrees<4.71);assert.ok(c.maxAngleErrorRadians<1e-6);}}});

test('new continuity screen reproduces rejected E01 and does not mistake E02 for a seam fix',async()=>{const {spawnSync}=await import('node:child_process');for(const [dir,expected]of [['E01-local-gradient',1],['E02-elbow-axis-basis',0]]){const output=`artifacts/phase2/${dir}/seam-regression.json`,p=spawnSync(process.execPath,['scripts/rig-v2/phase2/seam-check.mjs','--asset',`artifacts/phase2/${dir}/motion.glb`,'--output',output],{encoding:'utf8'});assert.equal(p.status,expected,p.stderr);const r=JSON.parse(fs.readFileSync(output));assert.equal(r.pairCount,1785);assert.equal(r.clips.length,2);if(expected)assert.ok(r.clips[1].afterMaxM>.003);}});

test('E03 preserves exact equivalent vertices and repeats without changing geometry or animation',()=>{
 const dir='artifacts/phase2/E03-equivalence-projection',b=fs.readFileSync(`${dir}/motion.glb`),d=JSON.parse(fs.readFileSync(`${dir}/derivation.json`));
 assert.deepEqual(b,fs.readFileSync('artifacts/phase2/repeat-E03/motion.glb'));
 assert.equal(crypto.createHash('sha256').update(b).digest('hex'),d.outputSha256);
 const allowed=new Set(d.changes.flatMap(c=>[0,1,2,3].map(k=>c.offset+k)));for(let i=0;i<b.length;i++)if(b[i]!==baseline[i])assert.ok(allowed.has(i));
 assert.equal(new Set(d.changes.map(c=>c.accessor)).size,1);assert.equal(new Set(d.changes.map(c=>c.index)).size,43);
 assert.equal(d.singleVariable.selectedExportedVertices.length,22);assert.equal(d.singleVariable.equivalenceClasses.length,21);
 const byIndex=new Map();for(const c of d.changes){if(!byIndex.has(c.index))byIndex.set(c.index,[]);byIndex.get(c.index)[c.component]=c.after;}
 for(const c of d.singleVariable.equivalenceClasses)for(const i of c.members)assert.deepEqual(byIndex.get(i),byIndex.get(c.members[0]));
 const seam=JSON.parse(fs.readFileSync(`${dir}/seam-report.json`));assert.equal(seam.candidateSha256,d.outputSha256);assert.equal(seam.status,'AUTO PASS');for(const c of seam.clips)assert.equal(c.afterMaxM,0);
});
