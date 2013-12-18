CHILD=naima
SAGE=0 # TODO
EAGE=21 # TODO
list_of_grammars=$(shell echo $(CHILD)_*.lt) # topic-based (b/c "_") grammars

prepare:
	./all_preparation.sh # TODO


generate_grammars:
	python src/write_grammar.py $(CHILD)_docs_11to22m.ylt ProvidenceFinal/Final/all_doc_topics_reseg_lemmatized_tfidf.pickle $(CHILD) # writes $(CHILD).lt
	python src/write_grammar.py $(CHILD)_docs_11to22m.ylt ProvidenceFinal/Final/all_doc_topics_reseg_lemmatized_tfidf.pickle -a $(CHILD) # writes $(CHILD)_readapt.lt
	python src/write_grammar.py $(CHILD)_docs_11to22m.ylt ProvidenceFinal/Final/all_doc_topics_reseg_lemmatized_tfidf.pickle -d $(CHILD) # writes $(CHILD)_doc_colloc.lt
	python src/write_grammar.py $(CHILD)_docs_11to22m.ylt ProvidenceFinal/Final/all_doc_topics_reseg_lemmatized_tfidf.pickle -t $(CHILD) # writes $(CHILD)_topics_colloc.lt
	python src/write_grammar.py $(CHILD)_docs_11to22m.ylt ProvidenceFinal/Final/all_doc_topics_reseg_lemmatized_tfidf.pickle -s $(CHILD) # writes $(CHILD)_syll.lt
	python src/write_grammar.py $(CHILD)_docs_11to22m.ylt ProvidenceFinal/Final/all_doc_topics_reseg_lemmatized_tfidf.pickle -a -d $(CHILD) # writes $(CHILD)_readapt_doc_colloc.lt
	python src/write_grammar.py $(CHILD)_docs_11to22m.ylt ProvidenceFinal/Final/all_doc_topics_reseg_lemmatized_tfidf.pickle -a -t $(CHILD) # writes $(CHILD)_readapt_topics_colloc.lt
	python src/write_grammar.py $(CHILD)_docs_11to22m.ylt ProvidenceFinal/Final/all_doc_topics_reseg_lemmatized_tfidf.pickle -a -s $(CHILD) # writes $(CHILD)_readapt_syll.lt
	python src/write_grammar.py $(CHILD)_docs_11to22m.ylt ProvidenceFinal/Final/all_doc_topics_reseg_lemmatized_tfidf.pickle -a -d -s $(CHILD) # writes $(CHILD)_readapt_doc_colloc_syll.lt
	python src/write_grammar.py $(CHILD)_docs_11to22m.ylt ProvidenceFinal/Final/all_doc_topics_reseg_lemmatized_tfidf.pickle -a -t -s $(CHILD) # writes $(CHILD)_readapt_topics_colloc_syll.lt
	python src/write_grammar.py $(CHILD)_docs_11to22m.ylt ProvidenceFinal/Final/all_doc_topics_reseg_lemmatized_tfidf.pickle -d -s $(CHILD) # writes $(CHILD)_doc_colloc_syll.lt
	python src/write_grammar.py $(CHILD)_docs_11to22m.ylt ProvidenceFinal/Final/all_doc_topics_reseg_lemmatized_tfidf.pickle -t -s $(CHILD) # writes $(CHILD)_topics_colloc_syll.lt


basic_AGs:
	./launch_unigram.sh $(CHILD)_11to22m
	./launch_colloc.sh $(CHILD)_11to22m


%.prs: %.lt
	./launch_adaptor.sh $(subst .lt,,$<) $(CHILD)_docs_11to22m
	python scripts/trees-words.py -c "^Word" -i "^_d" < $@ > $(subst .prs,.seg,$@)
	python scripts/eval.py -g $(CHILD)_11to22m.gold < $(subst .prs,.seg,$@)


all: generate_grammars $(subst .lt,.prs,$(list_of_grammars))
	@echo "generating all grammars:"
	@echo "$(list_of_grammars)"

