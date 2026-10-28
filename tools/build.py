#!/usr/bin/env python3
"""Deterministic original prototype assets + UDMF builder; Python 3 + Pillow."""
from pathlib import Path
import random,math,struct,zipfile,json,wave,io,hashlib
from PIL import Image,ImageDraw,PngImagePlugin
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'build'; OUT.mkdir(exist_ok=True)
files={}; registry=[]; rng=random.Random(2718)
def put(n,b): files[n]=b.encode() if isinstance(b,str) else b
def png(n,im,offset=None,kind='prototype'):
 b=io.BytesIO(); info=PngImagePlugin.PngInfo()
 if offset: info.add(b'grAb',struct.pack('>ii',*offset))
 im.save(b,format='PNG',pnginfo=info); put(n,b.getvalue()); registry.append(dict(path=n,origin=('Rasterisation DejaVu Sans / tools/build.py' if n.startswith('graphics/M_') or n=='graphics/TITLEPIC.png' else 'tools/build.py — dessin/procédural original'),license=('Bitstream-Vera-DejaVu' if n.startswith('graphics/M_') or n=='graphics/TITLEPIC.png' else 'CC0-1.0'),status=kind,size=list(im.size),collision='définie en ZScript ou géométrie UDMF'))
# Textures, generated rather than sampled from commercial IWADs.
for name,base in [('MUD',(65,54,36)),('LEAF',(33,56,33)),('BARK',(65,59,43)),('ROCK',(72,78,67)),('WOOD',(91,79,53)),('METAL',(68,82,77)),('WATER',(36,66,63)),('ROOF',(62,76,69))]:
 im=Image.new('RGB',(128,128)); p=im.load()
 for y in range(128):
  for x in range(128):
   a=rng.randrange(-13,14)+(7*math.sin(x*.5) if name in ['BARK','WOOD'] else 0)+(10*math.sin(y*.3+x*.05) if name=='WATER' else 0)
   p[x,y]=tuple(max(0,min(255,int(c+a))) for c in base)
 d=ImageDraw.Draw(im)
 if name in ['METAL','ROOF']:
  for x in range(0,128,16): d.line((x,0,x,128),fill=(31,44,41),width=2)
 if name=='WOOD':
  for y in range(0,128,32): d.line((0,y,128,y),fill=(35,31,25),width=2)
 png('textures/'+name+'.png',im)
put('models/wood.png',files['textures/WOOD.png'])
# Sky: mist, cloud layers and distant canopy.
im=Image.new('RGB',(1024,256)); d=ImageDraw.Draw(im)
for y in range(256): d.line((0,y,1024,y),fill=(int(115-y*.20),int(142-y*.22),int(134-y*.24)))
for i in range(150):
 x=rng.randrange(1024); y=rng.randrange(140,260); r=rng.randrange(20,90); d.ellipse((x-r,y-r,x+r,y+r),fill=(32+y//12,61+y//20,47+y//25))
png('textures/SKYGUI.png',im)
# Hybrid foliage billboard, solid trunk actor, no Doom sprites.
for name in ['TREE','FERN','CASE','BEAC','MEDI','AMMO']:
 size=(192,256) if name=='TREE' else (96,80); im=Image.new('RGBA',size); d=ImageDraw.Draw(im); w,h=size
 if name=='TREE':
  d.polygon([(83,256),(96,62),(107,54),(117,256)],fill=(59,53,37));
  for j in range(5): d.polygon([(96,205),(43+j*18,255),(101,243)],fill=(72,65,43))
  for j in range(24):
   x=rng.randrange(10,182); y=rng.randrange(5,123); d.ellipse((x-30,y-18,x+30,y+18),fill=(26+rng.randrange(16),53+rng.randrange(22),31,255))
 elif name=='FERN':
  for j in range(14):
   x=rng.randrange(5,91); y=rng.randrange(0,65); d.line((48,80,x,y),fill=(61,95,44),width=2)
   for k in range(3,9):
    t=k/10; px=48+(x-48)*t; py=80+(y-80)*t; d.polygon([(px,py),(px-13,py-7),(px+4,py-4)],fill=(35,74,36))
 else:
  col={'CASE':(174,141,58),'BEAC':(52,186,164),'MEDI':(176,196,172),'AMMO':(82,102,62)}[name]
  d.rounded_rectangle((15,23,81,76),radius=4,fill=col,outline=(22,33,29),width=4); d.rectangle((30,16,65,26),outline=col,width=5)
  if name=='MEDI': d.rectangle((42,34,54,65),fill=(164,49,41)); d.rectangle((31,43,65,55),fill=(164,49,41))
  if name=='CASE': d.text((26,45),'DATA',fill=(20,29,24))
  if name=='BEAC': d.ellipse((30,28,66,64),fill=(131,244,194))
 png(f'sprites/{name}A0.png',im,(w//2,h))
for frame in 'AB':
 im=Image.new('RGBA',(20,20)); d=ImageDraw.Draw(im)
 for k in range(8):
  x=rng.randrange(3,17); y=rng.randrange(3,17); d.ellipse((x-3,y-3,x+3,y+3),fill=(167,153,109,170 if frame=='A' else 70))
 png('sprites/IMPA'+frame+'0.png',im,(10,10))
# Directional militia/raptor figures, intentionally provisional, 8 facings and 3 frames.
for creature,code in [('militia','MLTC'),('raptor','RAPT')]:
 for frame in 'ABC':
  for rot in range(1,9):
   im=Image.new('RGBA',(96,96)); d=ImageDraw.Draw(im); phase=0 if frame=='A' else (-5 if frame=='B' else 5); side=math.sin((rot-1)*math.pi/4)
   if creature=='militia':
    d.ellipse((35,4,59,27),fill=(138,111,80)); d.rectangle((34,6,60,16),fill=(60,69,50)); d.polygon([(32,27),(61,27),(66,62),(29,62)],fill=(73,81,53)); d.rectangle((38,30,55,57),fill=(48,55,42))
    d.line((37,58,33+phase,91),fill=(49,57,41),width=12); d.line((57,58,60-phase,91),fill=(57,63,44),width=12)
    d.line((30,33,20,57),fill=(92,95,61),width=10); d.line((61,34,72,52),fill=(92,95,61),width=10); d.line((19,55,76,43+side*8),fill=(24,31,29),width=6)
   else:
    d.polygon([(17,57),(3,44),(35,48),(56,32),(75,34),(81,43),(58,48),(55,69),(34,72)],fill=(93,111,58)); d.polygon([(70,32),(92,36),(91,44),(67,43)],fill=(124,133,68)); d.ellipse((80,34,83,37),fill=(239,194,71)); d.line((40,64,32+phase,88,46+phase,90),fill=(101,114,61),width=7); d.line((54,62,65-phase,86,77-phase,89),fill=(77,93,49),width=7); d.line((60,48,71,59),fill=(107,121,58),width=4)
    if rot in [5,6,7]: im=im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
   png(f'sprites/{code}{frame}{rot}.png',im,(48,96))
 # Corpse, simple dedicated sprite.
 im=Image.new('RGBA',(96,32)); d=ImageDraw.Draw(im); d.ellipse((4,8,93,30),fill=(56,62,41)); png(f'sprites/{code}D0.png',im,(48,32))
# First-person weapons: eight original sprite poses, no runtime 3D weapon models.
# A ready, B muzzle flash, C recoil, D lower, E remove magazine, F insert, G action, H return.
for code,rifle in [('FREN',True),('PAM9',False)]:
 for frame in 'ABCDEFGH':
  im=Image.new('RGBA',(320,200)); d=ImageDraw.Draw(im); off={'A':0,'B':-3,'C':8,'D':43,'E':32,'F':25,'G':10,'H':4}[frame]
  def poly(pts,col): d.polygon([(x,y+off) for x,y in pts],fill=col)
  poly([(200,200),(212,150),(249,145),(294,200)],(73,81,55)); poly([(207,169),(216,148),(238,148),(250,180)],(145,115,78))
  if rifle:
   poly([(150,199),(166,125),(176,91),(189,91),(204,127),(224,200)],(26,34,32)); poly([(166,153),(173,114),(195,114),(204,155)],(60,70,62)); poly([(177,111),(178,65),(188,65),(189,111)],(27,34,34)); d.rectangle((177,66+off,188,75+off),outline=(130,142,128),width=2); 
   if frame!='E': poly([(160,164),(197,161),(205,194),(154,194)],(45,54,44))
  else:
   poly([(173,199),(175,140),(186,96),(208,96),(222,140),(216,199)],(24,31,31)); poly([(185,102),(208,102),(216,149),(178,149)],(82,91,85)); poly([(181,151),(214,151),(210,184),(179,184)],(45,53,48))
  if frame in 'EF':
   mx,my=(108,172) if frame=='E' else (147,163)
   d.polygon([(mx-8,my+28),(mx-1,my-12),(mx+18,my-9),(mx+23,my+28)],fill=(38,48,40))
   d.polygon([(mx-40,200),(mx-26,my+10),(mx-5,my+4),(mx+18,my+15),(mx+8,200)],fill=(143,112,77))
  if frame=='G':
   d.polygon([(210,200),(200,155),(187,132),(172,130),(168,145),(185,160),(180,200)],fill=(145,115,78))
  if frame=='B': poly([(180,72),(160,51),(177,51),(182,26),(190,51),(210,45),(194,73)],(255,213,92))
  png(f'sprites/{code}{frame}0.png',im,(0,0))
# Original synthesized audio; no recordings or implied field authenticity.
sr=22050
for name,dur in [('rifle',.20),('pistol',.16),('reload',.7),('hit',.12),('call',.8),('ambient',8),('pickup',.4)]:
 samples=[]
 for i in range(int(sr*dur)):
  t=i/sr; noise=rng.uniform(-1,1)
  if name in ['rifle','pistol','hit']: v=(noise*.6+math.sin(2*math.pi*75*t)*.4)*math.exp(-t*30)
  elif name=='ambient': v=noise*.05+math.sin(2*math.pi*(3100+90*math.sin(t*3))*t)*.035*(.5+.5*math.sin(t*12))
  elif name=='reload': v=noise*.3 if (t<.07 or .38<t<.44 or .60<t<.65) else 0
  elif name=='call': v=math.sin(2*math.pi*(150+100*t)*t)*math.sin(math.pi*t/dur)*.35
  else: v=math.sin(2*math.pi*(600+500*t)*t)*math.exp(-t*9)*.4
  samples.append(int(max(-1,min(1,v)) * 24000))
 b=io.BytesIO()
 with wave.open(b,'wb') as f: f.setparams((1,2,sr,0,'NONE','not compressed')); f.writeframes(struct.pack('<'+'h'*len(samples),*samples))
 put('sounds/'+name+'.wav',b.getvalue()); registry.append(dict(path='sounds/'+name+'.wav',origin='synthèse originale tools/build.py',license='CC0-1.0',status='provisoire — pas un enregistrement de Guyane'))
# Standalone interface resources, no inherited Doom UI textures.
fontpath='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
from PIL import ImageFont
for name,label in [('M_DOOM','CRIQUE'),('M_NGAME','NOUVELLE MISSION'),('M_OPTION','OPTIONS'),('M_LOADG','CHARGER'),('M_SAVEG','SAUVEGARDER'),('M_QUITG','QUITTER'),('M_EPISOD','OPERATION'),('M_NEWG','NOUVELLE MISSION'),('M_SKILL','DIFFICULTE')]:
 font=ImageFont.truetype(fontpath,28 if name=='M_DOOM' else 13)
 box=font.getbbox(label); im=Image.new('RGBA',(box[2]+6,box[3]+6)); ImageDraw.Draw(im).text((3,0),label,font=font,fill=(196,215,175)); png('graphics/'+name+'.png',im)
for name in ['M_SKULL1','M_SKULL2']:
 im=Image.new('RGBA',(12,12)); ImageDraw.Draw(im).polygon([(0,0),(11,6),(0,11)],fill=(116,203,162)); png('graphics/'+name+'.png',im)
for name in ['CONBACK','TITLEPIC']:
 im=Image.new('RGB',(640,360),(16,32,27)); d=ImageDraw.Draw(im)
 for i in range(90):
  x=rng.randrange(640); d.line((x,360,x+rng.randrange(-25,26),0),fill=(24,43,33),width=rng.randrange(3,16))
 if name=='TITLEPIC':
  d.text((58,95),'CRIQUE',font=ImageFont.truetype(fontpath,64),fill=(204,214,178)); d.text((64,179),'OPERATION LISIERE / PROTOTYPE 0.1',font=ImageFont.truetype(fontpath,18),fill=(127,174,145)); d.text((64,280),'ENTREE : MENU  /  RECUPERER PUIS EXTRAIRE',font=ImageFont.truetype(fontpath,15),fill=(177,189,165))
 png('graphics/'+name+'.png',im)
for name in ['F_SKY1','brdr_b','brdr_t','brdr_l','brdr_r','brdr_tl','brdr_tr','brdr_bl','brdr_br']:
 png('textures/'+name+'.png',Image.new('RGB',(8,8),(20,36,30)))
# Original palette ensures standalone software compatibility.
put('PLAYPAL',bytes([c for i in range(256) for c in (i,i,i)]))
put('CRIQUEID','CRIQUE prototype 0.1')
# UDMF grid with a central massif separating two approaches, camp and return loop.
C=256; cells={}
for x in range(17):
 for y in range(25):
  valid=(y<4 and 5<=x<=11) or (3<=y<=18 and (3<=x<=5 or 11<=x<=13)) or (17<=y<=23 and 3<=x<=13) or (y in range(3,6) and 3<=x<=13)
  if valid: cells[x,y]=len(cells)
# roofed shed north of camp
verts=[]; vid={}; sides=[]; lines=[]; sectors=[]
def vertex(p):
 if p not in vid: vid[p]=len(verts); verts.append(p)
 return vid[p]
def side(sec,tex='-'):
 sides.append(f'sidedef {{ sector={sec}; texturemiddle="{tex}"; texturetop="WOOD"; texturebottom="MUD"; }}'); return len(sides)-1
edges={}
for (x,y),sec in cells.items():
 water=y<=1; shed=7<=x<=10 and y>=21
 sectors.append(f'sector {{ heightfloor={-16 if water else 0}; heightceiling={112 if shed else 512}; texturefloor="{"WATER" if water else "WOOD" if shed else "MUD" if y<5 or y>17 else "LEAF"}"; textureceiling="{"ROOF" if shed else "F_SKY1"}"; lightlevel={140 if shed else 165 if y>17 else 142}; }}')
 pts=[(x*C,y*C),(x*C,(y+1)*C),((x+1)*C,(y+1)*C),((x+1)*C,y*C)]
 for a,b in zip(pts,pts[1:]+pts[:1]):
  key=tuple(sorted((a,b)))
  if key in edges:
   li,prev=edges[key]; lines[li]['back']=side(sec); lines[li]['two']=True; sides[lines[li]['front']]=sides[lines[li]['front']].replace('texturemiddle="BARK"','texturemiddle="-"')
  else:
   edges[key]=(len(lines),sec); lines.append(dict(a=vertex(a),b=vertex(b),front=side(sec,'BARK'),back=-1,two=False))
text=['namespace="ZDoom";']
text += [f'vertex {{ x={x}; y={y}; }}' for x,y in verts]; text+=sectors; text+=sides
for l in lines:
 text.append(f'linedef {{ v1={l["a"]}; v2={l["b"]}; sidefront={l["front"]};'+(f' sideback={l["back"]}; twosided=true;' if l['two'] else ' blocking=true;')+' }')
things=[]
def thing(x,y,typ,angle=0): things.append(f'thing {{ x={x}; y={y}; type={typ}; angle={angle}; skill1=true; skill2=true; skill3=true; skill4=true; skill5=true; single=true; }}')
thing(8.5*C,2.7*C,1,90); thing(8*C,0.8*C,15010);
for x,y in [(6,19),(9,20),(7,22),(10,23)]: thing(x*C+50,y*C+50,15009)
thing(8.5*C,1.5*C,15004); thing(8.4*C,22.3*C,15003)
for x,y,a in [(4,8,270),(4.8,13,90),(12,9,270),(12.8,16,90),(5,19,0),(12,19,180),(7,22,270),(10,22,270)]: thing(x*C,y*C,15001,a)
for x,y in [(3.8,16),(11.8,13),(6.5,20.2),(10,18.5)]: thing(x*C,y*C,15002,270)
for (x,y) in cells:
 if y<3: continue
 for j in range(2 if y<18 else 1):
  # keep clear lanes; edge planting avoids corridor-filling billboards.
  px=x*C+rng.choice([38,218]); py=y*C+rng.randrange(38,218)
  if (x in [3,5,11,13] or y in [4,17,23]) and not (7<=x<=10 and y>=21): thing(px,py,15006 if min(abs(py-1152),abs(py-4992))<72 else 15005)
  elif rng.random()<.55: thing(px,py,15006)
for x,y in [(4.5,6),(12.5,7),(4.5,17),(11.5,20),(8,21)]: thing(x*C,y*C,15007); thing(x*C+60,y*C,15008)
text+=things
# Write map wad with TEXTMAP/ENDMAP; UZDoom builds nodes on load.
lumps=[('MAP01',b''),('TEXTMAP','\n'.join(text).encode()),('ENDMAP',b'')]; data=b''; directory=b''
for n,b in lumps: directory+=struct.pack('<ii8s',12+len(data),len(b),n.encode().ljust(8,b'\0')); data+=b
put('maps/MAP01.wad',b'PWAD'+struct.pack('<ii',len(lumps),12+len(data))+data+directory)
for p in (ROOT/'src').rglob('*'):
 if p.is_file() and p.suffix not in ['.blend','.blend1']: put(str(p.relative_to(ROOT/'src')),p.read_bytes())
with zipfile.ZipFile(ROOT/'dist/crique.ipk3','w',zipfile.ZIP_DEFLATED) as z:
 for n,b in sorted(files.items()):
  zi=zipfile.ZipInfo(n,(2026,1,1,0,0,0)); zi.compress_type=zipfile.ZIP_DEFLATED; z.writestr(zi,b)
registry.extend(json.loads((ROOT/'reports/blender-props.json').read_text()))
(ROOT/'docs/assets.json').write_text(json.dumps(registry,ensure_ascii=False,indent=2))
(ROOT/'reports/build.json').write_text(json.dumps(dict(cells=len(cells),linedefs=len(lines),things=len(things),files=len(files),sha256=hashlib.sha256((ROOT/'dist/crique.ipk3').read_bytes()).hexdigest()),indent=2))
print((ROOT/'reports/build.json').read_text())
