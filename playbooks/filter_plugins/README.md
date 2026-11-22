# filter_plugins

Ansible filter plugins for this playbook directory. `vyos_configuration.yaml` uses `vyos_tree.py`; Ansible loads `filter_plugins/` next to the playbook automatically.

## vyos_tree.py

State-driven VyOS helpers. Tree conventions match the VyOS CLI (see `inventory/host_vars/edge-router/README.md`).

| Filter | Arguments | Result |
| --- | --- | --- |
| `vyos_flatten` | nested dict | Canonical `set ...` lines |
| `vyos_plan` | desired lines, running config, managed sections, optional protected regexes | `{"set": [...], "delete": [...]}` for those sections |
| `vyos_mask` | list of lines | Same lines with values masked when the path looks like a secret (`password`, `key`, and similar) |

Deletes collapse to the highest ancestor whose whole subtree is being removed, but never above `<section> <child>`. Lines matching `vyos_protected` are kept even if they are missing from vars.
