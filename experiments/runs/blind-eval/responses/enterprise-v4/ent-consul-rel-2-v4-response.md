# Enterprise v4 (full-stack): ent-consul-rel-2
Date: 2026-04-18

## Answer
The prompt shows four documented registration paths for checks, and each hangs the check payload off a different API shape. The server-side catalog path is `/v1/catalog/register`, where checks are supplied through the `Checks` field on `structs.RegisterRequest`. The agent-local check path is `/v1/agent/check/register`, which goes through `AgentRegisterCheck`. Service registration is a third path: `/v1/agent/service/register` can attach checks through the `Check` or `Checks` fields on `ServiceDefinition`. Finally, the CLI path `consul services register` also supports checks through the `Check` and `Checks` fields on `api.AgentServiceRegistration`.

## Synthesis
In other words, checks are not owned by a single endpoint; they can arrive through catalog writes, direct agent-check registration, service registration, or the CLI wrapper over the agent API.
