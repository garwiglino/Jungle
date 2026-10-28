"""Blender: render a single imported GLB from fixed orthographic cameras.
Usage: blender -b -t 4 --python tools/render_arm_turnaround.py -- mesh.glb output_dir
No generative image modification occurs between the views.
"""
import bpy,sys,math,json
from pathlib import Path
from mathutils import Vector
args=sys.argv[sys.argv.index('--')+1:]
if len(args)<2:raise SystemExit('Expected model.glb output_dir')
model=Path(args[0]).resolve();out=Path(args[1]).resolve();out.mkdir(parents=True,exist_ok=True)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
bpy.ops.import_scene.gltf(filepath=str(model))
meshes=[o for o in bpy.context.scene.objects if o.type=='MESH']
if not meshes:raise RuntimeError('No mesh in input')
root=bpy.data.objects.new('shared source model',None);bpy.context.collection.objects.link(root)
for o in list(bpy.context.scene.objects):
 if o!=root and o.parent is None:o.parent=root
bpy.context.view_layer.update()
def bounds():
 pts=[o.matrix_world @ Vector(v) for o in meshes for v in o.bound_box]
 return Vector(tuple(min(p[i] for p in pts) for i in range(3))),Vector(tuple(max(p[i] for p in pts) for i in range(3)))
lo,hi=bounds();dims=hi-lo;axis=max(range(3),key=lambda i:dims[i])
if axis==0:root.rotation_euler.y=-math.pi/2
elif axis==1:root.rotation_euler.x=math.pi/2
bpy.context.view_layer.update();lo,hi=bounds();center=(lo+hi)/2;root.location=-center
bpy.context.view_layer.update();lo,hi=bounds();height=hi.z-lo.z
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=48;s.cycles.use_denoising=False
s.render.resolution_x=1024;s.render.resolution_y=1536;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB';s.render.film_transparent=False
s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.42,.42,.42,1);s.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8
s.view_settings.view_transform='Standard'
for name,loc,power in [('key',(-2,-3,4),160),('fill',(3,-1,2),80),('rim',(1,3,3),100)]:
 bpy.ops.object.light_add(type='AREA',location=Vector(loc)*height);light=bpy.context.object;light.name=name;light.data.energy=power*height*height;light.data.size=height*3;light.rotation_euler=(-light.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add();cam=bpy.context.object;cam.data.type='ORTHO';cam.data.ortho_scale=height*1.16;cam.data.clip_start=max(height*.001,.0001);cam.data.clip_end=height*100;s.camera=cam
views=[('01-dos',0),('02-profil-pouce',90),('03-paume',180),('04-profil-externe',270),('05-trois-quarts',45)]
counts={'mesh_objects':len(meshes),'vertices':sum(len(o.data.vertices) for o in meshes),'polygons':sum(len(o.data.polygons) for o in meshes)}
bpy.ops.wm.save_as_mainfile(filepath=str(out/'turnaround-source.blend'))
for name,deg in views:
 a=math.radians(deg);cam.location=(math.sin(a)*height*4,-math.cos(a)*height*4,0);cam.rotation_euler=(-cam.location).to_track_quat('-Z','Y').to_euler()
 s.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True)
(out/'render-checks.json').write_text(json.dumps({'source':str(model),'same_geometry_for_every_view':True,'same_texture_for_every_view':True,'projection':'orthographic','scale':cam.data.ortho_scale,'resolution':[1024,1536],'angles':views,**counts},indent=2))
