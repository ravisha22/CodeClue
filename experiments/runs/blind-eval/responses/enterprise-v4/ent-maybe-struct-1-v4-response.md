# Enterprise v4 (full-stack): ent-maybe-struct-1
Date: 2026-04-18

## Answer
The README and deep-context material describe Maybe as a personal finance app for everyone and as a fully working application rather than just a code sample. The documented usage modes split cleanly by audience: end users get the browser product, self-hosters are pointed to Docker-based hosting guidance, and developers are directed to the separate local-development setup instead of the self-hosting path. That distinction is reinforced by the prompt’s explicit mention of `docs/hosting/docker.md` for Docker self-hosting. The same prompt also shows that Maybe exposes a documented JSON API surface, including the AI chat API under `/api/v1/chats`. So the repo presents one product with distinct surfaces for app users, Docker self-hosters, and API/development consumers.

## Synthesis
Maybe exposes a working personal-finance app, a Docker self-hosting track, a separate developer setup path, and an API surface that includes AI chat.
