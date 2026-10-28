"""Export corrected Blender renders; the previous generated pose is archived in legacy/."""
from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).resolve().parent/'blender/export_sprites.py'),run_name='__main__')
