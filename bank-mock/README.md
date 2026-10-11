# Final bank mock

The seven POST services implement the supplied contract under `/voice/v1/`. This is synthetic test data, not a real bank. `test-customers.json` is an unchanged copy of the official final fixture. Static responses and ignored call/auth metadata are explicitly required by the test-environment document; no database or invented payment processing is used.

Pinned environment: Node 24.19.0 and Wrangler 4.149.0.

```console
npm ci
npm test
npx wrangler login
npm run deploy
```

Deployment uses the account in wrangler.toml; another operator must authenticate to that account or supply their own account configuration. No token is committed. Keep the worker running until event results are announced.

Active base URL: https://freya-final-bank.freya-final-bank-mock.workers.dev
Health: GET /health. This diagnostic endpoint is separate from the bank contract.

617 source response fixtures are compared locally, including the prescribed 12-second delay. `export-fixtures.js` writes the same explicit checks for `scripts/check_mock.py`. Remote comparison results belong to the measured run; local passing checks alone do not prove deployment.
