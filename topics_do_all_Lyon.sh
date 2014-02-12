#!/bin/bash
echo ">>> usage: ./topics_do_all_Lyon.sh child_name,"
echo "e.g. ./topics_do_all_Lyon.sh ana"
echo "This scripts segments all LyonFinal/ToSegment/*.txt into documents"
echo "based on the KL-divergence with topics learned from over-segmentation,"
echo "and then relearns a topics model."
if [[ "$#" -ne 1 ]]; then
    echo "ERROR: you must specify a child name as argument"
    exit
fi
echo "==> We will do that for the child $1"
echo "-----------------------------------------"
chi=$(echo "$1" | cut -c 1-3)
### First extract .cha to .txt to cut them into documents, put them into
### the folder 'LyonFinal/ToSegment'
mkdir -p LyonFinal/OverSeg
sed -e s/@?/@/ LyonFinal/ToSegment/segmented_w_age.txt > LyonFinal/OverSeg/segmented_w_age_over_seg.txt
python src/prepare_corpus_tfidf.py LyonFinal/OverSeg/ --fr
python src/split_corpus.py LyonFinal/ToSegment/segmented_w_age.txt --fr
mkdir -p LyonFinal/Final
cp LyonFinal/ToSegment/*_final_split.txt LyonFinal/Final/
### we also assume that you have:
###  - 'phonology_dict/filterWords.txt'
###  - 'phonology_dict/words.txt'
###  - 'phonology_dict/phoneSet'
python src/prepare_corpus_tfidf.py LyonFinal/Final/ --fr &>LyonFinal/topics.txt
### edit the next file depending on which LDA model you want to use
### this also splits in kids name and months
python src/prefix_sentences_by_docs.py LyonFinal/Final/*_final_split.txt --fr
### optional, cuts sentences that are too long (see inside the *.py for params)
python src/cut_too_long.py LyonFinal/Final/${chi}_
### you need the 'phonology_dict' folder stuffed
for name in `ls LyonFinal/Final/${chi}_docs_*.txt`;
do
    python src/text_to_phon_fr.py $name;
    python src/split_sin.py < ${name%.*}.sin > ${name%.*}.ylt;
done;
cat LyonFinal/Final/${chi}_docs_1*.ylt LyonFinal/Final/${chi}_docs_20.ylt LyonFinal/Final/${chi}_docs_21.ylt LyonFinal/Final/${chi}_docs_23.ylt > $1_docs_11to23m.ylt
cat LyonFinal/Final/${chi}_docs_1*.sin LyonFinal/Final/${chi}_docs_20.sin LyonFinal/Final/${chi}_docs_21.sin LyonFinal/Final/${chi}_docs_23.sin > $1_docs_11to23m.sin
for name in `ls LyonFinal/Final/${chi}_topic_*.txt`;
do
    python src/text_to_phon_fr.py $name;
    python src/split_sin.py < ${name%.*}.sin > ${name%.*}.ylt;
done;
cat LyonFinal/Final/${chi}_topic_1*.ylt LyonFinal/Final/${chi}_topic_20.ylt LyonFinal/Final/${chi}_topic_21.ylt LyonFinal/Final/${chi}_topic_23.ylt > $1_topic_11to23m.ylt
cat LyonFinal/Final/${chi}_topic_1*.sin LyonFinal/Final/${chi}_topic_20.sin LyonFinal/Final/${chi}_topic_21.sin LyonFinal/Final/${chi}_topic_23.sin > $1_topic_11to23m.sin
cut -d " " -f 2- $1_docs_11to22m.sin > $1_11to22m.gold
#cut -d " " -f 2- $1_topic_11to22m.sin > $1_11to22m.gold ### useless

python src/write_grammar.py $1_docs_11to22m.ylt LyonFinal/Final/*_doc_topics_lemmatized_tfidf.pickle # writes grammar.lt
### now you need the py-cfg adaptor grammar compiled and in py-cfg
# use the Makefile, the workflow looks like:
#./launch_adaptor.sh
#python scripts/trees-words.py -c "^Word" -i "^_d" < output.prs > output.seg
#python scripts/eval.py -g $1_11to22m.gold < output.seg
