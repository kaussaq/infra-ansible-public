# inventory

Example inventory for the public playbooks. Hosts and addresses are placeholders.

## hosts.yml

| Group | Purpose | Members |
| --- | --- | --- |
| `ubuntu` | Apt upgrade / reboot (`lin_ubuntu_apt_update.yaml`) | `web01`, `app01` |
| `compose` | Docker Compose update (`lin_compose_update.yaml`) | `web01`, `app01` |
| `linux` | Parent of the groups above | |
| `vyos` | Router reconciled from `host_vars/edge-router/` | `edge-router` (`10.1.30.1`) |

## Adding a host

1. Put it in the right groups in `hosts.yml` (`ansible_host` on the first occurrence is enough).
2. For Compose, add `host_vars/<hostname>.yaml` with `compose_project_dir`.
3. To pause Uptime Kuma during apt or Compose updates, set `kuma_monitors` in that file.
4. For another router, copy `host_vars/edge-router/` to `host_vars/<inventory_hostname>/` and edit the YAML. The directory name must match `inventory_hostname`.
