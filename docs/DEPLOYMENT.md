# Deployment

Target: GenLayer Studionet through GenLayer Studio. Constructor takes no arguments. Load the exact `contracts/release_origin.py` file and deploy using the built-in Studio wallet. Never export a wallet private key to run this project.

Runtime validation and live transaction evidence are recorded here and in `deployment.json` as they become available. Do not treat local mocks or example fixture signatures as proof of a live deployment.

The `npm run schema` command requests schema generation for the source through the GenLayer JS SDK. Its endpoint may require network access. `npm run verify` reads public finalized chain state and compares exact source bytes and hash-linked receipts. These commands perform no signing and hold no private keys.
