#!/bin/bash
cd "$(dirname "$0")/.." ; P=/tmp/claude-1000/-home-aid1-Documents-4-19C-astronomy/addb1fc3-63d3-4989-8753-aa4c400b100e/scratchpad/venv/bin/python
export W3_THREADS=1 W3_RETRIES=6 W3_BACKOFF=60
$P scripts/w3_enumerate.py w3_c3 20260701 20260916 61222.000428 61300 > out/w3_c3_resume.stdout 2>&1
$P scripts/w3_enumerate.py w3_p60 20260501 20260701 61162.000428 61222.000428 > out/w3_p60_resume.stdout 2>&1
$P scripts/w3_enumerate.py w3_c5 20260224 20260502 61095.000428 61162.000428 61222.000428 > out/w3_c5_resume.stdout 2>&1
echo done > out/w3_resume.done
