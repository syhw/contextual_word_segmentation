#!/bin/bash
echo "launch_adaptor_generic with params ${1} ${2} ${3} ${4} ${5} ${6}\n"
${1} -n ${6} -G ${2}_${6}.wlt -A ${2}_${6}.prs -F ${2}_${6}.trace -E -d 101 -a 0.0001 -b 10000 -e 1 -f 1 -g 100 -h 0.01 -R -1 -x 10 -X "bash -c 'echo Level0; ./inline_eval_generic.sh ${5}/${4} 0'" -X "bash -c 'echo Level1; ./inline_eval_generic.sh ${5}/${4} 1'" -X "bash -c 'echo Level2; ./inline_eval_generic.sh ${5}/${4} 2'" -X "bash -c 'echo Level3; ./inline_eval_generic.sh ${5}/${4} 3'" -P ${2}.lt < ${5}/${3}.ylt

