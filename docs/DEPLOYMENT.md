# Deployment

Target: GenLayer Studionet through GenLayer Studio. Constructor takes no arguments. Load the exact `contracts/release_origin.py` file and deploy using the built-in Studio wallet. Never export a wallet private key to run this project.

Runtime validation and live transaction evidence are recorded here and in `deployment.json` as they become available. Do not treat local mocks or example fixture signatures as proof of a live deployment.

The `npm run schema` command requests schema generation for the source through the GenLayer JS SDK. Its endpoint may require network access. `npm run verify` reads public finalized chain state and compares exact source bytes and hash-linked receipts. These commands perform no signing and hold no private keys.

## Deployed instance (24 November 2026)

[Open contract explorer](https://explorer-studio.genlayer.com/address/0x4EA67e0A09dE17aA2909e3f402Dc2E381aeFaAfb).

Contract: `0x4EA67e0A09dE17aA2909e3f402Dc2E381aeFaAfb`, Studionet chain ID `61999`.

Deployment transaction: [0x338f2bb8…](https://explorer-studio.genlayer.com/tx/0x338f2bb88147fe37c2168798e74941877c50d3dd7cbc57b7d20ee97c2c8eea1d).

Deployment used Studio's built-in wallet and NORMAL full consensus. GenVM schema generation succeeded and `sim_lintContract` reported zero issues. See `contract-schema.json` and `genvm-lint.json`. `RO-LIVE-001` is the live signed receipt-helper fixture. Current finalized phase, verdict, source SHA-256 and receipt checks are in `verification.json`; each `tx-*.json` records observed transaction status and votes. The exact source-byte comparison checks the deployed code against this repository.

Do not use a generic explorer from an older SDK chain definition: this deployment is on `explorer-studio.genlayer.com`. Studionet resets may remove historical state; archived JSON observations do not guarantee permanent network retention.

## Completed lifecycle (25 November 2026)

`RO-LIVE-001` is **FINALIZED / VERIFIED**, with two successful reviews and six linked receipts. The independently read finalized receipt head is `42f2eca8250bed2314b7682231dc4f16ba24c4231bac2a98e5f0cb7ec12a5be7`.

| Step | Transaction | Observed outcome |
| --- | --- | --- |
| Deploy | [0x338f2bb8](https://explorer-studio.genlayer.com/tx/0x338f2bb88147fe37c2168798e74941877c50d3dd7cbc57b7d20ee97c2c8eea1d) | Successful, finalized |
| Create claim | [0xfb09b9e8](https://explorer-studio.genlayer.com/tx/0xfb09b9e86ba70417ebad48f82dc0e98200def17443abb432eeeb7414e8071fc5) | Successful, finalized |
| Submit evidence | [0xfbb7b0d3](https://explorer-studio.genlayer.com/tx/0xfbb7b0d32ba99e8c40d50e953fb8a555e2a6e1431afc848e1473a6295bc49769) | Successful, finalized |
| Initial review | [0x18f1717e](https://explorer-studio.genlayer.com/tx/0x18f1717e2df934ca024a82f42ae748749a64ab4c1a80db98d0b3d34954cb52b5) | VERIFIED, finalized |
| Challenge | [0x47661092](https://explorer-studio.genlayer.com/tx/0x47661092ac98b84656fa348935bd583c6b55367fbb2ba6e71549a3982dbe69c2) | Recorded, finalized |
| First adjudication attempt | [0x41e2f188](https://explorer-studio.genlayer.com/tx/0x41e2f1887d9657e89d43cae84d7993e244e51bb003832892455e93866585b52b) | Consensus UNDETERMINED; no application state mutation |
| Adjudication retry | [0x544353cf](https://explorer-studio.genlayer.com/tx/0x544353cfd1f69aaaaa7162882334837a0bd4855b811ba3d2a9b8432eb7dd2392) | VERIFIED, finalized |
| Owner finalization | [0x3dc1199b](https://explorer-studio.genlayer.com/tx/0x3dc1199b8bc2a9fd15aefbfd0dec8706dea60c88b556f96a367b46b4b87f0826) | Successful, finalized |

The failed adjudication attempt's leader returned UNKNOWN after its bounded model-response checks failed. Other validators disagreed, so the network did not accept that proposed state. The retry independently reached consensus on SUPPORTED, preserving the immutable procedure and evidence. No validator rules, model settings, evidence or contract source were weakened or changed for the retry. An explorer transaction can be finalized with an Undetermined consensus result; finality alone does not imply a successful application mutation. Some explorer method labels currently display `(constructor)` for calls; use the ABI/calldata and application receipts for method identity.

`npm run verify` re-read finalized state and verified exact deployed-source equality, evidence byte hashes, claim/bundle/result commitments, receipt linkage and final state commitment. The source SHA-256 remains `d36a38974303a1663e9c848c22b9b81ad26b86cdb5b31523ca24f40b9599abe7`.
