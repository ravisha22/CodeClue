# Enterprise v4 (full-stack): ent-mattermost-rel-2
Date: 2026-04-18

## Answer
The prompt ties channel discovery and team deletion together through admin/compliance gates. Getting all channels requires `manage_system`, and the stronger `SearchAllChannels` capability can search both private and open channels across all teams while also supporting exclusion of default channels. Team discovery follows the same split: regular users only see open teams in the broad listing, whereas showing all teams again requires `manage_system`. Deletion is more constrained still: team deletion is soft by default, and permanent deletion is reserved for compliance-driven cases when `ServiceSettings.EnableAPITeamDeletion` is enabled.

## Synthesis
The common pattern is deliberate escalation: broad cross-team discovery is admin-only, and irreversible deletion adds a separate compliance-focused feature gate on top of that admin boundary.
