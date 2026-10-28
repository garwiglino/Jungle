#!/usr/bin/env python3
"""Download pinned official engine, verify exact binary, extract without FUSE/root."""
from pathlib import Path
import hashlib,urllib.request,subprocess,shutil,os
R=Path(__file__).resolve().parents[1]; cache=R/'runtime';cache.mkdir(exist_ok=True)
version='5.0.3'; digest='9c5166febc09cbf80c24612a78829037c953f38c4d986e36f8475ddd507e0228'
engine=cache/'engine/usr/bin/uzdoom'
if engine.exists(): print(engine);raise SystemExit
archive=cache/'uzdoom.AppImage'
url=f'https://github.com/UZDoom/UZDoom/releases/download/{version}/Linux-UZDoom-Release-x86_64.AppImage'
if not archive.exists():
 print('Téléchargement UZDoom '+version,flush=True)
 with urllib.request.urlopen(url,timeout=90) as response,archive.open('wb') as f:shutil.copyfileobj(response,f)
if hashlib.sha256(archive.read_bytes()).hexdigest()!=digest:raise SystemExit('SHA256 incorrect : supprimer runtime/uzdoom.AppImage et recommencer.')
archive.chmod(0o755)
subprocess.run([str(archive),'--appimage-extract'],cwd=cache,check=True,stdout=subprocess.DEVNULL)
(cache/'squashfs-root').rename(cache/'engine')
# Keep core, exclude optional packages derived from commercial game graphics.
for name in ['game_support.pk3','game_widescreen_gfx.pk3','brightmaps.pk3','lights.pk3']:
 for path in (cache/'engine').rglob(name):path.unlink()
core=cache/'engine/usr/bin/uzdoom.pk3'
core.symlink_to('../share/games/uzdoom/uzdoom.pk3')
print(engine)
