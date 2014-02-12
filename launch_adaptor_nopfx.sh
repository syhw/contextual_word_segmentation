# the syntax is ./launch_adaptor_nopfx.sh py-cfg_software grammar_type input_name_pattern gold_name_pattern output_folder number_of_iterations
${1} -n ${6} -G ${5}/${2}_${6}.wlt -A ${5}/${2}_${6}.prs -F ${5}/${2}_${6}.trace -x 1 -E -d 101 -a 0.0001 -b 10000 -e 1 -f 1 -g 100 -h 0.001 -R -1 -Y "bzip2 -9 > ${5}/${2}_${6}.samples.bz2" -P ${2}.lt -u ${5}/${3}_nopfx.ylt -U "./inline_eval_nopfx.sh ${5}/${3}_test" < ${5}/${3}_train.ylt

