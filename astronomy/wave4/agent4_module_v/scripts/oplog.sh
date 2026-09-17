#!/bin/bash
# usage: oplog.sh "message" [file_to_hash...]
D=/home/aid1/Documents/4_19C_astronomy/repo/astronomy/wave4/agent4_module_v
msg="$1"; shift
line="$(date -u +%Y-%m-%dT%H:%M:%SZ) | $msg"
for f in "$@"; do line="$line | sha256:$(sha256sum "$f" | cut -c1-64) $f"; done
echo "$line" >> $D/order_of_operations.log
