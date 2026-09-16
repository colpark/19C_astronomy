#!/usr/bin/env bash
# usage: queue_cli.sh <skill-copy-dir>
Q="$1/scripts/queue.py"
run() { echo "\$ python3 scripts/queue.py $*"; python3 "$Q" "$@" 2>&1; echo "[exit=$?]"; echo; }
run --counted 40 --passed 13 --survivors 7 --target 10 --remaining 200
run --counted 6 --passed 1 --survivors 1 --target 10
run --counted 250 --passed 9 --survivors 9 --target 100
run --counted 30 --passed 1 --survivors 1 --target 100
run --counted 1071 --passed 1071 --survivors 535 --target 600
run --counted 1072 --passed 1072 --survivors 520 --target 600
run --counted 11183 --passed 7154 --survivors 7154 --target 100
run --counted 11183 --passed 7154 --survivors 7154 --target 8000 --remaining 20000
run --counted 100000 --passed 1 --survivors 1 --target 10 --remaining 1000000
