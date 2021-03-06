#!/bin/bash
# usage: ./prepare_child_months.sh $CHILD $START_AGE $END_AGE $BASE_FOLDER
folder=$1_$2to$3m
mkdir $folder
chi=$(echo "$1" | cut -c 1-3)
l_ylt=($4/Final/${chi}_docs_$2.ylt);
l_sin=($4/Final/${chi}_docs_$2.sin);
month=$2
while [ $month -le $3 ]; do
    l_ylt+=($4/Final/${chi}_docs_$month.ylt)
    l_sin+=($4/Final/${chi}_docs_$month.sin)
    month=$(($month+1))
done
echo ${l_ylt[@]}
echo ${l_sin[@]}
cat ${l_ylt[@]} > ${folder}/$1_docs_$2to$3m.ylt
cat ${l_sin[@]} > ${folder}/$1_docs_$2to$3m.sin
cut -d " " -f 2- ${folder}/$1_docs_$2to$3m.sin > ${folder}/${folder}.gold
cut -d " " -f 2- ${folder}/$1_docs_$2to$3m.ylt > ${folder}/${folder}.ylt
l_ylt=($4/Final/${chi}_topic_$2.ylt);
l_sin=($4/Final/${chi}_topic_$2.sin);
month=$2
while [ $month -le $3 ]; do
    l_ylt+=($4/Final/${chi}_topic_$month.ylt)
    l_sin+=($4/Final/${chi}_topic_$month.sin)
    month=$(($month+1))
done
echo ${l_ylt[@]}
echo ${l_sin[@]}
cat ${l_ylt[@]} > ${folder}/$1_topic_$2to$3m.ylt
cat ${l_sin[@]} > ${folder}/$1_topic_$2to$3m.sin
cut -d " " -f 2- ${folder}/$1_topic_$2to$3m.sin > ${folder}/${folder}_as_per_topic.gold
cut -d " " -f 2- ${folder}/$1_topic_$2to$3m.ylt > ${folder}/${folder}.ylt
if ! cmp ${folder}/${folder}.gold ${folder}/${folder}_as_per_topic.gold
then
    echo "***********************************************"
    echo "both ${folder}/${folder}*.gold files differ !!!"
    echo "***********************************************"
else
    echo "both ${folder}/${folder}*.gold files are the same."
fi
