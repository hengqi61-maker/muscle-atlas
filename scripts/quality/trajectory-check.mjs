import fs from'node:fs';
const file=process.argv[2],out=process.argv[3],d=JSON.parse(fs.readFileSync(file)),rows=d.samples;
const pairs=[['UpperArm','Forearm'],['Forearm','LeftHand'],['RightUpperArm','RightForearm'],['RightForearm','RightHand']];
const dist=(a,b)=>Math.hypot(...a.map((v,i)=>v-b[i]));const angle=(a,b)=>2*Math.acos(Math.min(1,Math.abs(a.reduce((v,x,i)=>v+x*b[i],0))))*180/Math.PI;
let maxStepDistance_m=0,maxStepAngle_deg=0,maxSpeed_m_s=0;const failures=[];
if(rows.length<21)failures.push('fewer than21samples');
for(let i=0;i<rows.length;i++)for(const [name,b]of Object.entries(rows[i].joints)){
 const values=[...b.position_m,...b.quaternion_xyzw];if(!values.every(Number.isFinite))failures.push('nonfinite '+name);if(Math.abs(Math.hypot(...b.quaternion_xyzw)-1)>.001)failures.push('unnormalized quaternion '+name);
 if(i){const before=rows[i-1],dt=rows[i].time_s-before.time_s;if(dt<=0)failures.push('nonincreasing time');const step=dist(b.position_m,before.joints[name].position_m);maxStepDistance_m=Math.max(maxStepDistance_m,step);maxSpeed_m_s=Math.max(maxSpeed_m_s,step/dt);maxStepAngle_deg=Math.max(maxStepAngle_deg,angle(b.quaternion_xyzw,before.joints[name].quaternion_xyzw))}
}
const segments=pairs.map(([a,b])=>{const lengths=rows.map(r=>dist(r.joints[a].position_m,r.joints[b].position_m)),min=Math.min(...lengths),max=Math.max(...lengths);if(max-min>.001)failures.push('fixed segment changed>1mm '+a);return{from:a,to:b,min_m:min,max_m:max,range_m:max-min}});
const endpointMaxDistance_m=Math.max(...Object.keys(rows[0].joints).map(n=>dist(rows[0].joints[n].position_m,rows.at(-1).joints[n].position_m)));
const report={samples:rows.length,failures,segments,maxStepDistance_m,maxStepAngle_deg,maxSpeed_m_s,endpointMaxDistance_m,method:'Adjacent sampled world transforms; absolute quaterniondot handles sign. Fixedsegment tolerance1mm is modelrig invariant, not human criterion. Step/speed metrics are descriptive with no universal physiological cutoff. Samples can miss intersample snapping. Does not certify muscleforce,actualsurfacecontact,shouldercoordination.'};fs.writeFileSync(out,JSON.stringify(report,null,2));console.log(report);if(failures.length)process.exit(1);
