"""Original low-poly props. Blender 4.3; export OBJ with Y up, UVs, origin at feet."""
import bpy,math,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]; out=R/'src/models';out.mkdir(exist_ok=True)
def reset(): bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
def box(loc,scale):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.scale=scale;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);return o
def export(name):
 bpy.ops.object.select_all(action='SELECT');bpy.ops.object.join();o=bpy.context.object
 bpy.context.view_layer.objects.active=o;bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
 bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.uv.smart_project(island_margin=.03);bpy.ops.object.mode_set(mode='OBJECT')
 bpy.ops.wm.save_as_mainfile(filepath=str(out/(name+'.blend')))
 # Explicit stable triangulated OBJ export from Blender's actual evaluated mesh.
 mesh=o.data;mesh.calc_loop_triangles();ls=['# Original Blender mesh; CC0-1.0']
 for v in mesh.vertices:ls.append('v %.6f %.6f %.6f'%(v.co.x,v.co.z,-v.co.y))
 uv=mesh.uv_layers.active.data
 for lp in mesh.loops:ls.append('vt %.6f %.6f'%(uv[lp.index].uv.x,uv[lp.index].uv.y))
 for t in mesh.loop_triangles:ls.append('f '+' '.join('%d/%d'%(mesh.loops[l].vertex_index+1,l+1) for l in t.loops))
 (out/(name+'.obj')).write_text('\n'.join(ls))
 return dict(name=name,vertices=len(mesh.vertices),triangles=len(mesh.loop_triangles),origin='base z=0',scale='map units: player 56',uv=True,license='CC0-1.0',status='prototype; collision actor simplifiee')
stats=[];reset();box((0,0,20),(56,44,40))
for x in [-29,29]:
 for y in [-23,23]:box((x,y,20),(4,4,44))
for z in [5,35]:box((0,-24,z),(64,3,4));box((0,24,z),(64,3,4))
stats.append(export('crate'))
reset()
# River boat hull: hollow shell assembled from low-poly panels; no people represented.
box((0,0,4),(150,44,8));box((0,-26,16),(156,5,28));box((0,26,16),(156,5,28))
for x in [-53,0,53]:box((x,0,23),(14,48,5))
for x in [-78,78]:box((x,0,13),(5,52,24))
stats.append(export('boat'))
(R/'reports/blender-props.json').write_text(json.dumps(stats,indent=2))
