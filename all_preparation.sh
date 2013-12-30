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
### change "nai" here for another kid if you'd like:
for name in `ls ProvidenceFinal/Final/nai_docs_*.txt`;
do
    python src/text_to_phon.py $name;
    python src/split_sin.py < ${name%.*}.sin > ${name%.*}.ylt;
done;
cat ProvidenceFinal/Final/nai_docs_1*.ylt ProvidenceFinal/Final/nai_docs_20.ylt ProvidenceFinal/Final/nai_docs_21.ylt ProvidenceFinal/Final/nai_docs_22.ylt > naima_docs_11to22m.ylt
python src/write_grammar.py naima_docs_11to22m.ylt ProvidenceFinal/Final/*_doc_topics_reseg_lemmatized_tfidf.pickle # writes grammar.lt
### now you need the py-cfg adaptor grammar compiled and in py-cfg
# use the Makefile, the workflow looks like:
#./launch_adaptor.sh
#python scripts/trees-words.py -c "^Word" -i "^_d" < output.prs > output.seg
#python scripts/eval.py -g naima_11to22m.gold < output.seg
