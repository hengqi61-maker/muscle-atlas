import fs from'node:fs';import path from'node:path';import{fileURLToPath}from'node:url';
export function nextAction(m){
 if(m.stage==='M1'||!m.repairScopeApproval)return{action:'WAIT_OWNER_SCOPE',mayModifyProduction:false};
 if(m.reworkCycles>=2)return{action:'STOP_AND_ESCALATE',mayModifyProduction:false};
 const blockers=(m.defects||[]).filter(d=>['P0','P1'].includes(d.severity)&&d.status!=='RESOLVED');
 if(blockers.length)return{action:'ASSIGN_SCOPED_REWORK_THEN_NEW_FROZEN_REVIEW',mayModifyProduction:true,scope:m.repairScopeApproval,blockers:blockers.map(d=>d.id),nextCycle:(m.reworkCycles||0)+1};
 return{action:'WAIT_OWNER_M3_ACCEPTANCE',mayModifyProduction:false};
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url))console.log(JSON.stringify(nextAction(JSON.parse(fs.readFileSync(process.argv[2]))),null,2));
