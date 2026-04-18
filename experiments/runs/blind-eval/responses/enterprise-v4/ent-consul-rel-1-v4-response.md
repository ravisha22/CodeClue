# Enterprise v4 (full-stack): ent-consul-rel-1
Date: 2026-04-18

## Answer
The ACL documentation in the prompt makes tokens the hub of the model. ACL tokens are the central runtime credential, and those tokens are linked to policies and roles rather than standing alone. External identity systems plug in through `AuthMethods` plus `BindingRules`, which can mint ACL tokens from Kubernetes, JWT, or OIDC identities. Separately, `ServiceIdentity` and `NodeIdentity` act as policy templates for a concrete service or node, and those templates can then be rendered into a full policy that attaches to tokens.

## Synthesis
So the relationship graph is: external identity may create a token, the token carries roles/policies, and service/node identities are reusable templates for the policy side of that token.
