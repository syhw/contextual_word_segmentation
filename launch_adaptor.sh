# the syntax is ./launch_adaptor.sh py-cfg_software grammar_type input_name_pattern gold_name_pattern output_folder
${1} -n 500 -G ${5}/${2}.wlt -A ${5}/${2}.prs -F ${5}/${2}.trace -x 1 -E -d 101 -a 0.0001 -b 10000 -e 1 -f 1 -g 100 -h 0.001 -R -1 -Y "cat > ${5}/${2}.samples" -P ${2}.lt < ${5}/${3}.ylt
python scripts/trees-words.py -c "^Word" -i "^_d" < ${5}/${2}.prs > ${5}/${2}.seg
python scripts/eval.py -g ${5}/${4}.gold < ${5}/${2}.seg
