# host_vars

Per-host variables. Ansible loads `host_vars/<inventory_hostname>.yaml` automatically. A directory named after the host (`edge-router/`) is loaded as well: every `*.yaml` in that directory is merged.

Values here are examples. Replace them. Do not commit API passwords, PPPoE credentials, WireGuard private keys, or password hashes.

## Linux hosts

| File | Host | Variables |
| --- | --- | --- |
| `web01.yaml` | `web01` | `compose_project_dir`, `kuma_monitors` |
| `app01.yaml` | `app01` | `compose_project_dir`, `kuma_monitors` |

`lin_compose_update.yaml` fails the host if `compose_project_dir` is missing.

`kuma_monitors` is a list of Uptime Kuma monitor names. `kuma_maintenance` opens a window for those monitors before apt and Compose updates. Leave it unset or empty to skip that host. `kuma_url`, `kuma_user`, and `kuma_pass` are not stored here.

## VyOS

See [edge-router/README.md](edge-router/README.md).
