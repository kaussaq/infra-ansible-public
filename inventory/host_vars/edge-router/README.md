# edge-router

Example desired VyOS configuration for host `edge-router` (`10.1.30.1`). `playbooks/vyos_configuration.yaml` flattens this tree to CLI `set` lines, diffs them against `show configuration commands`, and applies the delta.

Removing a key from these files deletes that node on the router **if** its top-level section is listed in `vyos_sections`. Always run with `vyos_dry_run=true` first.

Every address, MAC, and key below is a placeholder.

## Files

| File | Variable | Contents |
| --- | --- | --- |
| `connection.yaml` | Ansible connection | `network_cli`, `vyos.vyos.vyos`, timeouts |
| `settings.yaml` | Reconcile policy | Managed sections, protected lines, delete limits, `vyos_no_log` |
| `tree.yaml` | `vyos_tree` | Wires each section var into one dict for the playbook |
| `firewall.yaml` | `vyos_firewall` | Groups and IPv4 forward/input rulesets |
| `interfaces.yaml` | `vyos_interfaces` | Bond, bridge/VIFs, PPPoE, WireGuard |
| `nat.yaml` | `vyos_nat` | Destination (port-forward) and source NAT |
| `protocols.yaml` | `vyos_protocols` | Static routes |
| `service.yaml` | `vyos_service` | DHCP, DNS, HTTPS API, NTP, SSH |
| `system.yaml` | `vyos_system` | Hostname, login users, DNS, syslog, time zone |
| `vrf.yaml` | `vyos_vrf` | Example tenant VRF |

YAML shape matches the VyOS CLI: dict keys are path nodes, scalars are leaf values, lists are multi-value leaves, an empty value is a valueless node.

## settings.yaml

- `vyos_sections` — top-level sections the playbook owns. Anything under those sections that is not in vars is deleted.
- `vyos_protected` — regexes that are never deleted (SSH and the `awx` login user, so a bad run cannot lock AWX out).
- `vyos_max_deletes` / `vyos_allow_mass_delete` — refuse large delete plans unless you override.
- `vyos_no_log` — keep task output from leaking secrets; set false only while debugging.

To manage a new section: add a vars file, include it in `tree.yaml`, and add the section name to `vyos_sections`.

Passwords, hashes, and keys should be extra vars or Vault (`vyos_cred_*`), not committed as plaintext. The example `system.yaml` SSH key is not a real key; replace it.
