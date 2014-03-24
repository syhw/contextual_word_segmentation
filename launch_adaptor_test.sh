# the syntax is ./launch_adaptor_test.sh py-cfg_software grammar_type input_name_pattern gold_name_pattern output_folder number_of_iterations
### perl -n -e 'print if (rand() < .2)' < ${5}/${3}.ylt > ${5}/test_${3}.ylt
echo "launch_adaptor_test with params ${1} ${2} ${3} ${4} ${5} ${6}\n"
${1} -n ${6} -G ${5}/${2}_${6}_test.wlt -A ${5}/${2}_${6}_test.prs -F ${5}/${2}_${6}_test.trace -x 1 -E -d 101 -a 0.0001 -b 10000 -e 1 -f 1 -g 100 -h 0.01 -R -1 -Y "bzip2 -9 > ${5}/${2}_${6}.samples.bz2" -P ${2}.lt -u ${5}/${3}_test.ylt -U "./inline_eval.sh ${5}/${4}_test" < ${5}/${3}_train.ylt
