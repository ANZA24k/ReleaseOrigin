# ReleaseOrigin

A standalone GenLayer Intelligent Contract for software build provenance verification. ReleaseOrigin locks a release's source commit, version, artifact/dependency/procedure hashes and trusted builder public key. It retrieves commit-pinned evidence, verifies its byte identity, checks a signed build attestation, and uses independent validator reasoning to assess the declared procedure and build exceptions.

**VERIFIED means documentary provenance is supported under the submitter's locked trust policy. It does not mean the build was independently reproduced, the builder is trustworthy, the source is safe, or the artifact is free of vulnerabilities.**

## What trust problem it solves

Release metadata can claim a source commit or dependency set without supporting it. A valid signature can also cover a build that deviates from the promised process. ReleaseOrigin combines deterministic consistency and signature checks with evidence-grounded semantic review. A validator independently reruns the review and must agree on its decision; a correctly formatted leader answer alone never suffices.

The primitive has no web application dependency, custody, token or escrow. Use its public methods directly in GenLayer Studio or another GenLayer client.

## Outcomes

| Outcome | Meaning |
| --- | --- |
| VERIFIED | Retrieved evidence matches its locked bytes; hashes, RSA signature and versions agree; independent semantic review supports the documented procedure with no disclosed exceptions. |
| CONDITIONAL | The deterministic gates pass and review finds only exceptions expressly allowed by the immutable policy. |
| MISMATCH | Retrieved documents demonstrate a hash/version/signature/schema inconsistency or a clear procedure/policy contradiction. |
| INCONCLUSIVE | A source is unavailable or differs from the submitted bytes, the model cannot give grounded reasoning, or the documentary record is insufficient. |

Network consensus failure is a transaction failure/undetermined transaction, **not** a persisted INCONCLUSIVE result. Failed transactions do not advance the record's review budget.

## Use

1. Install Node 22+ and Python 3.12+. Run `npm ci` and `python -m pip install -r requirements-dev.txt`.
2. Run `npm test`. The local harness mocks the VM and HTTP/LLM responses; its assertions are not a live consensus certificate.
3. Deploy `contracts/release_origin.py` with no constructor arguments in [GenLayer Studio](https://studio.genlayer.com/contracts). Studio's built-in wallet is sufficient. No wallet secret is requested by this repository.
4. Call `create_release(release_id, claim_json)` using the complete JSON **string** in `fixtures/claim.json` or your own policy. The transaction sender becomes the record owner.
5. The same owner calls `submit_evidence(release_id, bundle_json)` using `fixtures/bundle.json` or a matching bundle. Claims and evidence cannot be replaced.
6. Anyone may call `review(release_id)`, then inspect `get_release(release_id)` and `get_receipt(release_id, sequence)`.
7. Anyone can raise one documentary `challenge(release_id, reason)` while the record remains open and budget remains. Call `review` again to adjudicate against the same immutable evidence. The owner may `finalize(release_id)` after review.

Successful INCONCLUSIVE reviews can be retried, with at most three successful reviews total, including challenge adjudication. Other outcomes cannot be rerolled without the single recorded challenge. Owner finalization closes challenges immediately; there is no timed challenge window or claim of economic dispute security. An exhausted record may retain an unresolved INCONCLUSIVE outcome.

See [EVIDENCE](docs/EVIDENCE.md) for the exact schema/signature format, [DEPLOYMENT](docs/DEPLOYMENT.md) for network status, [SECURITY](SECURITY.md) for trust boundaries, and [SUBMISSION](docs/SUBMISSION.md) for reviewer notes.

## Real fixture

The fixture builds the small `src/canonical.mjs` receipt-hashing utility by normalizing line endings. `scripts/build-fixture.py` reads committed source inputs, executes that procedure locally, and signs the resulting attestation with an ephemeral RSA key. Only the public modulus and signature are published. This is a project-controlled builder example, not independent third-party attestation.

To regenerate: first commit the source, manifest and procedure; run `python scripts/build-fixture.py`; publish the generated artifact, claim and attestation; then run `python scripts/prepare-bundle.py` and publish the bundle. Source files use the source commit; the artifact and report use the later evidence commit, avoiding a circular commit/signature reference.

## Architecture and sources

`CREATED → SUBMITTED → REVIEWED/RETRYABLE → [CHALLENGED → review] → FINALIZED`. Every successful mutation appends a receipt with actor, event, state commitment and previous receipt hash. Old receipts and input evidence remain readable.

The implementation follows current official [GenLayer equivalence principle](https://docs.genlayer.com/developers/intelligent-contracts/equivalence-principle), [SDK](https://sdk.genlayer.com/v0.1.4/api/genlayer.html), [storage](https://docs.genlayer.com/developers/intelligent-contracts/storage) and [web access](https://docs.genlayer.com/developers/intelligent-contracts/features/web-access) documentation. Retrieval uses strict equality of byte-check results; semantic review uses `gl.vm.run_nondet_unsafe` with independent leader/validator model calls and exact decision agreement plus exact quotation grounding.

MIT license. No assertion here authenticates physical build execution or independently certifies a release.
