# Enterprise v4 (full-stack): ent-maybe-rel-1
Date: 2026-04-18

## Answer
The Chat API relationship is explicitly layered across authentication, feature enablement, and scopes. All chat endpoints require either OAuth2 or an API key, and they also require `ai_enabled=true`, so valid credentials alone are not enough if AI is disabled. Read-style chat operations such as get/list use the `read` scope, while create, update, delete, message-send, and retry operations require `write`. The error model keeps those failures separate: unauthorized responses cover missing or invalid auth, while forbidden responses are used when permissions are insufficient or AI is disabled. That means chat access is granted only when auth, AI enablement, and endpoint scope all line up.

## Synthesis
Maybe’s Chat API is guarded by three gates at once: auth, AI enablement, and the correct read/write scope.
