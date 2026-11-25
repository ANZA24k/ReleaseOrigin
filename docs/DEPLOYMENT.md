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
