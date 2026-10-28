"""Single anatomical source -> one arm mesh -> physically coherent turnaround.
Source: MakeHuman base.obj (CC0); source license bundled beside OBJ.
"""
import bpy,math,json,sys
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[1]/'art/arm-anatomy-local';R.mkdir(exist_ok=True)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
vs=[];groups={};faces=[];group=''
for line in (R/'source/base.obj').read_text().splitlines():
 p=line.split()
 if not p:continue
 if p[0]=='v':vs.append(Vector(tuple(map(float,p[1:4]))))
 elif p[0]=='g':group=p[1];groups.setdefault(group,set())
 elif p[0]=='f':
  face=[int(x.split('/')[0])-1 for x in p[1:]];groups[group].update(face)
  if group=='body':faces.append(face)
def joint(n):
 inds=groups['joint-r-'+n];return sum((vs[i] for i in inds),Vector())/len(inds)
S,E,W=joint('shoulder'),joint('elbow'),joint('hand');F=joint('finger-3-4');U=(E-S).normalized();V=(W-E).normalized()
q=V.rotation_difference(U);qglobal=U.rotation_difference(Vector((0,0,-1)))
def distance(p,a,b):
 v=b-a;t=max(0,min(1,(p-a).dot(v)/v.length_squared));return (p-(a+t*v)).length
HC=(W+F)/2
keep=set()
for i in groups['body']:
 p=vs[i]
 if (p-S).dot(U)<-.20:continue
 if min(distance(p,S,E)/.87,distance(p,E,W)/.76,(p-HC).length/1.25)<1:keep.add(i)
# Connected component nearest the hand excludes neighboring torso pieces.
ff=[f for f in faces if all(i in keep for i in f)];adj={i:set() for f in ff for i in f}
for f in ff:
 for a,b in zip(f,f[1:]+f[:1]):adj[a].add(b);adj[b].add(a)
seed=min(adj,key=lambda i:(vs[i]-W).length);component={seed};todo=[seed]
while todo:
 for n in adj[todo.pop()]:
  if n not in component:component.add(n);todo.append(n)
ff=[f for f in ff if all(i in component for i in f)];ids=sorted(component);remap={old:new for new,old in enumerate(ids)}
def unbend(p):
 d=(p-E).dot(V);t=max(0,min(1,d/.45));t=t*t*(3-2*t)
 # The distal forearm and entire hand rotate together; no mirroring.
 return p.lerp(E+q@(p-E),t)
def transform(p):return qglobal@(unbend(p)-S)*.12+Vector((0,0,.68))
points=[transform(vs[i]) for i in ids]
mesh=bpy.data.meshes.new('MakeHuman right arm anatomical mesh');mesh.from_pydata(points,[],[[remap[i] for i in f] for f in ff if max(transform(vs[i]).z for i in f)<transform(W).z+.045]);mesh.update();arm=bpy.data.objects.new('RIGHT arm, one anatomical source',mesh);bpy.context.collection.objects.link(arm)
for p in mesh.polygons:p.use_smooth=True
mod=arm.modifiers.new('smooth anatomical surface','SUBSURF');mod.levels=2;mod.render_levels=2
# Materials: physically shared by all camera views.
def material(name,color,rough=.7):
 m=bpy.data.materials.new(name);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Roughness'].default_value=rough;return m
skin=material('skin',(.39,.20,.11),.68);n=skin.node_tree.nodes;l=skin.node_tree.links;p=n.get('Principled BSDF');p.inputs['Subsurface Weight'].default_value=.08
noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=240;bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.15;bump.inputs['Distance'].default_value=.0005;l.new(noise.outputs['Fac'],bump.inputs['Height']);l.new(bump.outputs['Normal'],p.inputs['Normal']);arm.data.materials.append(skin)
# Derive transverse axes from the actual right hand. This fixes handedness once.
thumb=transform(joint('finger-1-3'));little=transform(joint('finger-5-1'));tv=thumb-little;tv.z=0;T=tv.normalized();N=Vector((T.y,-T.x,0))
# T is screen-right in the dorsal view, hence right thumb appears picture-right.
newE=transform(E);newW=transform(W);newS=Vector((0,0,.68));length=.68-newW.z
cloth=material('Tiger Stripe cotton',(.12,.16,.06),.95);n=cloth.node_tree.nodes;l=cloth.node_tree.links;p=n.get('Principled BSDF')
# Real fabric artwork used as a surface texture; no anatomy inferred by image generation.
img=bpy.data.images.load(str(R/'source/tigerstripe-tile.png'));tex=n.new('ShaderNodeTexImage');tex.image=img;tex.extension='REPEAT';uv=n.new('ShaderNodeTexCoord');mapping=n.new('ShaderNodeVectorMath');mapping.operation='MULTIPLY';mapping.inputs[1].default_value=(1,1,1);l.new(uv.outputs['UV'],mapping.inputs[0]);l.new(mapping.outputs[0],tex.inputs[0]);l.new(tex.outputs['Color'],p.inputs['Base Color'])
noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=500;bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.14;bump.inputs['Distance'].default_value=.0004;l.new(noise.outputs['Fac'],bump.inputs['Height']);l.new(bump.outputs['Normal'],p.inputs['Normal'])
def sleeve(name,z0,z1,radius_function,mat,rows=90):
 verts=[];quads=[];segments=64
 for j in range(rows+1):
  t=j/rows;z=z0+(z1-z0)*t;rad=radius_function(t)
  for k in range(segments):
   a=k*2*math.pi/segments;rr=rad*(1+.035*math.cos(5*a+t*4)+.02*math.sin(11*a-t*9))
   verts.append(tuple((T*math.cos(a)+N*math.sin(a))*rr+Vector((0,0,z))))
 for j in range(rows):
  for k in range(segments):
   a=j*segments+k;b=j*segments+(k+1)%segments;quads.append((a,b,b+segments,a+segments))
 quads.append(tuple(reversed(range(segments))));quads.append(tuple(rows*segments+k for k in range(segments)))
 me=bpy.data.meshes.new(name);me.from_pydata(verts,[],quads);me.update();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);o.data.materials.append(mat)
 uv=me.uv_layers.new()
 for poly in me.polygons:
  for li in poly.loop_indices:
   vi=me.loops[li].vertex_index;j,k=divmod(vi,segments);u=k/segments
   if any(me.loops[x].vertex_index%segments==0 for x in poly.loop_indices) and k==segments-1:u=-1/segments
   uv.data[li].uv=(u,j/rows)
  poly.use_smooth=True
 mod=o.modifiers.new('fabric thickness','SOLIDIFY');mod.thickness=.0015;sub=o.modifiers.new('fabric surface','SUBSURF');sub.levels=1;sub.render_levels=1
 return o
wz=newW.z+.012;top=.695
# Fit roomy cotton sleeve around a single anatomical limb, with elbow and cuff folds.
def radius(t):
 z=top+(wz-top)*t
 if t<.14:base=.004+.077*math.sin(t/.14*math.pi/2)
 elif t<.45:base=.081-(t-.14)*.05
 else:base=.066-(t-.45)*.035
 elbow=math.exp(-((z-newE.z)/.06)**2);wrist=math.exp(-((t-.90)/.09)**2)
 return base +.003*math.sin(t*55)*elbow+.003*math.sin(t*120)*wrist
sleeve('one continuous loose sleeve',top,wz+.035,radius,cloth)
sleeve('one cuff',wz+.037,wz-.012,lambda t:.047,cloth,10)
# One cuff button on the radial/thumb surface, never duplicated for a camera.
bpy.ops.mesh.primitive_uv_sphere_add(segments=16,ring_count=8,location=T*.049+Vector((0,0,wz+.011)));button=bpy.context.object;button.name='single radial cuff button';button.scale=(.007,.007,.0025);button.rotation_euler=Vector(T).to_track_quat('Z','Y').to_euler();button.data.materials.append(material('button',(.025,.03,.018)))
# Small nail surfaces follow the actual source finger joints and right-hand normal.
nailmat=material('natural nails',(.48,.29,.19),.48)
for finger in range(1,6):
 a=transform(joint('finger-%d-3'%finger));b=transform(joint('finger-%d-4'%finger));d=(b-a).normalized();normal=T if finger==1 else N
 c=a.lerp(b,.45);near=[v for v in points if (v-c).length<.018]
 if near:
  depth=max(v.dot(normal) for v in near);c+=normal*(depth-c.dot(normal)+.0004)
 right=normal.cross(d).normalized();forward=right.cross(normal).normalized();verts=[]
 for k in range(12):
  angle=k*2*math.pi/12;verts.append(tuple(c+right*.0045*math.cos(angle)+forward*.006*math.sin(angle)))
 me=bpy.data.meshes.new('nail');me.from_pydata(verts,[],[tuple(range(12))]);me.update();o=bpy.data.objects.new('nail %d'%finger,me);bpy.context.collection.objects.link(o);o.data.materials.append(nailmat)
# Fixed scene; only camera rotates. No regenerated views.
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=48;scene.cycles.use_denoising=False;scene.render.resolution_x=768;scene.render.resolution_y=1152;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=False
scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.42,.42,.42,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.65;scene.view_settings.view_transform='Standard'
for name,loc,power,size in [('key',(-1,-1,1.4),45,1.7),('fill',(1,-.5,1),20,1.5),('rim',(0,1,1.1),25,1.4)]:
 bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.name=name;o.data.energy=power;o.data.size=size;o.rotation_euler=(Vector((0,0,.35))-o.location).to_track_quat('-Z','Y').to_euler()
minz=min(v.z for v in points);center=Vector((0,0,(top+minz)/2));height=top-minz
bpy.ops.object.camera_add();cam=bpy.context.object;cam.data.type='ORTHO';cam.data.ortho_scale=height*1.13;scene.camera=cam
out=R/'renders';out.mkdir(exist_ok=True);bpy.ops.wm.save_as_mainfile(filepath=str(R/'right-arm-turnaround.blend'))
views=[('01-dos',0),('02-profil-pouce',90),('03-paume',180),('04-profil-externe',270),('05-trois-quarts',45)]
if '--test-only' in sys.argv:views=views[:1]
for name,deg in views:
 a=math.radians(deg);direction=N*math.cos(a)+T*math.sin(a);cam.location=center+direction*2;cam.rotation_euler=(center-cam.location).to_track_quat('-Z','Y').to_euler();scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True)
(R/'provenance.json').write_text(json.dumps({'mesh':'MakeHuman base.obj CC0, right arm extracted without reflection','source':'https://github.com/makehumancommunity/makehuman/blob/master/makehuman/data/3dobjs/base.obj','same_geometry_all_views':True,'same_texture_all_views':True,'views':views,'vertices':len(points),'faces':len(ff),'dorsal_camera_normal':list(N),'thumb_direction':list(T),'status':'anatomical blockout with provisional garment and material finish'},indent=2))
