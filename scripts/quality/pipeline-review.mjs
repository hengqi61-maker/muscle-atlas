/** Evidence validation is deliberately independent of motion or owner approval. */
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {fileURLToPath} from 'node:url';
import {assess} from './gate.mjs';
export const roles=['biomechanics','visual','exerciseScience','softwareQa'];
export function stageReport(manifest,review){
  const normalize=(value,prefix)=>value===prefix+'_PASS'||value==='PASS';
  const build=normalize(manifest.build?.status,'BUILD');
  const software=normalize(manifest.softwareTests?.status,'SOFTWARE_TEST');
  const geometry=manifest.motionGeometry?.status??'INCONCLUSIVE';
  const reviewed=roles.every(r=>review?.reviews?.[r]);
  const metadataErrors=reviewed?assess(review,false):['four independent reviews pending'];
  const approved=review?.userApproval==='approved'&&!!review?.ownerApprovalEvidence;
  const releaseErrors=[...metadataErrors,...(!build?['build not passed']:[]),...(!software?['software tests not passed']:[]),...(!['PASS','MOTION_GEOMETRY_PASS'].includes(geometry)?['motion geometry not passed']:[])];
  if(reviewed)releaseErrors.push(...assess(review,true));else releaseErrors.push('review gate pending');
  if(!approved)releaseErrors.push('owner approval pending');
  return {BUILD:build?'BUILD_PASS':'BUILD_FAIL_OR_INCONCLUSIVE',SOFTWARE_TEST:software?'SOFTWARE_TEST_PASS':'SOFTWARE_TEST_FAIL_OR_INCONCLUSIVE',MOTION_GEOMETRY:geometry,BIOMECHANICS_REVIEW:review?.reviews?.biomechanics?.verdict??'PENDING',VISUAL_REVIEW:review?.reviews?.visual?.verdict??'PENDING',EXERCISE_SCIENCE_REVIEW:review?.reviews?.exerciseScience?.verdict??'PENDING',SOFTWARE_QA_REVIEW:review?.reviews?.softwareQa?.verdict??'PENDING',OWNER_APPROVAL:approved?'RECORDED_REQUIRES_HUMAN_PROVENANCE_CHECK':'PENDING',metadataErrors,releaseErrors:[...new Set(releaseErrors)],mayRelease:releaseErrors.length===0};
}
export function verifyReviewBinding(manifest,review,candidate){
 if(!review)return [];
 const errors=[];
 if(!/^[a-f0-9]{40}$/.test(candidate??''))errors.push('explicit full frozen candidate required');
 else if(review.commit!==candidate)errors.push('review commit mismatch');
 const asset=Array.isArray(manifest.files)?manifest.files.find(f=>f.path===manifest.outputs?.glb):null;
 if(!asset||review.anatomyGlbSha256!==asset.sha256)errors.push('review asset mismatch');
 return errors;
}
export function verifyInventory(manifest){
 const errors=[],entries=manifest.files??[], refs=new Set(Array.isArray(entries)?entries.map(e=>e.path):Object.keys(entries));
 for(const name of ['glb','blend','trajectory','video'])if(typeof manifest.outputs?.[name]!=='string'||!refs.has(manifest.outputs[name]))errors.push('missing inventoried output '+name);
 if(typeof manifest.outputs?.browser!=='string'||!refs.has(manifest.outputs.browser+'/report.json'))errors.push('inventoried actual Three consumer report required');
 if(!refs.has('validator.json'))errors.push('inventoried GLB validator report required');
 const frames=manifest.outputs?.keyframes;if(!Array.isArray(frames)||frames.length<50||new Set(frames).size!==frames.length||frames.some(p=>!refs.has(p)))errors.push('50 unique inventoried keyframes required');
 return errors;
}
export function verifyFiles(base,entries){
 const errors=[];const pairs=Array.isArray(entries)?entries.map(e=>[e.path,e.sha256]):Object.entries(entries??{}).map(([k,v])=>[k,typeof v==='string'?v:v.sha256]);
 if(!pairs.length)errors.push('empty evidence inventory');
 const seen=new Set();
 for(const [ref,expected]of pairs){
  if(typeof ref!=='string'||seen.has(ref)){errors.push('invalid/duplicate evidence path');continue;}seen.add(ref);
  const target=path.resolve(base,ref),root=fs.realpathSync(base);
  if(!target.startsWith(path.resolve(base)+path.sep)||!fs.existsSync(target)||!fs.realpathSync(target).startsWith(root+path.sep)){errors.push('missing or escaped evidence '+ref);continue;}
  const sha=crypto.createHash('sha256').update(fs.readFileSync(target)).digest('hex');if(sha!==expected)errors.push('changed evidence '+ref);
 }
 return errors;
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)){
 const file=path.resolve(process.argv[2]??''),manifest=JSON.parse(fs.readFileSync(file)),reviewPath=process.argv.find(a=>a.startsWith('--review='))?.slice(9),review=reviewPath?JSON.parse(fs.readFileSync(reviewPath)):null;
 const report={evidenceErrors:[...verifyInventory(manifest),...verifyFiles(path.dirname(file),manifest.files)],...stageReport(manifest,review)};
 // A review declaring a different fixed asset/commit is never applicable.
 const candidate=process.argv.find(a=>a.startsWith('--candidate='))?.slice(12);
 report.evidenceErrors.push(...verifyReviewBinding(manifest,review,candidate));
 report.mayRelease=report.mayRelease&&report.evidenceErrors.length===0;
 console.log(JSON.stringify(report,null,2));if(report.evidenceErrors.length||process.argv.includes('--release')&&!report.mayRelease)process.exitCode=1;
}
