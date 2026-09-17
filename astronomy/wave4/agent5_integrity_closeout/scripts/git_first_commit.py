#!/usr/bin/env python3
"""Derive, without running git, for each given path: whether HEAD's tree contains it, the earliest
commit (by committer timestamp, over all commits reachable from HEAD) whose tree contains it,
that commit's blob id, and whether the working-tree bytes equal the HEAD blob.
Reads loose objects from .git/objects with zlib only. Fails loudly on packfiles (none present).
usage: git_first_commit.py <repo-relative path>...   -> JSON on stdout"""
import os, sys, zlib, json, hashlib
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
G = os.path.join(ROOT, ".git")
def obj(sha):
    p = os.path.join(G, "objects", sha[:2], sha[2:])
    if not os.path.exists(p): raise SystemExit(f"object {sha} not loose (packfile?); not derivable by this script")
    raw = zlib.decompress(open(p, "rb").read()); hdr, _, body = raw.partition(b"\0")
    return hdr.split(b" ")[0].decode(), body
def head():
    ref = open(os.path.join(G, "HEAD")).read().strip()
    return open(os.path.join(G, ref[5:])).read().strip() if ref.startswith("ref: ") else ref
def commit(sha):
    t, b = obj(sha); assert t == "commit"
    tree, parents, ts = None, [], None
    for line in b.split(b"\n\n", 1)[0].split(b"\n"):
        k, _, v = line.partition(b" ")
        if k == b"tree": tree = v.decode()
        elif k == b"parent": parents.append(v.decode())
        elif k == b"committer": ts = int(v.split(b" ")[-2])
    return tree, parents, ts
def tree_entries(sha):
    t, b = obj(sha); assert t == "tree"; out = {}; i = 0
    while i < len(b):
        sp = b.index(b" ", i); nul = b.index(b"\0", sp)
        mode = b[i:sp].decode(); name = b[sp+1:nul].decode(); out[name] = (mode, b[nul+1:nul+21].hex()); i = nul + 21
    return out
_cache = {}
def lookup(tree, path):
    cur = tree
    for part in path.split("/"):
        key = (cur,)
        if key not in _cache: _cache[key] = tree_entries(cur)
        e = _cache[key].get(part)
        if e is None: return None
        cur = e[1]
    return cur
def blob_id(p):
    data = open(p, "rb").read(); return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()
h = head(); seen, stack, commits = set(), [h], []
while stack:
    c = stack.pop()
    if c in seen: continue
    seen.add(c); tree, parents, ts = commit(c); commits.append((ts, c, tree)); stack.extend(parents)
commits.sort()
res = {"head": h, "commits_reachable": len(commits), "paths": {}}
head_tree = commit(h)[0]
for path in sys.argv[1:]:
    first = next(((ts, c, b) for ts, c, t in commits for b in [lookup(t, path)] if b), None)
    hb = lookup(head_tree, path); wp = os.path.join(ROOT, path)
    res["paths"][path] = {
        "in_head_tree": hb is not None, "head_blob": hb,
        "working_tree_equals_head_blob": (blob_id(wp) == hb) if (hb and os.path.exists(wp)) else None,
        "first_commit": first[1] if first else None, "first_commit_committer_epoch": first[0] if first else None,
        "first_commit_blob": first[2] if first else None,
        "distinct_blobs_in_history": len({b for ts, c, t in commits for b in [lookup(t, path)] if b})}
print(json.dumps(res, indent=1))
