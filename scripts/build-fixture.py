"""Build and sign the small real receipt-helper release. Never persists private keys."""
import hashlib
import json
import pathlib
import subprocess
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
ROOT = pathlib.Path(__file__).resolve().parents[1]
canon = lambda x: json.dumps(x, sort_keys=True, separators=(',', ':'), ensure_ascii=True)
sha = lambda x: hashlib.sha256(x).hexdigest()
source = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
# Read committed inputs, not dirty working-tree files.
def committed(path):
    return subprocess.check_output(['git', 'show', source + ':' + path], cwd=ROOT)
manifest = committed('fixtures/manifest.json')
procedure = committed('fixtures/procedure.txt')
artifact = committed('src/canonical.mjs').replace(b'\r\n', b'\n')
(ROOT/'fixtures/artifact.mjs').write_bytes(artifact)
key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
claim = {'schema':'releaseorigin/v1','repository':'ANZA24k/ReleaseOrigin','source_commit':source,'version':json.loads(manifest)['version'],'artifact_sha256':sha(artifact),'manifest_sha256':sha(manifest),'procedure_sha256':sha(procedure),'builder_rsa_n':format(key.public_key().public_numbers().n, '0512x'),'exception_policy':''}
payload = {k:v for k,v in claim.items() if k not in ('builder_rsa_n','exception_policy')}
payload.update(build_description='Read src/canonical.mjs at the declared source commit, normalized CRLF to LF, and wrote the unchanged remaining UTF-8 bytes to fixtures/artifact.mjs. Computed SHA-256 for the artifact, manifest and procedure, and recorded the source commit and manifest version. The dependencies object is empty. No compilation, network installation or minification was performed.',exceptions='')
message = b'ReleaseOrigin attestation v1\x00' + canon(payload).encode()
signature = key.sign(message, padding.PKCS1v15(), hashes.SHA256()).hex()
(ROOT/'fixtures/attestation.json').write_text(canon({'payload':payload,'signature':signature})+'\n')
(ROOT/'fixtures/claim.json').write_text(canon(claim)+'\n')
print('Built and signed receipt helper from source commit', source)
