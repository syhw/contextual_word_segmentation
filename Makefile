all:
	### First extract .cha to .txt and cut them into documents, put them into
	### the folder 'ProvidenceResegmented'
	### we also assume that you have:
	###  - 'phonology_dict/filterWords.txt'
	###  - 'phonology_dict/words.txt'
	###  - 'phonology_dict/phoneSet'
	python src/prepare_corpus.py
	### edit the next file depending on which LDA model you want to use
	python src/prefix_sentences_by_docs.py ProvidenceResegmented/all_1min.txt
	### you need the 'phonology_dict' folder stuffed
	python src/text_to_phon.py ProvidenceResegmented/all_1min_docs_reseg_lemmatized.txt
	python src/split_sin < naima_docs_11to22m.sin > naima_docs_11to22m.ylt
	python src/write_grammar.py naima_docs_11to22m.ylt all_1min_doc_topics_reseg_lemmatized.pickle # writes grammar.lt
	# now you need the py-cfg adaptor grammar compiled and in py-cfg
	./launch_adaptor.sh
	python mark_scripts/topicsandcollocations/trees-words.py -c "^Word" -i "^_d" < output.prs > output.seg
	python ben_scripts/eval.py -g naima_11to22m.gold < output_cluster.seg
