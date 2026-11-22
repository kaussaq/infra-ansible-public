# playbooks

Job templates in AWX should point here. Custom Jinja filters for VyOS live in `filter_plugins/` (Ansible loads that directory automatically when the playbook is in this folder). Shared roles live in `roles/`.

## Linux

These playbooks are here because they open an Uptime Kuma window before changing hosts.

| Playbook | Hosts | What it does |
| --- | --- | --- |
| `lin_ubuntu_apt_update.yaml` | `ubuntu` | Dist upgrade, then reboot if `/var/run/reboot-required` (or `force_reboot=true`). Opens an Uptime Kuma window first when `kuma_monitors` is set |
| `lin_compose_update.yaml` | `compose` | Pull Compose images, recreate the stack, prune unused images older than 7 days (`168h`). Needs `compose_project_dir` in host_vars. `become` follows `compose_become` (default `true`). Opens an Uptime Kuma window first when `kuma_monitors` is set |

Both include `kuma_maintenance` as a pre-task. The role does nothing when `kuma_monitors` is empty or unset. `kuma_url`, `kuma_user`, and `kuma_pass` come from an AWX credential. See [roles/kuma_maintenance/README.md](roles/kuma_maintenance/README.md).

## VyOS

| Playbook | Hosts | What it does |
| --- | --- | --- |
| `vyos_con_test.yaml` | `vyos` | `show version` and `show system uptime` |
| `vyos_get_config.yaml` | `vyos` | Dump `show configuration commands` |
| `vyos_configuration.yaml` | `vyos` | Reconcile running config with `host_vars/<device>/*.yaml` |

`vyos_configuration.yaml` **requires** `vyos_dry_run` set to `true` or `false` at launch (survey or extra vars). With `true` it prints the set/delete plan and stops. With `false` it applies and saves. See `inventory/host_vars/edge-router/README.md`.

`vyos_get_config.yaml` prints the live router config, which can include secrets. Do not publish that job output.
