# roles

Ansible roles used by playbooks in the parent directory. A playbook includes a role by its directory name (`ansible.builtin.include_role`).

| Role | Included by | What it does |
| --- | --- | --- |
| `kuma_maintenance` | `lin_ubuntu_apt_update.yaml`, `lin_compose_update.yaml` | Opens an Uptime Kuma maintenance window for the host before work starts |

See [kuma_maintenance/README.md](kuma_maintenance/README.md).
