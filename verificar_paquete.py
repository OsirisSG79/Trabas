from pathlib import Path
import hashlib, json
root=Path(__file__).resolve().parent
manifest=json.loads((root/'MANIFIESTO_SHA256.json').read_text(encoding='utf-8'))
bad=[]
for name, expected in manifest.items():
 p=root/name
 if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=expected: bad.append(name)
print('Archivos verificados:',len(manifest),'Errores:',len(bad))
for name in bad: print(name)
raise SystemExit(bool(bad))
