"""Original nonfunctional game prop. Model geometry fixes the grip/hand relationship.
All first-person output is pre-rendered PNG sprites, never an in-engine weapon model.
"""
import bpy,math,json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
def mat(name,color,metal=0,rough=.7):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=rough;return m
steel=mat('parkerized steel',(.045,.055,.05),.65,.72);edge=mat('steel highlight',(.105,.12,.11),.65,.66);black=mat('dark grip panels',(.035,.038,.027),.1,.82);skin=mat('hands',(.24,.115,.055),0,.72);nail=mat('subtle knuckles',(.29,.15,.075));inside=mat('dark recess',(.01,.014,.011));flashmat=mat('muzzle flash',(.95,.43,.08));flashmat.node_tree.nodes.get('Principled BSDF').inputs['Emission Color'].default_value=(1,.45,.08,1);flashmat.node_tree.nodes.get('Principled BSDF').inputs['Emission Strength'].default_value=3
camo=mat('original procedural Tiger Stripe',(.13,.17,.07),0,.95)
n=camo.node_tree.nodes;l=camo.node_tree.links;p=n.get('Principled BSDF');tex=n.new('ShaderNodeTexWave');tex.wave_type='BANDS';tex.bands_direction='Z';tex.inputs['Scale'].default_value=3.8;tex.inputs['Distortion'].default_value=9;tex.inputs['Detail Scale'].default_value=2.2;tex.inputs['Detail'].default_value=4
ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.interpolation='CONSTANT';ramp.color_ramp.elements.remove(ramp.color_ramp.elements[1]);ramp.color_ramp.elements[0].position=0;ramp.color_ramp.elements[0].color=(.025,.028,.015,1)
for pos,col in [(.19,(.065,.035,.015,1)),(.36,(.085,.115,.045,1)),(.72,(.20,.17,.085,1)),(.84,(.045,.075,.025,1))]: e=ramp.color_ramp.elements.new(pos);e.color=col
l.new(tex.outputs['Fac'],ramp.inputs[0]);l.new(ramp.outputs['Color'],p.inputs['Base Color'])
noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=170;bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.12;bump.inputs['Distance'].default_value=.002;l.new(noise.outputs['Fac'],bump.inputs['Height']);l.new(bump.outputs['Normal'],p.inputs['Normal'])
def group(name,parent=None):
 o=bpy.data.objects.new(name,None);bpy.context.collection.objects.link(o);o.parent=parent;return o
root=group('weapon pose');left=group('left support hand',root);mag=group('magazine',root)
def finish(o,name,material,parent=root,bevel=0):
 o.name=name;o.data.materials.append(material);o.parent=parent
 if bevel:
  mod=o.modifiers.new('manufactured edges','BEVEL');mod.width=bevel;mod.segments=2;o.modifiers.new('weighted corners','WEIGHTED_NORMAL')
 return o
def box(name,loc,scale,material=steel,parent=root,bevel=.003):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.scale=scale;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);return finish(o,name,material,parent,bevel)
def ball(name,loc,scale,material=skin,parent=root):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=16,ring_count=10,location=loc);o=bpy.context.object;o.scale=scale;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);bpy.ops.object.shade_smooth();return finish(o,name,material,parent)
def segment(name,a,b,radius,material,parent=root,r2=None):
 a,b=Vector(a),Vector(b);d=b-a
 bpy.ops.mesh.primitive_cone_add(vertices=20,radius1=radius,radius2=radius if r2 is None else r2,depth=d.length,location=(a+b)/2);o=bpy.context.object;o.rotation_euler=d.to_track_quat('Z','Y').to_euler();return finish(o,name,material,parent,.001)
def tube(name,pts,radius,material=steel,parent=root):
 c=bpy.data.curves.new(name,'CURVE');c.dimensions='3D';c.bevel_depth=radius;c.bevel_resolution=2;s=c.splines.new('POLY');s.points.add(len(pts)-1)
 for p,v in zip(s.points,pts):p.co=(*v,1)
 o=bpy.data.objects.new(name,c);bpy.context.collection.objects.link(o);o.data.materials.append(material);o.parent=parent;return o
# Stylized external prop geometry only, without functional internal mechanism.
box('stamped receiver',(0,.075,.015),(.105,.38,.105))
box('top stamped cover',(0,.045,.072),(.094,.30,.012),edge)
box('rear plate',(0,-.122,.015),(.114,.025,.112),steel)
# Grip is attached BELOW rear receiver. It never projects from a side wall.
grip=box('pistol grip UNDER receiver',(0,-.105,-.105),(.055,.085,.17),black);grip.rotation_euler.x=math.radians(-12)
box('grip attachment underside',(0,-.09,-.046),(.058,.07,.025))
tube('trigger guard underside',[(0,-.045,-.045),(0,.025,-.06),(0,.02,-.105),(0,-.06,-.12)],.005)
box('forward magazine housing',(0,.18,-.055),(.066,.085,.08))
box('straight magazine',(0,.18,-.215),(.043,.062,.26),black,mag)
box('magazine base',(0,.18,-.348),(.053,.07,.012),steel,mag)
# Barrel shroud represented by separated metal rings and ribs, actual open gaps.
segment('inner barrel',(0,.25,.018),(0,.53,.018),.016,black)
for i in range(6):segment('shroud band '+str(i),(0,.255+i*.038,.018),(0,.272+i*.038,.018),.039,steel)
for x,z in [(-.03,.018),(.03,.018),(0,-.012)]:box('shroud rib',(x,.365,z),(.012,.24,.012))
segment('muzzle lip',(0,.50,.018),(0,.535,.018),.025,edge)
box('front post',(0,.48,.071),(.008,.015,.035),black)
for x in [-.028,.028]:box('front sight ear',(x,.48,.071),(.009,.022,.05),steel)
box('rear sight base',(0,-.045,.086),(.055,.032,.014),black)
for x in [-.022,.022]:box('rear sight ear',(x,-.045,.103),(.008,.02,.032),steel)
box('right ejection recess',(.053,.11,.022),(.002,.065,.035),inside,bevel=0)
for x in [-.04,.04]:segment('retracted wire stock',(x,-.16,-.015),(x,.13,-.015),.005,edge)
# Right hand wraps around vertical pistol grip from below; receiver sides remain bare.
ball('right palm beneath receiver',(.025,-.13,-.12),(.034,.047,.045))
ball('right thumb under rear',(.033,-.079,-.065),(.018,.041,.018))
for i in range(4):
 z=-.087-i*.024
 segment('right finger '+str(i),(.04,-.068,z),(-.023,-.062,z),.012,skin)
 ball('right knuckle '+str(i),(.042,-.068,z),(.014,.015,.013),nail)
# Connected phalanges at the visible outer grip edge make the grip readable.
for i in range(3):
 z=-.11-i*.021
 ball('visible curled finger '+str(i),(.033,-.155,z),(.022,.014,.011),skin)
# Skin grain is procedural, independent of any generated source image.
for material in [skin,nail]:
 nodes=material.node_tree.nodes;links=material.node_tree.links;shader=nodes.get('Principled BSDF')
 noise=nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=110
 bump=nodes.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.10;bump.inputs['Distance'].default_value=.001
 links.new(noise.outputs['Fac'],bump.inputs['Height']);links.new(bump.outputs['Normal'],shader.inputs['Normal'])
# Index finger rests along lower trigger-guard area in idle, not on receiver wall.
segment('right index idle',(.044,-.055,-.067),(.026,.009,-.07),.010,skin)
segment('right wrist',(.05,-.16,-.15),(.115,-.26,-.10),.031,skin)
segment('right Tiger Stripe sleeve',(.115,-.26,-.10),(.40,-.56,-.18),.045,camo,r2=.105)
segment('right cuff',(.105,-.248,-.107),(.13,-.277,-.092),.048,camo)
# Support hand encloses magazine housing BELOW the forward receiver.
ball('left palm under magwell',(-.035,.16,-.105),(.04,.052,.05),skin,left)
for i in range(4):
 z=-.075-i*.021;segment('left finger '+str(i),(-.052,.205,z),(.025,.208,z),.011,skin,left)
segment('left thumb',(-.048,.14,-.07),(-.025,.12,-.051),.014,skin,left)
segment('left wrist',(-.07,.13,-.13),(-.12,-.04,-.12),.032,skin,left)
segment('left Tiger Stripe sleeve',(-.12,-.04,-.12),(-.42,-.52,-.18),.047,camo,left,r2=.11)
segment('left cuff',(-.116,-.028,-.12),(-.135,-.066,-.112),.05,camo,left)
# Fine steel finish for a readable retro sprite rather than flat default shading.
for material in [steel,edge]:
 nodes=material.node_tree.nodes;links=material.node_tree.links;shader=nodes.get('Principled BSDF')
 noise=nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=100;noise.inputs['Detail'].default_value=2
 bump=nodes.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.14;bump.inputs['Distance'].default_value=.001
 links.new(noise.outputs['Fac'],bump.inputs['Height']);links.new(bump.outputs['Normal'],shader.inputs['Normal'])
# Muzzle flash is a separate rendered state, hidden for idle.
flash=segment('flash',(0,.54,.018),(0,.69,.018),.055,flashmat,r2=.002);flash.hide_render=True
bpy.ops.object.camera_add(location=(0,-.85,.28));cam=bpy.context.object;cam.name='centered first person camera';target=Vector((0,.45,.08));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=24;cam.data.clip_start=.015;bpy.context.scene.camera=cam
for name,loc,energy,size in [('key',(-1,-.5,1.4),45,1.5),('fill',(.8,-.5,.8),18,1.2),('rim',(0,1,1),30,1)]:
 bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.name=name;o.data.energy=energy;o.data.shape='DISK';o.data.size=size;o.rotation_euler=(Vector((0,.1,0))-o.location).to_track_quat('-Z','Y').to_euler()
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=64;s.cycles.use_denoising=False;s.render.resolution_x=640;s.render.resolution_y=400;s.render.resolution_percentage=100;s.render.film_transparent=True;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA';s.world.color=(.2,.2,.2);s.view_settings.view_transform='Standard';s.view_settings.look='Medium High Contrast'
bpy.ops.wm.save_as_mainfile(filepath=str(R/'mat49-pose.blend'))
frames='A' if '--idle-only' in __import__('sys').argv else 'ABCDEFGH'
for f in frames:
 root.location=(0,0,0);root.rotation_euler=(0,0,0);left.location=(0,0,0);mag.location=(0,0,0);flash.hide_render=True
 if f=='B':flash.hide_render=False;root.rotation_euler.x=math.radians(2)
 if f=='C':root.rotation_euler.x=math.radians(5);root.location.y=-.02
 if f in 'DEFGH':
  root.rotation_euler.x=math.radians(-{'D':6,'E':9,'F':9,'G':4,'H':2}[f]);root.location.z=-.015
 if f=='E':left.location=(0,-.04,-.13);mag.location=(0,-.04,-.13)
 if f=='F':left.location=(0,0,-.065);mag.location=(0,0,-.065)
 s.render.filepath=str(R/('MAT4'+f+'0-source.png'));bpy.ops.render.render(write_still=True)
(R/'geometry-check.json').write_text(json.dumps({'origin':'original Blender scene, no generative image retouch','grip':'under receiver at x=0, y=-0.105, z=-0.105','right_palm':'under receiver at x=0.025, y=-0.13, z=-0.12','rendered_frames':frames,'runtime_weapon_model':False,'status':'stylized game prop; historical details not certified'},indent=2))
