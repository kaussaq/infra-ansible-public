# group_vars

Connection defaults for every host in the matching inventory group. Files in `host_vars/` override these.

| File | Group | What it sets |
| --- | --- | --- |
| `linux.yaml` | `linux` | SSH on port 22 |

VyOS does not use this file. Its connection plugin (`ansible.netcommon.network_cli` / `vyos.vyos.vyos`) is set on the host in `host_vars/edge-router/connection.yaml`.

Ansible users and passwords are not stored here. They come from AWX credentials.
