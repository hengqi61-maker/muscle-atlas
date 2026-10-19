"""Run actual GLB calibration or native render+encode; refuses existing output."""
import argparse,subprocess,json,hashlib,time
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--asset');p.add_argument('--output',required=True);p.add_argument('--contract');p.add_argument('--calibrate',nargs='+');p.add_argument('--smoke',action='store_true');a=p.parse_args();out=Path(a.output).resolve();assert not out.exists(),out;out.mkdir(parents=True)
script=Path(__file__).with_name('render.py').resolve();(out/'render-executed.py').write_bytes(script.read_bytes());(out/'run-render-executed.py').write_bytes(Path(__file__).read_bytes());start=time.monotonic()
if a.calibrate:args=['--calibrate',str(out)]+[str(Path(x).resolve()) for x in a.calibrate]
else:
 assert a.asset and a.contract;args=[str(Path(a.asset).resolve()),str(out),str(Path(a.contract).resolve())]+(['--smoke'] if a.smoke else [])
with (out/'blender.log').open('w') as log:subprocess.run(['/Applications/Blender.app/Contents/MacOS/Blender','-b','--python-exit-code','1','--python',str(script),'--',*args],stdout=log,stderr=subprocess.STDOUT,check=True)
if not a.calibrate:
 native=json.loads((out/'native.json').read_text())
 if not a.smoke:
  for clip in native['clips']:
   d=out/clip['clip']
   with (out/'ffmpeg.log').open('a') as log:subprocess.run(['ffmpeg','-y','-framerate',str(30/clip['durationSeconds']),'-i',str(d/'sequence/%04d.png'),'-c:v','libx264','-pix_fmt','yuv420p',str(d/'motion.mp4')],stdout=subprocess.DEVNULL,stderr=log,check=True)
files=[{'path':str(f.relative_to(out)),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'bytes':f.stat().st_size} for f in sorted(out.rglob('*')) if f.is_file()]
(out/'manifest.json').write_text(json.dumps({'status':'CALIBRATION_COMPLETE' if a.calibrate else ('SMOKE_NOT_REVIEWED' if a.smoke else 'RENDERED_NOT_REVIEWED'),'wallSeconds':time.monotonic()-start,'files':files,'producerSha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'ffmpegVersion':subprocess.check_output(['ffmpeg','-version'],text=True).splitlines()[0]},indent=2))
