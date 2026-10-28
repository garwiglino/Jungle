from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
r=Path(__file__).resolve().parents[1];(r/'build').mkdir(exist_ok=True)
with ZipFile(r/'build/tests.pk3','w',ZIP_DEFLATED) as z:z.write(r/'tests/ZSCRIPT','ZSCRIPT')
print(r/'build/tests.pk3')
