"""Check packaged resource integrity; does not certify visual quality/game balance."""
from pathlib import Path
from zipfile import ZipFile
from PIL import Image
import io,struct,wave,json,re
r=Path(__file__).resolve().parents[1];checks=[]
with ZipFile(r/'dist/crique.ipk3') as z:
 assert z.testzip() is None
 names=z.namelist(); assert all('..' not in n.split('/') and not n.startswith('/') for n in names)
 for n in names:
  b=z.read(n)
  if n.endswith('.png'):
   im=Image.open(io.BytesIO(b));im.load();assert im.width>0 and im.height>0
   if n.startswith('sprites/'):assert b'grAb' in b
  if n.endswith('.wav'):
   with wave.open(io.BytesIO(b)) as w:assert w.getnchannels()==1 and w.getsampwidth()==2 and w.getframerate()==22050
 for n in ['IWADINFO','MAPINFO','ZSCRIPT','MODELDEF','PLAYPAL','maps/MAP01.wad','models/boat.obj','models/crate.obj','models/wood.png']:assert n in names,n
 assert len(z.read('PLAYPAL'))==768
 b=z.read('maps/MAP01.wad');sig,count,start=struct.unpack_from('<4sii',b);assert sig==b'PWAD' and count==3
 for i in range(count):
  ofs,size,n=struct.unpack_from('<ii8s',b,start+i*16);assert ofs+size<=start
  if n.rstrip(b'\0')==b'TEXTMAP':udmf=b[ofs:ofs+size].decode()
 nv=udmf.count('vertex {');ns=udmf.count('sector {');nd=udmf.count('sidedef {')
 for key,limit in [('v1',nv),('v2',nv),('sidefront',nd),('sideback',nd),('sector',ns)]:
  assert all(0<=int(v)<limit for v in re.findall(r'\b'+key+r'=(\d+)',udmf)),key
 checks=['ZIP CRC / paths','PNG decoding / sprite origins','WAV PCM format','standalone core resources','UDMF vertex/sector/side references']
print(json.dumps(dict(passed=checks,files=len(names)),indent=2))
