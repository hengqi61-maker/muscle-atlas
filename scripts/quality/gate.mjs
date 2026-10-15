import fs from 'node:fs';import path from 'node:path';import crypto from 'node:crypto';import{fileURLToPath}from'node:url';import{spawnSync}from'node:child_process';
export function assess(m,release=false){const errors=[];const roles=['biomechanics','visual','exerciseScience','softwareQa'];const allowed=['PASS','FAIL','INCONCLUSIVE'];
 if(!/^[a-f0-9]{40}$/.test(m.commit||''))errors.push('full commit required');
 if(!/^[a-f0-9]{64}$/.test(m.anatomyGlbSha256||''))errors.push('asset sha256 required');
 if((m.sampleCount||0)<21)errors.push('at least21samples required');
 if(m.reworkCycles>2)errors.push('two-cycle limit exceeded; return to owner');
 const sessions=roles.map(r=>m.reviews?.[r]?.session);if(sessions.some(s=>!s)||new Set(sessions).size!==4)errors.push('four distinct reviewer sessions required');
 if(sessions.some(s=>m.producerSessions?.includes(s)))errors.push('producer cannot release own work');
 for(const role of roles)if(!allowed.includes(m.reviews?.[role]?.verdict))errors.push('invalid verdict '+role);
 if(release||m.readyForMerge===true){if(roles.some(r=>m.reviews?.[r]?.verdict!=='PASS'))errors.push('release requires four PASS verdicts');if(m.userApproval!=='approved'||!m.ownerApprovalEvidence)errors.push('explicit owner approval evidence required');if(m.defects?.some(d=>['P0','P1'].includes(d.severity)&&d.status!=='RESOLVED'))errors.push('unresolved P0/P1 blocks release')}
 return errors;
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)){
 const file=path.resolve(process.argv[2]),base=path.dirname(file),m=JSON.parse(fs.readFileSync(file));const errors=assess(m,process.argv.includes('--release'));const bundle=spawnSync(process.execPath,[path.join(path.dirname(fileURLToPath(import.meta.url)),'validate-review-bundle.mjs'),file],{encoding:'utf8'});if(bundle.status!==0)errors.push('incomplete evidence bundle: '+bundle.stderr);if(Object.keys(m.evidenceHashes||{}).length<26)errors.push('hash manifest must include20frames,video,trajectory and4reports');
 for(const [ref,h]of Object.entries(m.evidenceHashes||{})){const f=path.resolve(base,ref);if(!f.startsWith(base+path.sep)||!fs.existsSync(f))errors.push('invalid evidence path '+ref);else if(crypto.createHash('sha256').update(fs.readFileSync(f)).digest('hex')!==h)errors.push('changed evidence '+ref)}
 if(errors.length){console.error(errors.join('\n'));process.exit(1)}console.log(process.argv.includes('--release')?'RELEASE_FIELDS_VALID; human approval provenance must still be verified':'REVIEW_METADATA_VALID; not release approval');
}
