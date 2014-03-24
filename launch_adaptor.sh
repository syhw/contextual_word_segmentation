# the syntax is ./launch_adaptor.sh py-cfg_software grammar_type input_name_pattern gold_name_pattern output_folder number_of_iterations
echo "launch_adaptor with params ${1} ${2} ${3} ${4} ${5} ${6}\n"
${1} -n ${6} -G ${5}/${2}_${6}.wlt -A ${5}/${2}_${6}.prs -F ${5}/${2}_${6}.trace -x 1 -E -d 101 -a 0.0001 -b 10000 -e 1 -f 1 -g 100 -h 0.01 -R -1 -Y "bzip2 -9 > ${5}/${2}_${6}.samples.bz2" -P ${2}.lt < ${5}/${3}.ylt
python scripts/trees-words.py -c "^Word" -i "^(_d|_t)" < ${5}/${2}_${6}.prs > ${5}/${2}_${6}.seg
python scripts/eval.py -g ${5}/${4}.gold < ${5}/${2}_${6}.seg
