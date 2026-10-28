from pathlib import Path
from PIL import Image,PngImagePlugin
from zipfile import ZipFile,ZIP_DEFLATED
import struct,json
r=Path(__file__).resolve().parent;project=r.parents[2]
im=Image.open(r/'mat49-ready-source.png').convert('RGBA').resize((320,200),Image.Resampling.NEAREST)
info=PngImagePlugin.PngInfo();info.add(b'grAb',struct.pack('>ii',0,22));im.save(r/'preview/sprites/M49PA0.png',pnginfo=info)
with ZipFile(project/'dist/mat49-painted-preview.pk3','w',ZIP_DEFLATED) as z:
 for p in (r/'preview').rglob('*'):
  if p.is_file():z.write(p,p.relative_to(r/'preview'))
(r/'asset.json').write_text(json.dumps({'origin':'image_gen edit of the approved painted sprite','status':'painted idle pose; right hand lowered beneath rear receiver; animation not yet authored','canvas':[320,200],'spriteOrigin':[0,22],'runtimeWeaponModel':False,'historicalAccuracy':'not certified','style':'painted retro FPS, original approved reference','blenderFramesUsed':False},indent=2))
