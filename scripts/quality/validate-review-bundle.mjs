#!/usr/bin/env node
// Evidence completeness validator. Passing means the review package is COMPLETE,
// not that the animation is biomechanically correct.
import {readFileSync,existsSync} from 'node:fs';
import path from 'node:path';
const manifestFile=process.argv[2];
if(!manifestFile){console.error('usage: node scripts/quality/validate-review-bundle.mjs <manifest.json>');process.exit(2);}
const origin=path.dirname(path.resolve(manifestFile));
const issues=[];
let m;
try{m=JSON.parse(readFileSync(manifestFile,'utf8'));}
catch(e){console.error('Review manifest is not readable JSON:',String(e));process.exit(2);}
function check(ok,msg){if(!ok)issues.push(msg);}
function fileRef(ref,label){
  if(typeof ref!=='string'||!ref.trim()){issues.push(label+' missing');return;}
  const abs=path.resolve(origin,ref);
  const rel=path.relative(origin,abs);
  if(rel.startsWith('..')||path.isAbsolute(rel)){issues.push(label+' escapes bundle root');return;}
  check(existsSync(abs),label+' missing file: '+ref);
}
check(/^([a-f0-9]{40})$/.test(m.commit||''),'commit must be a full Git SHA');
check(/^([a-f0-9]{64})$/.test(m.anatomyGlbSha256||''),'anatomyGlbSha256 must be SHA-256');
check(m.exercise==='lat-pulldown','exercise must be lat-pulldown for this pilot');
check(m.variant==='seated-front-pulldown','variant must match acceptance contract');
fileRef(m.video,'video');
fileRef(m.trajectoryCsv,'trajectoryCsv');
for(const view of ['front','side','back','grip']){
  const frames=m.frames?.[view];
  for(const pct of ['0','25','50','75','100'])fileRef(frames?.[pct],`frames.${view}.${pct}`);
}
let blocking=false;
for(const key of ['biomechanics','visual','exerciseScience','softwareQa']){
  const report=m.reviews?.[key];
  fileRef(report?.file,'reviews.'+key+'.file');
  const verdict=report?.verdict;
  check(['PASS','FAIL','INCONCLUSIVE'].includes(verdict),'reviews.'+key+'.verdict invalid');
  if(verdict!=='PASS')blocking=true;
}
check(['pending','approved','rejected'].includes(m.userApproval),'userApproval must be pending/approved/rejected');
if(m.readyForMerge===true) {
  check(!blocking,'readyForMerge requires four PASS verdicts');
  check(m.userApproval==='approved','readyForMerge requires explicit owner approval');
}
if(issues.length){console.error('EVIDENCE_INVALID\n- '+issues.join('\n- '));process.exit(1);}
console.log('EVIDENCE_COMPLETE; reviewer verdicts and owner approval still control release.');
