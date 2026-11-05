import json,subprocess,sys,tempfile
from pathlib import Path
SKILL=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as td:
 root=Path(td)/'project';root.mkdir();(root/'package.json').write_text('{"name":"demo"}')
 out=Path(td)/'docs';out.mkdir()
 subprocess.run([sys.executable,str(SKILL/'scripts/inventory.py'),'--root',str(root),'--out',str(out/'inventory.json')],check=True)
 data=json.loads((out/'inventory.json').read_text());assert 'package.json' in data['manifest_paths']
 (out/'00_auditoria.md').write_text('# Auditoria\n\n'+('Inventário técnico preliminar com evidência: package.json. '*5),encoding='utf-8')
 subprocess.run([sys.executable,str(SKILL/'scripts/build_documents.py'),'--input',str(out),'--output',str(out/'pdf')],check=True)
 subprocess.run([sys.executable,str(SKILL/'scripts/validate_output.py'),'--dir',str(out),'--mode','auditoria'],check=True)
 print('SMOKE PASS')
