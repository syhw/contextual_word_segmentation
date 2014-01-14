#!/bin/bash
echo ">>> usage: ./topics_do_all.sh CHILD_NAME, e.g. ./topics_do_all.sh naima"
echo "This scripts segments all ProvidenceFinal/ToSegment/*.txt into documents"
echo "based on the KL-divergence with topics learned from over-segmentation,"
echo "and then relearns a topics model."
echo "-----------------------------------------"
chi=$(echo "$1" | cut -c 1-3)
### First extract .cha to .txt to cut them into documents, put them into
### the folder 'ProvidenceFinal/ToSegment' (alternatively use Lan's docs split)
mkdir -p ProvidenceFinal/OverSeg
sed -e s/@?/@/ ProvidenceFinal/ToSegment/*.txt > ProvidenceFinal/OverSeg/all_over_seg.txt
python src/prepare_corpus_tfidf.py ProvidenceFinal/OverSeg/
python src/split_corpus.py ProvidenceFinal/ToSegment/*.txt
mkdir -p ProvidenceFinal/Final
cp ProvidenceFinal/ToSegment/*_final_split.txt ProvidenceFinal/Final/
### we also assume that you have:
###  - 'phonology_dict/filterWords.txt'
###  - 'phonology_dict/words.txt'
###  - 'phonology_dict/phoneSet'
python src/prepare_corpus_tfidf.py ProvidenceFinal/Final/
### edit the next file depending on which LDA model you want to use
### this also splits in kids name and months
python src/prefix_sentences_by_docs.py ProvidenceFinal/Final/*_final_split.txt
### you need the 'phonology_dict' folder stuffed
for name in `ls ProvidenceFinal/Final/${chi}_docs_*.txt`;
do
    python src/text_to_phon.py $name;
    python src/split_sin.py < ${name%.*}.sin > ${name%.*}.ylt;
done;
cat ProvidenceFinal/Final/${chi}_docs_1*.ylt ProvidenceFinal/Final/${chi}_docs_20.ylt ProvidenceFinal/Final/${chi}_docs_21.ylt ProvidenceFinal/Final/${chi}_docs_22.ylt > $1_docs_11to22m.ylt
cat ProvidenceFinal/Final/${chi}_docs_1*.sin ProvidenceFinal/Final/${chi}_docs_20.sin ProvidenceFinal/Final/${chi}_docs_21.sin ProvidenceFinal/Final/${chi}_docs_22.sin > $1_docs_11to22m.sin
for name in `ls ProvidenceFinal/Final/${chi}_topic_*.txt`;
do
    python src/text_to_phon.py $name;
    python src/split_sin.py < ${name%.*}.sin > ${name%.*}.ylt;
done;
cat ProvidenceFinal/Final/${chi}_topic_1*.ylt ProvidenceFinal/Final/${chi}_topic_20.ylt ProvidenceFinal/Final/${chi}_topic_21.ylt ProvidenceFinal/Final/${chi}_topic_22.ylt > $1_topic_11to22m.ylt
cat ProvidenceFinal/Final/${chi}_topic_1*.sin ProvidenceFinal/Final/${chi}_topic_20.sin ProvidenceFinal/Final/${chi}_topic_21.sin ProvidenceFinal/Final/${chi}_topic_22.sin > $1_topic_11to22m.sin
cut -d " " -f 2- $1_docs_11to22m.sin > $1_11to22m.gold
#cut -d " " -f 2- $1_topic_11to22m.sin > $1_11to22m.gold ### useless

python src/write_grammar.py $1_docs_11to22m.ylt ProvidenceFinal/Final/*_doc_topics_reseg_lemmatized_tfidf.pickle # writes grammar.lt
### now you need the py-cfg adaptor grammar compiled and in py-cfg
# use the Makefile, the workflow looks like:
#./launch_adaptor.sh
#python scripts/trees-words.py -c "^Word" -i "^_d" < output.prs > output.seg
#python scripts/eval.py -g $1_11to22m.gold < output.seg
