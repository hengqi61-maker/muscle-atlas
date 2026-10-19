"""Mac adapter using, without copying, the Windows-owned exchange contract."""
import argparse, hashlib, importlib.util, json, subprocess
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[2]
TOLERANCE=2e-5
WINDOWS_COMMIT='c12e30eed644e797206fe1296010b252c9325de3'

def load_contract(root):
 spec=importlib.util.spec_from_file_location('windows_kinematics',Path(root)/'scripts/biomechanics/kinematics.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module

def main(contract_root):
 for relative in ['scripts/biomechanics/kinematics.py','schemas/kinematics/packet-v1.schema.json']:
  frozen=subprocess.check_output(['git','show',WINDOWS_COMMIT+':'+relative],cwd=contract_root)
  assert (Path(contract_root)/relative).read_bytes()==frozen, 'Contract differs from frozen Windows W2: '+relative
 k=load_contract(contract_root);out=ROOT/'docs/rig-v2/handoff/v1';native_path=out/'native-observations.json';gltf_path=ROOT/'docs/rig-v2/handoff/mac-observation-v0.1.json'
 native=json.loads(native_path.read_text());gltf=json.loads(gltf_path.read_text());commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
 digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
 def packet(kind,ref,reference,samples,uri,sha,up):
  parents={b['name']:b['parentBone'] for b in (native['rest'] if kind=='blender-export' else gltf['bones'])}
  def transforms(obs):return {b['name']:{'localMatrix':b['localMatrix'] if parents[b['name']] else b['worldMatrix'],'worldMatrix':b['worldMatrix']} for b in obs}
  node_tr=transforms(reference)
  return {'schemaVersion':'1.0.0','experimentId':'rig-v2-'+kind+'-'+ref,'source':{'kind':kind,'uri':uri,'sha256':sha,'gitCommit':gltf['source']['assetCommit'],'producerCommit':commit,'assetSha256':native['sourceBlendSha256'] if kind=='blender-export' else gltf['source']['modelSha256'],'software':'Blender '+native['blenderVersion'] if kind=='blender-export' else 'Three.js '+gltf['source']['threeVersion'],'licenseStatus':'Source model terms remain separate; no relicensing by this numeric packet'},'coordinates':{'lengthUnit':'m','timeUnit':'s','handedness':'right','axes':{'x':'numeric X; anatomical axes uncalibrated','y':'up' if up=='Y' else 'numeric Y; native front is -Y','z':'up' if up=='Z' else 'numeric Z'},'matrixStorage':'column-major-16','vectorConvention':'column-vectors','transformMeaning':'T_parent_from_local; T_world_from_local','rotationConvention':'active-right-handed-matrix'},'referencePose':{'kind':ref,'description':'Actual '+ref+'; not anatomical calibration; non-bone parent folded into root local','anatomicallyCalibrated':False},'coverage':{'sides':['left','right','midline'],'mirrored':False,'independentlyValidated':False},'evidence':{'type':'script-derived','confidence':'high-numerical','uncertainties':['Authored diagnostic trajectories, not measured physiological motion','Anatomical axes, joint centres and attachments uncalibrated']},'nodes':[{'id':name,'parentId':parents[name],'side':'left' if name.startswith('Left') else 'right' if name.startswith('Right') else 'midline',**tr,'anatomicalAxesKnown':False} for name,tr in node_tr.items()],'samples':[{'timeSeconds':s['timeSeconds'],'phase':str(s['phase']),'transforms':transforms(s['bones']),'origin':'model-provided'} for s in samples],'attachments':[]}
 packets={}
 def save(name,p):
  errors=k.validate(p);assert not errors,(name,errors);(out/(name+'.packet.json')).write_text(json.dumps(p,indent=2));packets[name]=p
 save('blender-rest',packet('blender-export','model-default',native['rest'],[],str(native_path.relative_to(ROOT)),digest(native_path),'Z'))
 save('gltf-default',packet('gltf-observation','default-node',gltf['reference'],[],str(gltf_path.relative_to(ROOT)),digest(gltf_path),'Y'))
 # glTF skeleton inverse binds are skin-space references; this asset has one skin.
 assert len({json.dumps(s['joints'],sort_keys=True) for s in gltf['skins']})==1, 'Ambiguous skeleton inverse binds'
 assert all(np.allclose(k.matrix(s['bindMatrix']),np.eye(4),atol=1e-8) for s in gltf['skins']), 'Nonidentity mesh bind requires explicit skin-space handling'
 skin=gltf['skins'][0];world={j['name']:np.linalg.inv(k.matrix(j['inverseBindMatrix'])) for j in skin['joints']};bind=[]
 for b in gltf['bones']:
  w=world[b['name']];p=b['parentBone'];bind.append({'name':b['name'],'worldMatrix':k.flat(w),'localMatrix':k.flat(np.linalg.inv(world[p])@w if p else w)})
 save('gltf-bind',packet('gltf-observation','inverse-bind-derived',bind,[],str(gltf_path.relative_to(ROOT)),digest(gltf_path),'Y'))
 for c in native['clips']:save('blender-'+c['name'],packet('blender-export','animation-time0',c['frames'][0]['bones'],c['frames'],str(native_path.relative_to(ROOT)),digest(native_path),'Z'))
 for c in gltf['clips']:save('gltf-'+c['name'],packet('gltf-observation','animation-time0',c['frames'][0]['bones'],[c['frames'][i] for i in c['fixedPhaseFrameIndices']],str(gltf_path.relative_to(ROOT)),digest(gltf_path),'Y'))
 # Actual native rest S0 and actual glTF default T0 derive each local-frame offset.
 A=np.array([[1,0,0,0],[0,0,1,0],[0,-1,0,0],[0,0,0,1]],float)
 nref={b['name']:k.matrix(b['worldMatrix']) for b in native['rest']};gref={b['name']:k.matrix(b['worldMatrix']) for b in gltf['reference']}
 mapping={'formula':'T_target=A*U_s(T_source)*B','unitScale':1,'worldAlignmentA':k.flat(A),'tolerance':TOLERANCE,'meaning':'Numeric reference alignment only; not anatomical or joint-centre calibration','nodes':[]};maxerr=0;phase_error=0
 for name,S in nref.items():
  B=k.reference_offset(S,gref[name],A);mapping['nodes'].append({'sourceId':name,'targetId':name,'frameOffsetB':k.flat(B)})
  for c in native['clips']:
   gc=next(x for x in gltf['clips'] if x['name']==c['name'])
   for i,s in enumerate(c['frames']):
    w=k.matrix(next(x for x in s['bones'] if x['name']==name)['worldMatrix']);t=k.map_transform(w,A,B);back=k.unmap_transform(t,A,B);maxerr=max(maxerr,float(np.max(np.abs(back-w))))
    target=k.matrix(next(x for x in gc['frames'][gc['fixedPhaseFrameIndices'][i]]['bones'] if x['name']==name)['worldMatrix']);phase_error=max(phase_error,float(np.max(np.abs(t-target))))
 (out/'native-gltf-mapping.json').write_text(json.dumps(mapping,indent=2))
 report={'windowsOwnerCommit':WINDOWS_COMMIT,'contractRoot':str(Path(contract_root).resolve()),'contractCommit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=contract_root,text=True).strip(),'schemaSha256':digest(Path(contract_root)/'schemas/kinematics/packet-v1.schema.json'),'librarySha256':digest(Path(contract_root)/'scripts/biomechanics/kinematics.py'),'packetsValidated':list(packets),'nodesPerPacket':27,'samplesPerClip':5,'mathematicalRoundtripMaxError':maxerr,'actualNativeToGltfPhaseMaxElementError':phase_error,'predeclaredTolerance':TOLERANCE,'nativeWriteRead':native['nativeWriteRead'],'notProven':['Anatomical calibration','OpenSim model equivalence','Physiological motion quality']}
 assert maxerr<TOLERANCE;assert phase_error<TOLERANCE,report
 (out/'validation-report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--contract-root',required=True);a=p.parse_args();main(a.contract_root)
