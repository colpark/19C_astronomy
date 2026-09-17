#!/bin/bash
# usage: rd.sh <id> <startline> <endline>  -> prints "p<page> L<line>: text", runs of 3+ spaces shown as " || " (column break); blank lines skipped
F=/home/aid1/Documents/4_19C_astronomy/repo/astronomy/wave5_shape/agent1_census_shape/sources/$1.layout.txt
awk -v a=$2 -v b=$3 'BEGIN{p=1} {n=gsub(/\f/,""); p+=n; line=$0; if(NR>=a && NR<=b){ gsub(/^[ \t]+/,"",line); gsub(/[ \t][ \t][ \t]+/," || ",line); gsub(/[ \t]+/," ",line); if(line ~ /[^ ]/) print "p" p " L" NR ":" line } }' "$F"
