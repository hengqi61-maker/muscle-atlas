"""Real Blender exception must stop the pipeline before encoding or PASS creation."""
import subprocess,tempfile,json
from pathlib import Path
root=Path(__file__).resolve().parents[3];out=root/'artifacts/motion-pipeline/failure-fixture';out.mkdir(parents=True,exist_ok=True);fixture=out/'intentional-error.py';fixture.write_text("raise RuntimeError('E3 deliberate strict failure fixture')\n")
p=subprocess.run(['/Applications/Blender.app/Contents/MacOS/Blender','-b','--python-exit-code','1','--python',str(fixture)],capture_output=True,text=True);(out/'blender.log').write_text(p.stdout+p.stderr)
# Same checked subprocess sequencing as production; later operations only follow success.
encoded=False;passed=False
try:
 p.check_returncode();encoded=True;passed=True
except subprocess.CalledProcessError:pass
result={'exitCode':p.returncode,'encodeWouldRun':encoded,'passManifestWouldBeCreated':passed,'passed':p.returncode!=0 and not encoded and not passed};(out/'result.json').write_text(json.dumps(result,indent=2));assert result['passed'];print(result)
