# AWX examples: VyOS desired state and Uptime Kuma maintenance

A public, sanitized slice of an AWX project. It shows two patterns:

- **VyOS** — desired config is YAML. A filter plugin flattens it to `set` lines, diffs that against `show configuration commands`, and applies the delta.
- **Uptime Kuma** — before apt or Compose work, a role opens a maintenance window for the monitors named on that host.

Addresses, hostnames, NIC IDs, DHCP mappings, SSH keys, and WireGuard material in `inventory/` are **examples**. They are not a real network. Put secrets in AWX credentials or Ansible Vault (`kuma_pass`, `vyos_cred_*`), not in git.

## Layout

```
awx-public/
├── collections/          Galaxy requirements for this slice
├── inventory/            Example hosts and desired VyOS state
└── playbooks/
    ├── filter_plugins/   vyos_flatten / vyos_plan / vyos_mask
    └── roles/kuma_maintenance/
```

## How to try it

1. Point an AWX project at this directory, or run Ansible locally against it.
2. Install collections: `ansible-galaxy collection install -r collections/requirements.yaml`.
3. Inventory source: `inventory/hosts.yml`.
4. VyOS jobs need an SSH credential for the router. Launch `playbooks/vyos_configuration.yaml` with `vyos_dry_run=true` before `false`.
5. Kuma jobs need `kuma_url`, `kuma_user`, and `kuma_pass` from a credential. Hosts with an empty or missing `kuma_monitors` list are skipped.

Linux connection defaults are SSH on port 22 (`inventory/group_vars/linux.yaml`). The VyOS connection plugin is set in `inventory/host_vars/edge-router/connection.yaml`.
