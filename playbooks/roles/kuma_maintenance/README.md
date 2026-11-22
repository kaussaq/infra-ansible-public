# kuma_maintenance

Opens an Uptime Kuma maintenance window for the current host, then returns. Included as a pre-task by `lin_ubuntu_apt_update.yaml` and `lin_compose_update.yaml`. It does not close the window; Uptime Kuma ends it when `duration_minutes` elapses.

The role skips the API call when `kuma_monitors` is unset or empty, so hosts without that list are left alone.

## What it runs

All tasks delegate to `localhost` (the AWX execution environment) and do not `become`.

1. Check that `/usr/bin/python3.12` can import `socketio` and `websocket`.
2. If that import fails, `pip install --user python-socketio websocket-client` with that interpreter.
3. Call `mrmeganova.uptime_kuma.maintenance` with the host's monitor list, every status page, and a title of `maintenance <inventory_hostname>`.

Requires the `mrmeganova.uptime_kuma` collection (`collections/requirements.yaml`).

## Variables

| Variable | Where | Meaning |
| --- | --- | --- |
| `kuma_monitors` | `inventory/host_vars/<host>.yaml` | Monitor names to put into maintenance. Empty or unset skips the role |
| `kuma_url` | AWX credential or Vault | Uptime Kuma API URL |
| `kuma_user` | AWX credential or Vault | API username |
| `kuma_pass` | AWX credential or Vault | API password |
| `kuma_maint_minutes` | extra var, optional | Window length in minutes. Default `60` |

Do not commit `kuma_user` or `kuma_pass`.
