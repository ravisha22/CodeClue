# Enterprise v4 (full-stack): ent-grafana-mech-2
Date: 2026-04-18

## Answer
The deep context presents unified alerting as its own control plane, and the clue file shows provisioning hooks wired into that subsystem rather than into dashboards alone. The provisionable alerting resources are alert rules, contact points, notification policies, mute timings, and templates. Grafana can provision them from files, from Terraform, or through the alerting provisioning HTTP API. Imported resources are treated differently from hand-created ones: file-provisioned or otherwise imported alerting objects are not edited in the UI like manual resources, and file provisioning is not available in Grafana Cloud. Grafana-managed alerts use Grafana’s provisioning HTTP API, while data source-managed alerts are provisioned through the relevant Mimir or Cortex tooling instead.

## Synthesis
Alerting provisioning is a dedicated resource pipeline with multiple inputs, but editability and tooling differ between Grafana-managed and datasource-managed alerts.
