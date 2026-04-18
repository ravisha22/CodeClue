# Enterprise v4 (full-stack): ent-mattermost-mech-2
Date: 2026-04-18

## Answer
Mattermost’s policy docs treat security response as a separate, time-bounded process. Security-sensitive issues are not supposed to go through public GitHub issues; they should be sent to `responsibledisclosure@mattermost.com`. Once fixes exist, security updates are only maintained for the latest three releases plus the current Extended Support Release. Critical fixes are shipped as dot releases, and disclosure is intentionally delayed: details about the security update are announced 30 days after the update becomes available.

## Synthesis
That creates a staged mechanism of private intake, limited support windows, urgent patch delivery, and delayed public detail release to balance remediation speed with coordinated disclosure.
