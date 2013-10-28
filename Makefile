all:
	### First extract .cha to .txt and cut them into documents, put them into
	### the folder 'ProvidenceFinal/ToSegment'
	mkdir -p ProvidenceFinal/OverSeg
	sed -e s/@?/@/ ProvidenceFinal/ToSegment/*.txt > ProvidenceFinal/OverSeg/all_over_seg.txt
	python src/prepare_corpus_tfidf.py ProvidenceFinal/OverSeg/
	python src/split_corpus.py ProvidenceFinal/ToSegment
	mkdir -p ProvidenceFinal/Final
	cp ProvidenceFinal/ToSegment/*_final_split.txt ProvidenceFinal/Final/
	### we also assume that you have:
	###  - 'phonology_dict/filterWords.txt'
	###  - 'phonology_dict/words.txt'
	###  - 'phonology_dict/phoneSet'
	#python src/prepare_corpus.py
	python src/prepare_corpus_tfidf.py ProvidenceFinal/Final/
	### edit the next file depending on which LDA model you want to use
	python src/prefix_sentences_by_docs.py ProvidenceFinal/Final/all_final_seg.txt
	### you need the 'phonology_dict' folder stuffed
	python src/text_to_phon.py ProvidenceFinal/Final/all_1min_doc_prefixed_reseg_lemmatized.txt
	python src/split_sin.py < naima_docs_11to22m.sin > naima_docs_11to22m.ylt
	python src/write_grammar.py naima_docs_11to22m.ylt ProvidenceFinal/Final/all_1min_doc_topics_reseg_lemmatized.pickle # writes grammar.lt
	# now you need the py-cfg adaptor grammar compiled and in py-cfg
	./launch_adaptor.sh
	python scripts/trees-words.py -c "^Word" -i "^_d" < output.prs > output.seg
	python scripts/eval.py -g Naima_11to22m.gold < output.seg
