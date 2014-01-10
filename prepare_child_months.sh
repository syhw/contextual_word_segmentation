#!/bin/bash
# usage: ./prepare_child_months.sh $CHILD $START_AGE $END_AGE
folder=$1_$2to$3m
mkdir $folder
chi=$(echo "$1" | cut -c 1-3)
l_ylt=(ProvidenceFinal/Final/${chi}_docs_$2.ylt);
l_sin=(ProvidenceFinal/Final/${chi}_docs_$2.sin);
month=$2
while [ $month -le $3 ]; do
    month=$(($month+1))
    l_ylt+=(ProvidenceFinal/Final/nai_docs_$month.ylt)
    l_sin+=(ProvidenceFinal/Final/nai_docs_$month.sin)
done
echo ${l_ylt[@]}
echo ${l_sin[@]}
cat ${l_ylt[@]} > ${folder}/$1_docs_$2to$3m.ylt
cat ${l_sin[@]} > ${folder}/$1_docs_$2to$3m.sin
cut -d " " -f 2- ${folder}/$1_docs_$2to$3m.sin > ${folder}/${folder}.gold
cut -d " " -f 2- ${folder}/$1_docs_$2to$3m.ylt > ${folder}/${folder}.ylt
