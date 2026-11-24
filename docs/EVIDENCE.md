# Evidence protocol v1

All JSON strings are bounded UTF-8. Duplicate keys and nonfinite constants are rejected. Canonical serialization is Python `json.dumps(sort_keys=True, separators=(',', ':'), ensure_ascii=True)`. Do not use JCS assumptions: protocol fields are strings, integers, booleans, objects and arrays. Digests are lowercase SHA-256 hex of exactly specified UTF-8 bytes.

## Immutable claim

Exactly: `schema` (`releaseorigin/v1`), `repository` (`owner/repo`), `source_commit` (40 lowercase hex), `version` (1–80 safe ASCII characters), `artifact_sha256`, `manifest_sha256`, `procedure_sha256` (64 hex each), `builder_rsa_n` (512 lowercase hex, odd 2048-bit modulus), `exception_policy` (0–1600 UTF-8 bytes). RSA exponent is fixed to 65537. The creator chooses the trusted key: consumers must independently decide whether that policy and builder are credible.

## Immutable bundle

Exactly four roles: `artifact`, `manifest`, `procedure`, `attestation`. Each has exactly `url`, `body` (nonempty UTF-8 string, up to 8000 bytes), `bytes` (exact integer byte length) and `sha256` (hash of the UTF-8 body). Whole bundle input max 28000 UTF-8 bytes including JSON escaping. Claim input max 6000 bytes. The actual binary release workflow must use a text representation artifact supported by this narrow version; this version does not download large binaries or verify arbitrary ecosystems.

Only `https://raw.githubusercontent.com/{declared owner/repo}/{full40commit}/{safe path}` URLs are accepted. No credentials, query, fragment, percent escapes, traversal, alternative ports, mutable refs or arbitrary domains. Manifest and procedure must be at the declared source commit. Artifact and attestation may live at a later immutable evidence commit in the same repository. The runtime handles HTTP transport; this SDK does not expose a contract-level streaming size limit or redirect option. The contract never follows evidence-supplied links and accepts only status 200 plus exact post-fetch byte length and SHA-256. VM/provider limits bound transport allocation; the 8000-byte check is after retrieval.

An HTTP failure or byte disagreement yields INCONCLUSIVE before interpreting supplied text. It does not prove the release itself mismatches. Large artifacts, inaccessible/private repositories, Git SHA-256 repositories and detached Sigstore/DSSE/SLSA envelopes are outside v1's supported formats.

## Dependency manifest

Exactly `name`, `version`, `dependencies`. Dependencies maps at most 64 names to exact version strings beginning with a digit. Ranges such as `^1.0` are rejected. This is declaration consistency, not package resolution or proof of transitive completeness. Manifest version must equal the locked release version; manifest bytes must match the declared and signed hash.

## Attestation and signature

Exactly `payload`, `signature`. Payload fields: `schema`, `repository`, `source_commit`, `version`, `artifact_sha256`, `manifest_sha256`, `procedure_sha256`, `build_description` (1–2400 bytes), `exceptions` (0–1600 bytes). First seven must exactly equal the corresponding claim fields.

Signature is exactly 256 bytes represented as 512 lowercase hex characters, RSA-2048 PKCS#1 v1.5 with SHA-256 and e=65537. Signed message:

```python
b'ReleaseOrigin attestation v1\x00' + canonical(payload).encode('utf-8')
```

The contract verifies the complete encoded message (00 01 FF...00 plus SHA-256 DigestInfo); signatures outside the modulus are rejected. The immutable claim binds key and exception policy. Attestations can intentionally be reused under different claims; they bind the release data, not the submitter identity or an endorsement of their exception policy. No CA, transparency log, key ownership or external builder identity is inferred.

## Semantic review

Evidence, policy and challenges are treated as untrusted data in the prompt. Each node independently interprets required steps and disclosed exceptions. Allowed model decisions are SUPPORTED, EXCEPTION, CONTRADICTED, UNKNOWN. The leader and validator must agree exactly on decision; explanation wording may vary. Both responses must independently pass schema and exact substring quotation checks against the procedure and canonical signed payload. Malformed/model errors get at most two model calls per node before UNKNOWN. Empty quotes are permitted only for UNKNOWN. An empty exception policy cannot produce CONDITIONAL; disclosed exceptions cannot produce VERIFIED even if the model incorrectly returns SUPPORTED.

Quotation presence is grounding, not a proof that the interpretation is correct. Consensus reduces unilateral interpretation risk; it does not make documentary claims physically true.

## Receipts

Each receipt includes schema, release ID, increasing sequence, previous receipt SHA-256, event, transaction actor, state hash and detail. Its `hash` is SHA-256 of the canonical receipt without the `hash` field. `state_hash` commits the resulting record before updating its `sequence` and `head` for this receipt. Review detail commits the entire result including retrieval checks and semantic explanation. The full bundle and claim have their own canonical hashes. Old receipts are never changed. Use `npm run verify` after configuring `docs/deployment.json` to independently check deployed source, evidence and receipt hashes at latest finalized state.
