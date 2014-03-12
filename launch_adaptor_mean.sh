#!/bin/bash
${1} -n ${6} -G ${5}/${2}_${6}.wlt -A ${5}/${2}_${6}.prs -F ${5}/${2}_${6}.trace -E -d 101 -a 0.0001 -b 10000 -e 1 -f 1 -g 100 -h 0.01 -R -1 -x 10 -X "bash -c ' tee >(./dump_trees.sh ${5}/${2}_${6}.trsws ${6}) | ./inline_eval.sh ${5}/${4} '" -P ${2}.lt < ${5}/${3}.ylt

