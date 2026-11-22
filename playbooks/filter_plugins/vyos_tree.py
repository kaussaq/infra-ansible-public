"""Filters for state-driven VyOS config management.

vyos_flatten(tree)            -> list of canonical `set ...` lines for a nested dict
vyos_plan(desired, running,   -> {"set": [...], "delete": [...]} needed to make the
          managed, protected)    managed subtrees of `running` equal `desired`
vyos_mask(lines)              -> same lines with secret values masked (for display)

Tree conventions (mirrors the VyOS CLI):
  dict key        -> path node            (tag nodes and plain nodes alike)
  scalar          -> leaf value           (rendered as: <path> '<value>')
  list            -> multi-value leaf     (one line per item)
  None / empty    -> valueless node       (rendered as: <path>)
"""
from __future__ import annotations

import re

from ansible.errors import AnsibleFilterError

_TOKEN = re.compile(r"'[^']*'|\S+")
_SECRET = re.compile(r"(password|private-key|pre-shared-key|secret|\bkey\b)", re.I)


def _scalar(v):
    if isinstance(v, bool):
        v = "true" if v else "false"
    s = str(v)
    if "'" in s:
        raise AnsibleFilterError("single quote in value %r is not supported" % s)
    return "'%s'" % s


def _walk(node, path, out):
    if node is None or node == {} or node == []:
        out.append(" ".join(path))
    elif isinstance(node, dict):
        for k, v in node.items():
            _walk(v, path + [str(k)], out)
    elif isinstance(node, (list, tuple)):
        for item in node:
            out.append(" ".join(path + [_scalar(item)]))
    else:
        out.append(" ".join(path + [_scalar(node)]))


def vyos_flatten(tree):
    if not isinstance(tree, dict):
        raise AnsibleFilterError("vyos_flatten expects a dict")
    out = []
    _walk(tree, ["set"], out)
    return out


def _norm(line):
    return line.replace("'", "").strip()


def _section(line):
    toks = line.split(None, 2)
    return toks[1] if len(toks) > 1 else ""


def vyos_plan(desired, running, managed, protected=None):
    """Compute the set/delete lines that reconcile `managed` sections."""
    managed = set(managed)
    protected_re = [re.compile(p) for p in (protected or [])]

    if isinstance(running, str):
        running = running.splitlines()
    running = [l.strip() for l in running if l.strip().startswith("set ")]

    run_managed = {}
    for l in running:
        if _section(l) in managed:
            run_managed[_norm(l)] = l
    des = {}
    for l in desired:
        if _section(l) in managed:
            des[_norm(l)] = l

    def is_protected(l):
        return any(p.search(l) for p in protected_re)

    keep = set(des) | {n for n, l in run_managed.items() if is_protected(l)}
    removed = {n: l for n, l in run_managed.items() if n not in keep}
    to_set = [l for n, l in des.items() if n not in run_managed]

    # Collapse deletes: delete the highest ancestor whose whole subtree is being removed.
    def toks(l):
        return _TOKEN.findall(l)[1:]  # drop leading 'set'

    total, gone = {}, {}
    for n, l in run_managed.items():
        t = toks(l)
        for i in range(1, len(t) + 1):
            k = tuple(_norm(x) for x in t[:i])
            total[k] = total.get(k, 0) + 1
            if n in removed:
                gone[k] = gone.get(k, 0) + 1

    deletes = []
    for n, l in removed.items():
        t = toks(l)
        best = len(t)
        for i in range(2, len(t)):  # never collapse above <section> <child>
            k = tuple(_norm(x) for x in t[:i])
            if gone.get(k) == total.get(k):
                best = i
                break
        d = "delete " + " ".join(t[:best])
        if d not in deletes:
            deletes.append(d)

    return {"set": to_set, "delete": deletes}


def vyos_mask(lines):
    out = []
    for l in lines:
        if _SECRET.search(l):
            l = re.sub(r"'[^']*'\s*$", "'********'", l)
        out.append(l)
    return out


class FilterModule(object):
    def filters(self):
        return {
            "vyos_flatten": vyos_flatten,
            "vyos_plan": vyos_plan,
            "vyos_mask": vyos_mask,
        }
