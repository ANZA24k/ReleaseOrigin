"""Bind local fixtures to an already published immutable evidence commit."""
import hashlib
import json
import pathlib
import subprocess
ROOT = pathlib.Path(__file__).resolve().parents[1]
c = json.loads((ROOT/'fixtures/claim.json').read_text())
commit = subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
b = {}
for role, name in [('artifact','artifact.mjs'),('manifest','manifest.json'),('procedure','procedure.txt'),('attestation','attestation.json')]:
    ref = c['source_commit'] if role in ('manifest','procedure') else commit
    raw = subprocess.check_output(['git','show',ref+':fixtures/'+name],cwd=ROOT)
    b[role] = {'url':f"https://raw.githubusercontent.com/{c['repository']}/{ref}/fixtures/{name}",'body':raw.decode(),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
(ROOT/'fixtures/bundle.json').write_text(json.dumps(b,sort_keys=True,separators=(',',':'))+'\n')
print('Prepared evidence bundle at', commit)
