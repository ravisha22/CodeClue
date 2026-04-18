# Enterprise v4 (full-stack): ent-calcom-mech-2
Date: 2026-04-18

## Answer
The prompt’s platform/testing materials describe local OAuth testing as a coordinated three-way setup rather than an isolated example app. Environment and config values must line up across the root workspace, the API v2 service, and the example app so both sides of the OAuth exchange agree on client identity and callback targets. On the backend side, the API v2 service includes local-development setup scripts/tooling specifically for preparing OAuth test secrets. The example app consumes the client-visible OAuth settings, while the matching secret stays in the server-side configuration. In the documented happy path, authorization redirects to `localhost:4321?code=abc`, the example app exchanges that code for access and refresh tokens, and it can then observe availability changes coming from the main web app.

## Synthesis
So the example app is wired as a real local OAuth consumer: shared config establishes trust, API v2 performs the secret-side token exchange, and the app then exercises live Cal.diy scheduling state.
