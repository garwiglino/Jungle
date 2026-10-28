from pathlib import Path
from PIL import Image,PngImagePlugin
from zipfile import ZipFile,ZIP_DEFLATED
import struct,json
r=Path(__file__).resolve().parents[1];project=r.parents[1];out=r/'preview/sprites';out.mkdir(exist_ok=True)
for old in out.glob('*.png'):old.unlink()
for f in 'ABCDEFGH':
 im=Image.open(r/'blender'/('MAT4'+f+'0-source.png')).convert('RGBA').resize((320,200),Image.Resampling.NEAREST)
 info=PngImagePlugin.PngInfo();info.add(b'grAb',struct.pack('>ii',0,22));im.save(out/('MAT4'+f+'0.png'),pnginfo=info)
with ZipFile(project/'dist/mat49-preview.pk3','w',ZIP_DEFLATED) as z:
 for p in (r/'preview').rglob('*'):
  if p.is_file():z.write(p,p.relative_to(r/'preview'))
(r/'asset.json').write_text(json.dumps({'origin':'original procedural Blender geometry, materials and animation, CC0-1.0','status':'prototype sprites; pose corrected by modeled grip below receiver; not a historical replica','canvas':[320,200],'spriteOrigin':[0,22],'frames':list('ABCDEFGH'),'gun3DInEngine':False,'sourceBlend':'blender/mat49-pose.blend','previousImage':'legacy/previous-side-grip.png is the previous pose, not used by current PK3'},indent=2))
