# ReleaseOrigin — Software Build Provenance Verification

Category: Intelligent Contracts (standalone primitive).

ReleaseOrigin verifies documentary software release provenance under an immutable source/build/key policy. It checks commit-pinned artifact, dependency manifest, procedure and signed attestation bytes; deterministically validates SHA-256, RSA-2048 signatures and release/source/version consistency; and uses independent GenLayer leader/validator reasoning to interpret build steps and permitted exceptions. Outcomes are VERIFIED, CONDITIONAL, MISMATCH and INCONCLUSIVE. Claims and evidence are immutable; challenges and reviews append hash-linked receipts. The included small receipt-helper release is actually built locally and signed with a project-controlled ephemeral key. This does not independently certify reproducible builds, real-world builder identity or software safety.

Review source, tests, EVIDENCE and SECURITY first. Use DEPLOYMENT and the machine-readable chain evidence for live verification. No point or acceptance guarantee is made.

## Evidence links

- [Source repository](https://github.com/ANZA24k/ReleaseOrigin)
- [Deployed contract](https://explorer-studio.genlayer.com/address/0x4EA67e0A09dE17aA2909e3f402Dc2E381aeFaAfb)
- [Reviewer guide](REVIEWER.md)
- [Finalized source and receipt verification](verification.json)
- [Test report](tests.json): 32 passing local/fixture tests; VM/web mocked in unit tests.
- [GenVM schema](contract-schema.json) and [lint result](genvm-lint.json): live runtime checks.

Live outcome and lifecycle details are recorded in verification.json and transaction summaries. Local tests cover all four outcomes; a live outcome must only be claimed when present in the collected chain state.

## Completed live evidence

The fixture `RO-LIVE-001` completed create → submit → review → challenge → adjudication → owner finalization. Finalized outcome: **VERIFIED**, two successful reviews, six hash-linked receipts. One earlier adjudication transaction failed to reach consensus and is explicitly preserved in DEPLOYMENT.md; it did not mutate application state. The successful retry and finalization used full NORMAL consensus and the original deployed source.
