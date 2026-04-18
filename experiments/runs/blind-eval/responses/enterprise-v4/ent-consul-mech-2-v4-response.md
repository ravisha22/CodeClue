# Enterprise v4 (full-stack): ent-consul-mech-2
Date: 2026-04-18

## Answer
The configuration path in the prompt makes agent config the canonical source of truth for starting Consul. Most settings come from HCL or JSON config files, with command-line flags and Auto-Config acting as additional inputs. The loader reads those files into an ordered list of configuration sources and merges them into a final `RuntimeConfig`. If Auto-Config is enabled, Consul repeats that process after receiving server-provided configuration, effectively adding the auto-configured data as another source in the merge chain.

## Synthesis
Mechanically, Consul config is an ordered-source merge pipeline, and Auto-Config works by re-running that merge with one more authoritative source injected into the list.
