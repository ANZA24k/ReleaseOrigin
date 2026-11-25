import hashlib
import json
import pathlib
import unittest
from cryptography.hazmat.primitives.asymmetric import rsa,padding
from cryptography.hazmat.primitives import hashes
ROOT=pathlib.Path(__file__).resolve().parents[1]
class PublishedFixtureTests(unittest.TestCase):
    def test_real_artifact_and_signature(self):
        claim=json.loads((ROOT/'fixtures/claim.json').read_text())
        att=json.loads((ROOT/'fixtures/attestation.json').read_text())
        key=rsa.RSAPublicNumbers(65537,int(claim['builder_rsa_n'],16)).public_key()
        canon=json.dumps(att['payload'],sort_keys=True,separators=(',',':'),ensure_ascii=True).encode()
        key.verify(bytes.fromhex(att['signature']),b'ReleaseOrigin attestation v1\x00'+canon,padding.PKCS1v15(),hashes.SHA256())
        self.assertEqual((ROOT/'fixtures/artifact.mjs').read_bytes(),(ROOT/'src/canonical.mjs').read_bytes().replace(b'\r\n',b'\n'))
        for role,name in [('artifact','artifact.mjs'),('manifest','manifest.json'),('procedure','procedure.txt')]:
            self.assertEqual(hashlib.sha256((ROOT/'fixtures'/name).read_bytes()).hexdigest(),claim[role+'_sha256'])
    def test_bundle_matches_published_bytes(self):
        bundle=json.loads((ROOT/'fixtures/bundle.json').read_text())
        for role,name in [('artifact','artifact.mjs'),('manifest','manifest.json'),('procedure','procedure.txt'),('attestation','attestation.json')]:
            e=bundle[role];raw=(ROOT/'fixtures'/name).read_bytes()
            self.assertEqual(e['body'].encode(),raw);self.assertEqual(e['bytes'],len(raw));self.assertEqual(e['sha256'],hashlib.sha256(raw).hexdigest())
