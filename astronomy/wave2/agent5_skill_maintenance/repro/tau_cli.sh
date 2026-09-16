#!/usr/bin/env bash
# usage: tau_cli.sh <skill-copy-dir>; run from agent5_skill_maintenance/
T="$1/scripts/tau.py"
for c in flat flat_with_sep saturating late_jump sep_holds sep_collapsed_at_sat sep_never_collapses astronomy_agent1_curve; do
  echo "\$ python3 scripts/tau.py --curve repro/tau/$c.csv"; python3 "$T" --curve repro/tau/$c.csv 2>&1; echo "[exit=$?]"; echo
done
