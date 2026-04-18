# Enterprise v4 (full-stack): ent-maybe-mech-1
Date: 2026-04-18

## Answer
The documented lifecycle starts with chat creation: `POST /api/v1/chats` can include an optional title, initial message, and model, and it returns the same overall shape as `Get Chat`. After a chat exists, `POST /api/v1/chats/:chat_id/messages` immediately returns the user message rather than blocking on the model, and it marks the work with `ai_response_status: pending`. That pending state exists because the assistant response is generated asynchronously in the background. A client observes completion by polling the chat endpoint again and looking for the new `assistant_message` record to appear in the chat’s `messages` array. So the API is intentionally request-now, observe-later rather than streaming the answer inline.

## Synthesis
Maybe returns chat/message writes immediately, does AI generation asynchronously, and expects clients to poll the chat resource for the assistant reply.
