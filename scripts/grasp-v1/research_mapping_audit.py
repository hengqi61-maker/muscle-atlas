"""Read-only reproduce PR21's authored transverse digit assignment; no bpy or asset write."""
import json
from pathlib import Path
DIGITS=['Thumb','Index','Middle','Ring','Little']
def assigned(u):
 n=max(0,min(1,(u+.02)/.08));di=max(0,min(4,int(round(n*4))))
 if u>.035:di=4
 digit=DIGITS[di] if di<4 else 'Thumb'
 if u<.028 and di==4:digit='Index'
 return digit
rows=[]
for i,digit in enumerate(DIGITS):
 t=i/4;u=-.018*(1-t)+.055*t
 if digit=='Thumb':u=.055*.85
 rows.append({'authoredBoneDigit':digit,'authoredMCPAcrossM':u,'weightRuleDigitAtSameAcrossCoordinate':assigned(u)})
out=Path('artifacts/grasp-research');out.mkdir(exist_ok=True,parents=True);(out/'mapping.json').write_text(json.dumps({'scope':'Static code-rule reproduction only, not anatomically calibrated assignment','rows':rows,'reachableDigits':sorted({assigned(-.1+i*.0001) for i in range(2001)})},indent=2));print(json.dumps(rows,indent=2))
