#!/usr/bin/env node
import fs from 'node:fs';import path from 'node:path';import crypto from 'node:crypto';import {spawnSync}from'node:child_process';import {fileURLToPath}from'node:url';
const argv=process.argv.slice(2),command=argv.shift(),arg=k=>argv[argv.indexOf('--'+k)+1];
function required(k){if(!argv.includes('--'+k)||!arg(k))throw Error('--'+k+' required');return arg(k)}
const worktree=path.resolve(required('worktree')),out=path.resolve(required('out')),ref=required('ref');
const run=(cmd,args,options={})=>{const r=spawnSync(cmd,args,{cwd:worktree,encoding:'utf8',...options});if(r.status!==0)throw Error(`${cmd} ${args.join(' ')} failed (${r.status}): ${r.stderr||r.error}`);return r.stdout};
const sha=run('git',['rev-parse','HEAD']).trim();if(sha!==ref||!/^[0-9a-f]{40}$/.test(ref))throw Error('Frozen HEAD differs from full --ref');
fs.mkdirSync(out,{recursive:true});const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
if(command==='freeze'){
 const tracked=run('git',['ls-files','src','scripts','public/models','tests','package.json','package-lock.json','vite.config.ts','playwright.config.ts']).trim().split('\n');const files={};
 for(const f of tracked){const bytes=fs.readFileSync(path.join(worktree,f)),committed=spawnSync('git',['show',sha+':'+f],{cwd:worktree,maxBuffer:100*1024*1024});if(committed.status!==0||hash(bytes)!==hash(committed.stdout))throw Error('Modified frozen input: '+f);files[f]=hash(bytes)}
 const asset=required('asset');fs.mkdirSync(path.join(out,'assets'),{recursive:true});fs.copyFileSync(path.join(worktree,asset),path.join(out,'assets',path.basename(asset)));
 const archive=spawnSync('git',['archive',sha,'src','scripts','tests','package.json','package-lock.json','AGENTS.md','vite.config.ts','playwright.config.ts'],{cwd:worktree,maxBuffer:100*1024*1024});if(archive.status!==0)throw Error('git archive failed');fs.writeFileSync(path.join(out,'frozen-code.tar'),archive.stdout);
 fs.writeFileSync(path.join(out,'freeze.json'),JSON.stringify({commit:sha,asset,assetSha256:files[asset],files,blendFiles:run('git',['ls-files','*.blend']).trim().split('\n').filter(Boolean),noBlendMeaning:'No tracked blend means original authoring scene not established, not permission to invent provenance.'},null,2));console.log('FROZEN '+sha)
}else if(['measure','capture','mesh-kinematics'].includes(command)){
 const adapter=required('adapter');if(!/^[a-z0-9-]+$/.test(adapter))throw Error('Invalid adapter name');const script=path.join(path.dirname(fileURLToPath(import.meta.url)),'adapters',adapter,command+'.mjs');if(!fs.existsSync(script))throw Error('Adapter not implemented: '+adapter);
 const args=[script,'--out',out];if(command==='capture')args.push('--url',required('url'));
 run(process.execPath,args,{stdio:'inherit'});
}else throw Error('Use freeze, measure or capture');
