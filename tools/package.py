#!/usr/bin/env python3
"""Package source/game/review evidence, excluding engines and user configuration."""
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import json,hashlib,re
r=Path(__file__).resolve().parents[1]
log=(r/'reports/final-validation.log').read_text()
assert ']quit' in log, 'GUI test still running'
assert log.count('CRIQUE_TEST PASS')==4 and 'CRIQUE_TEST FAIL' not in log
assert not re.search('Script error|VM execution aborted|not found|Unknown texture',log)
states=[tuple(map(int,m)) for m in re.findall(r'CRIQUE_PROBE health=(\d+) recovered=(\d+) complete=(\d+) mag=(\d+) reserve=(\d+)',log)]
assert len(states)==8,states
assert states[1][3]<states[0][3] and states[2][3]==30 and states[2][4]<states[1][4],states
assert states[3][3]==11 and states[4][2]==0
assert states[5][1]==1 and states[5][1:]==states[6][1:]
assert states[-1][2]==1
ai=(r/'reports/launcher-audio.log').read_text();assert ai.count('CRIQUE_TEST PASS')==7 and 'CRIQUE_TEST FAIL' not in ai
with ZipFile(r/'saves/checkpoint.zds') as z:(r/'reports/save-info.json').write_text(json.dumps(json.loads(z.read('info.json')),indent=2))
selected=['VALIDATION.md','build.json','resource-validation.json','blender-props.json','blender.log','final-validation.log','launcher-audio.log','performance.log','benchmarks.txt','save-info.json','boat.png','crate.png','rifle-fired.png','rifle-reloaded.png','pistol-fired.png','objective.png','restored.png','extraction.png','death.png','performance-camp.png']
paths=[]
for folder in ['src','tools','docs','tests','LICENSES']:
 paths.extend(p for p in (r/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.blend1')
paths += [r/p for p in ['README.md','LICENSE','requirements.txt','lancer.sh','.gitignore','dist/crique.ipk3']]
paths += [r/'reports'/p for p in selected if (r/'reports'/p).exists()]
archive=r/'dist/CRIQUE-prototype-0.1.zip'
with ZipFile(archive,'w',ZIP_DEFLATED,compresslevel=9) as z:
 for p in sorted(paths):z.write(p,'crique/'+str(p.relative_to(r)))
with ZipFile(archive) as z:assert z.testzip() is None
summary=dict(archive=str(archive),bytes=archive.stat().st_size,sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),files=len(paths),checks='passed')
(r/'dist/package.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
