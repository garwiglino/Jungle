from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import re,json
from PIL import Image
r=Path(__file__).resolve().parents[1]
log=(r/'reports/mat49-corrected.log').read_text();assert 'Init complete.' in log
assert not re.search('Script error|VM execution aborted|not found|Unknown texture',log)
states=[tuple(map(int,m)) for m in re.findall(r'mag=(\d+) reserve=(\d+)',log)]
assert states[:3]==[(32,150),(26,150),(32,144)],states
for f in 'ABCDEFGH':
 im=Image.open(r/'art/mat49/preview/sprites'/('MAT4'+f+'0.png'));assert im.mode=='RGBA' and im.size==(320,200)
files=[]
for folder in ['src','tools','docs','tests','LICENSES','art/mat49']:
 files.extend(p for p in (r/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.blend1')
files += [r/p for p in ['README.md','LICENSE','requirements.txt','lancer.sh','.gitignore','dist/crique.ipk3','dist/mat49-preview.pk3','reports/mat49-pose-corrigee.png','reports/mat49-tir-recharge.mp4','reports/mat49-corrected.log','reports/mat49-blender.log','reports/build.json','reports/resource-validation.json']]
archive=r/'dist/MAT49-pose-corrigee.zip'
with ZipFile(archive,'w',ZIP_DEFLATED) as z:
 for p in sorted(files):z.write(p,'crique/'+str(p.relative_to(r)))
with ZipFile(archive) as z:assert z.testzip() is None
print(json.dumps({'archive':str(archive),'bytes':archive.stat().st_size,'frames':8,'gameplay':'32 -> 26 -> 32, reserve 150 -> 144'},ensure_ascii=False))
