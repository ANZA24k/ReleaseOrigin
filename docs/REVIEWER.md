# Reviewer guide

ReleaseOrigin is a standalone Intelligent Contract. Its primary deliverables are the contract, its public ABI, bounded verification rules, tests and live transaction evidence. No frontend is required to exercise it.

## Live deployment

- Network: Studionet, chain ID 61999.
- [Contract explorer](https://explorer-studio.genlayer.com/address/0x4EA67e0A09dE17aA2909e3f402Dc2E381aeFaAfb).
- Contract source: `contracts/release_origin.py`.
- Release fixture ID: `RO-LIVE-001`.
- Raw input JSON: `fixtures/claim.json` and `fixtures/bundle.json`.
- Read `docs/verification.json`, `RO-LIVE-001-record.json`, `RO-LIVE-001-receipts.json` and `tx-*.json` for independently collected chain evidence. Transaction summaries report NORMAL execution and consensus votes; they are RPC observations, not cryptographically signed RPC certificates.

## Reproduce

Run `npm ci`, `python -m pip install -r requirements-dev.txt`, then `npm test`. Run `npm run verify` against the public deployment to compare exact deployed source and finalized record/receipt/evidence hashes. Use `node scripts/inspect-tx.mjs TRANSACTION_HASH` to refresh a transaction summary directly from Studionet.

In Studio, select the deployed contract and call `get_release("RO-LIVE-001")` and `get_receipt("RO-LIVE-001", 1)` through sequence shown in the record. To create your own record, deploy the source with the built-in wallet or use the existing contract, choose a new ID, then create/submit/review. Reusing the built fixture means trusting its explicitly project-controlled builder key; it does not establish a third-party builder identity.

## Where to look

- `check_url`, `check_bundle`: immutable source location, UTF-8 byte length and SHA-256 binding.
- `rsa_valid`: complete RSA PKCS#1-v1.5 encoded-message comparison.
- `deterministic`: hash/version/source/manifest/attestation consistency, independent of model opinion.
- `review`: exact retrieval agreement, independent leader/validator model reasoning, decision agreement and quote grounding.
- `_save`: append-only receipt linkage and resulting-state commitment.
- `challenge`, `finalize`: optional single challenge, total budget of three successful reviews, owner-controlled closure.

All four outcomes are tested locally. A live VERIFIED record demonstrates the actual semantic path. No fixture or test asserts independent reproducibility, malware absence, real-world key ownership, or an external audit. The model may be wrong; validators, immutable evidence and conservative unknown handling mitigate unilateral claims rather than eliminate truth uncertainty.
