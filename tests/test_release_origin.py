"""Local execution harness. Network/VM consensus is mocked; never a live-proof claim."""
import copy
import importlib.util
import json
import pathlib
import sys
import types
import unittest
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

class Return:
    def __init__(self, data): self.calldata = data
class Contract: pass
class Map:
    def __class_getitem__(cls, item): return dict
identity = lambda f: f
vm = types.SimpleNamespace(Return=Return)
gl = types.SimpleNamespace(Contract=Contract, public=types.SimpleNamespace(write=identity, view=identity), message=types.SimpleNamespace(sender_address='owner'), vm=vm)
sys.modules['genlayer'] = types.SimpleNamespace(gl=gl, TreeMap=Map, u256=int)
spec=importlib.util.spec_from_file_location('contract', pathlib.Path(__file__).resolve().parents[1]/'contracts/release_origin.py')
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class ReleaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.key=rsa.generate_private_key(public_exponent=65537,key_size=2048)
    def setUp(self):
        gl.message.sender_address='owner'
        self.c=m.ReleaseOrigin(); self.c.records={}; self.c.receipts={}
        self.claim={'schema':m.SCHEMA,'repository':'ANZA24k/ReleaseOrigin','source_commit':'a'*40,'version':'1.0.0','builder_rsa_n':format(self.key.public_key().public_numbers().n,'0512x'),'exception_policy':''}
        bodies={'artifact':'export const version="1.0.0";\n','manifest':m.canonical({'name':'helper','version':'1.0.0','dependencies':{}}),'procedure':'Copy source to artifact. No compilation or minification. No exceptions allowed.'}
        for role in bodies: self.claim[role+'_sha256']=m.sha(bodies[role].encode())
        self.payload={k:v for k,v in self.claim.items() if k not in ('builder_rsa_n','exception_policy')}
        self.payload.update(build_description='Copied source to artifact. No compilation or minification.',exceptions='')
        self.bundle={}
        for role,body in bodies.items(): self.put(role,body)
        self.sign()
        self.answer={'decision':'SUPPORTED','reason':'The stated copy procedure is followed without exceptions.','procedure_quote':'Copy source to artifact.','attestation_quote':'Copied source to artifact.'}
        self.fetches=0; self.prompts=0
        def get(url):
            self.fetches+=1
            return types.SimpleNamespace(status=200,body=next(e['body'].encode() for e in self.bundle.values() if e['url']==url))
        def prompt(p): self.prompts+=1; return m.canonical(self.answer)
        gl.nondet=types.SimpleNamespace(web=types.SimpleNamespace(get=get),exec_prompt=prompt)
        gl.eq_principle=types.SimpleNamespace(strict_eq=lambda f:f())
        def run(f,v):
            leader=f()
            if not v(Return(leader)): raise ValueError('Consensus rejected')
            return leader
        vm.run_nondet_unsafe=run
    def put(self,role,body):
        self.bundle[role]={'url':'https://raw.githubusercontent.com/ANZA24k/ReleaseOrigin/'+'a'*40+'/'+role+'.txt','body':body,'sha256':m.sha(body.encode()),'bytes':len(body.encode())}
    def sign(self):
        message=b'ReleaseOrigin attestation v1\x00'+m.canonical(self.payload).encode()
        self.put('attestation',m.canonical({'payload':self.payload,'signature':self.key.sign(message,padding.PKCS1v15(),hashes.SHA256()).hex()}))
    def submit(self):
        self.c.create_release('r1',m.canonical(self.claim)); self.c.submit_evidence('r1',m.canonical(self.bundle))
    def record(self): return json.loads(self.c.get_release('r1'))
    def test_verified_independent_reasoning(self):
        self.submit(); self.c.review('r1'); self.assertEqual(self.record()['result']['status'],'VERIFIED'); self.assertEqual(self.prompts,2); self.assertEqual(self.fetches,4)
    def test_signature_oracle(self):
        att=json.loads(self.bundle['attestation']['body']); self.assertTrue(m.rsa_valid(att['payload'],att['signature'],self.claim['builder_rsa_n'])); att['payload']['version']='2.0.0'; self.assertFalse(m.rsa_valid(att['payload'],att['signature'],self.claim['builder_rsa_n']))
    def test_invalid_signature(self):
        att=json.loads(self.bundle['attestation']['body']); att['signature']='00'*256; self.put('attestation',m.canonical(att)); self.submit(); self.c.review('r1'); self.assertIn('SIGNATURE_INVALID',self.record()['result']['failures']); self.assertEqual(self.prompts,0)
    def test_signature_modulus_boundary(self): self.assertFalse(m.rsa_valid(self.payload,self.claim['builder_rsa_n'],self.claim['builder_rsa_n']))
    def test_claim_hash_mismatch(self):
        self.claim['artifact_sha256']='b'*64; self.submit(); self.c.review('r1'); self.assertEqual(self.record()['result']['status'],'MISMATCH')
    def test_signed_version_mismatch(self):
        self.payload['version']='2.0.0'; self.sign(); self.submit(); self.c.review('r1'); self.assertIn('ATTESTATION_VERSION',self.record()['result']['failures'])
    def test_manifest_version_mismatch(self):
        self.put('manifest',m.canonical({'name':'helper','version':'2.0.0','dependencies':{}})); self.submit(); self.c.review('r1'); self.assertIn('MANIFEST_VERSION',self.record()['result']['failures'])
    def test_malformed_attestation(self):
        self.put('attestation','{}'); self.submit(); self.c.review('r1'); self.assertIn('MALFORMED_PROVENANCE',self.record()['result']['failures'])
    def test_unavailable_is_not_mismatch(self):
        self.submit(); gl.nondet.web.get=lambda u:types.SimpleNamespace(status=404,body=b''); self.c.review('r1'); self.assertEqual(self.record()['result']['status'],'INCONCLUSIVE'); self.assertEqual(self.prompts,0)
    def test_fetch_substitution(self):
        self.submit(); gl.nondet.web.get=lambda u:types.SimpleNamespace(status=200,body=b'substituted'); self.c.review('r1'); self.assertEqual(self.record()['result']['status'],'INCONCLUSIVE')
    def test_oversized_fetch(self):
        self.submit(); gl.nondet.web.get=lambda u:types.SimpleNamespace(status=200,body=b'x'*8001); self.c.review('r1'); self.assertEqual(self.record()['result']['status'],'INCONCLUSIVE')
    def test_fetch_exception(self):
        self.submit()
        def fail(u): raise RuntimeError('timeout')
        gl.nondet.web.get=fail; self.c.review('r1'); self.assertEqual(self.record()['result']['status'],'INCONCLUSIVE')
    def test_conditional(self):
        self.claim['exception_policy']='Minification is allowed.'; self.payload['exceptions']='Minification applied.'; self.sign(); self.answer['decision']='EXCEPTION'; self.submit(); self.c.review('r1'); self.assertEqual(self.record()['result']['status'],'CONDITIONAL')
    def test_model_cannot_invent_exception_authority(self):
        self.answer['decision']='EXCEPTION'; self.submit(); self.c.review('r1'); self.assertEqual(self.record()['result']['status'],'INCONCLUSIVE')
    def test_supported_cannot_ignore_disclosed_exception(self):
        self.payload['exceptions']='Minified.'; self.sign(); self.submit(); self.c.review('r1'); self.assertEqual(self.record()['result']['status'],'INCONCLUSIVE')
    def test_semantic_mismatch(self):
        self.answer['decision']='CONTRADICTED'; self.submit(); self.c.review('r1'); self.assertEqual(self.record()['result']['status'],'MISMATCH')
    def test_fabricated_quote_fails_closed(self):
        self.answer['procedure_quote']='not in document'; self.submit(); self.c.review('r1'); self.assertEqual(self.record()['result']['status'],'INCONCLUSIVE'); self.assertEqual(self.prompts,4)
    def test_validator_disagreement(self):
        self.submit()
        def run(f,v):
            a=f(); self.answer['decision']='CONTRADICTED'; self.assertFalse(v(Return(a))); raise ValueError('Consensus rejected')
        vm.run_nondet_unsafe=run
        with self.assertRaisesRegex(ValueError,'Consensus'): self.c.review('r1')
        self.assertEqual(self.record()['attempts'],0)
    def test_duplicate_json(self):
        with self.assertRaises(AssertionError):m.parse('{"x":1,"x":2}')
    def test_nonfinite_json(self):
        with self.assertRaises(ValueError):m.parse('{"x":NaN}')
    def test_url_restrictions(self):
        for url in ['http://localhost/x','https://raw.githubusercontent.com.evil/x','https://raw.githubusercontent.com/ANZA24k/ReleaseOrigin/main/x','https://raw.githubusercontent.com/ANZA24k/ReleaseOrigin/'+'a'*40+'/../x','https://raw.githubusercontent.com/ANZA24k/ReleaseOrigin/'+'a'*40+'/x?key=1','https://raw.githubusercontent.com/ANZA24k/ReleaseOrigin/'+'a'*40+'/%2e%2e/x']:
            with self.subTest(url=url), self.assertRaises(AssertionError):m.check_url(url,self.claim,'artifact')
    def test_source_commit_binding(self):
        url=self.bundle['manifest']['url'].replace('a'*40,'b'*40)
        with self.assertRaises(AssertionError):m.check_url(url,self.claim,'manifest')
    def test_evidence_byte_binding(self):
        self.bundle['artifact']['bytes']+=1
        with self.assertRaises(AssertionError):self.submit()
    def test_oversized_evidence(self):
        self.put('artifact','x'*8001)
        with self.assertRaises(AssertionError):self.submit()
    def test_owner_and_immutability(self):
        self.c.create_release('r1',m.canonical(self.claim)); gl.message.sender_address='attacker'
        with self.assertRaises(AssertionError):self.c.submit_evidence('r1',m.canonical(self.bundle))
        gl.message.sender_address='owner'; self.c.submit_evidence('r1',m.canonical(self.bundle))
        with self.assertRaises(AssertionError):self.c.submit_evidence('r1',m.canonical(self.bundle))
        with self.assertRaises(AssertionError):self.c.create_release('r1',m.canonical(self.claim))
    def test_receipt_chain_and_state_commitment(self):
        self.submit(); self.c.review('r1'); self.c.finalize('r1'); r=self.record(); prev=m.ZERO
        for i in range(1,r['sequence']+1):
            receipt=json.loads(self.c.get_receipt('r1',i)); claimed=receipt.pop('hash'); self.assertEqual(m.digest(receipt),claimed); self.assertEqual(receipt['previous'],prev); prev=claimed
        self.assertEqual(prev,r['head']); last=json.loads(self.c.get_receipt('r1',r['sequence'])); before=copy.deepcopy(r); before.update(sequence=r['sequence']-1,head=last['previous']); self.assertEqual(m.digest(before),last['state_hash'])
    def test_challenge_and_adjudication(self):
        self.submit(); self.c.review('r1'); old=self.record()['head']; gl.message.sender_address='reviewer'; self.c.challenge('r1','The declared procedure may prohibit minification.'); self.c.review('r1'); self.assertEqual(self.record()['attempts'],2); self.assertNotEqual(self.record()['head'],old)
        with self.assertRaises(AssertionError):self.c.challenge('r1','again')
        with self.assertRaises(AssertionError):self.c.finalize('r1')
        gl.message.sender_address='owner'; self.c.finalize('r1')
        with self.assertRaises(AssertionError):self.c.review('r1')
    def test_bounded_retry(self):
        self.answer['decision']='UNKNOWN'; self.submit()
        for _ in range(3):self.c.review('r1')
        with self.assertRaises(AssertionError):self.c.review('r1')
        self.assertEqual(self.record()['attempts'],3)
    def test_invalid_modulus(self):
        self.claim['builder_rsa_n']='0'*512
        with self.assertRaises(AssertionError):m.check_claim(self.claim)
    def test_dependency_ranges_rejected(self):
        self.put('manifest',m.canonical({'name':'helper','version':'1.0.0','dependencies':{'lib':'^1.0'}})); self.submit(); self.c.review('r1'); self.assertIn('MALFORMED_PROVENANCE',self.record()['result']['failures'])

if __name__=='__main__': unittest.main()
