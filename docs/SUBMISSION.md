# ReleaseOrigin — Software Build Provenance Verification

Category: Intelligent Contracts (standalone primitive).

ReleaseOrigin verifies documentary software release provenance under an immutable source/build/key policy. It checks commit-pinned artifact, dependency manifest, procedure and signed attestation bytes; deterministically validates SHA-256, RSA-2048 signatures and release/source/version consistency; and uses independent GenLayer leader/validator reasoning to interpret build steps and permitted exceptions. Outcomes are VERIFIED, CONDITIONAL, MISMATCH and INCONCLUSIVE. Claims and evidence are immutable; challenges and reviews append hash-linked receipts. The included small receipt-helper release is actually built locally and signed with a project-controlled ephemeral key. This does not independently certify reproducible builds, real-world builder identity or software safety.

Review source, tests, EVIDENCE and SECURITY first. Use DEPLOYMENT and the machine-readable chain evidence for live verification. No point or acceptance guarantee is made.
