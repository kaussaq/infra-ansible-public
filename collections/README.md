# collections

Galaxy collections this example depends on. AWX can install them as a project collection requirement pointing at `requirements.yaml`. Locally:

```bash
ansible-galaxy collection install -r collections/requirements.yaml
```

## requirements.yaml

| Collection | Used for |
| --- | --- |
| `community.docker` | Compose pull/recreate (`lin_compose_update.yaml`) |
| `vyos.vyos` | VyOS CLI and config (`vyos_*.yaml`) |
| `ansible.netcommon` | `network_cli` connection for VyOS |
| `mrmeganova.uptime_kuma` | Open a maintenance window (`roles/kuma_maintenance`) |

`ansible.builtin` comes with the execution environment and is not listed here.
