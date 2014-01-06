CHILD=naima
SAGE=11 # TODO
EAGE=22 # TODO
list_of_grammars=$(shell echo $(CHILD)_*.lt) # topic-based (b/c "_") grammars


prepare:
	# TODO personalize with $(CHILD)
	./all_preparation.sh
	# and now a hack to remove too long lines, UNCHECKED!!!
	mv $(CHILD)_docs_11to22m.ylt full_$(CHILD)_docs_11to22m.ylt
	mv $(CHILD)_11to22m.gold full_$(CHILD)_11to22m.gold
	awk 'length<=600' full_$(CHILD)_docs_11to22m.ylt > $(CHILD)_docs_11to22m.ylt
	awk 'length<=300' full_$(CHILD)_11to22m.gold > $(CHILD)_11to22m.gold


generate_grammars:
	python src/write_grammar.py $(CHILD)_docs_11to22m.ylt ProvidenceFinal/Final/*_doc_topics_reseg_lemmatized_tfidf.pickle $(CHILD) # writes $(CHILD).lt
	python src/write_grammar.py $(CHILD)_docs_11to22m.ylt ProvidenceFinal/Final/*_doc_topics_reseg_lemmatized_tfidf.pickle -a $(CHILD) # writes $(CHILD)_readapt.lt
	python src/write_grammar.py $(CHILD)_docs_11to22m.ylt ProvidenceFinal/Final/*_doc_topics_reseg_lemmatized_tfidf.pickle -d $(CHILD) # writes $(CHILD)_doc_colloc.lt
	python src/write_grammar.py $(CHILD)_docs_11to22m.ylt ProvidenceFinal/Final/*_doc_topics_reseg_lemmatized_tfidf.pickle -t $(CHILD) # writes $(CHILD)_topics_colloc.lt
	python src/write_grammar.py $(CHILD)_docs_11to22m.ylt ProvidenceFinal/Final/*_doc_topics_reseg_lemmatized_tfidf.pickle -s $(CHILD) # writes $(CHILD)_syll.lt
	python src/write_grammar.py $(CHILD)_docs_11to22m.ylt ProvidenceFinal/Final/*_doc_topics_reseg_lemmatized_tfidf.pickle -a -d $(CHILD) # writes $(CHILD)_readapt_doc_colloc.lt
	python src/write_grammar.py $(CHILD)_docs_11to22m.ylt ProvidenceFinal/Final/*_doc_topics_reseg_lemmatized_tfidf.pickle -a -t $(CHILD) # writes $(CHILD)_readapt_topics_colloc.lt
	python src/write_grammar.py $(CHILD)_docs_11to22m.ylt ProvidenceFinal/Final/*_doc_topics_reseg_lemmatized_tfidf.pickle -a -s $(CHILD) # writes $(CHILD)_readapt_syll.lt
	python src/write_grammar.py $(CHILD)_docs_11to22m.ylt ProvidenceFinal/Final/*_doc_topics_reseg_lemmatized_tfidf.pickle -a -d -s $(CHILD) # writes $(CHILD)_readapt_doc_colloc_syll.lt
	python src/write_grammar.py $(CHILD)_docs_11to22m.ylt ProvidenceFinal/Final/*_doc_topics_reseg_lemmatized_tfidf.pickle -a -t -s $(CHILD) # writes $(CHILD)_readapt_topics_colloc_syll.lt
	python src/write_grammar.py $(CHILD)_docs_11to22m.ylt ProvidenceFinal/Final/*_doc_topics_reseg_lemmatized_tfidf.pickle -d -s $(CHILD) # writes $(CHILD)_doc_colloc_syll.lt
	python src/write_grammar.py $(CHILD)_docs_11to22m.ylt ProvidenceFinal/Final/*_doc_topics_reseg_lemmatized_tfidf.pickle -t -s $(CHILD) # writes $(CHILD)_topics_colloc_syll.lt


basic_AGs:
	cut -d " " -f 2- naima_docs_11to22m.ylt > naima_11to22m.ylt
	qsub -N "$(CHILD)-unigram" -q cpu -cwd -pe openmpi_ib 4 launch_unigram.sh $(CHILD)_11to22m
	qsub -N "$(CHILD)-colloc" -q cpu -cwd -pe openmpi_ib 16 launch_colloc.sh $(CHILD)_11to22m
	qsub -N "$(CHILD)-colloc" -q cpu -cwd -pe openmpi_ib 16 launch_syll.sh $(CHILD)_11to22m
	qsub -N "$(CHILD)-colloc" -q cpu -cwd -pe openmpi_ib 16 launch_colloc_syll.sh $(CHILD)_11to22m
	#launch_unigram.sh $(CHILD)_11to22m
	#launch_colloc.sh $(CHILD)_11to22m
	#launch_syll.sh $(CHILD)_11to22m
	#launch_colloc_syll.sh $(CHILD)_11to22m


%.prs: %.lt
	qsub -N "$(CHILD)-docs-$(subst .lt,,$<)" -q cpu -cwd -pe openmpi_ib 4-16 launch_adaptor.sh $(subst .lt,,$<) $(CHILD)_docs_11to22m $(CHILD)_11to22m
	# launch_adaptor.sh $(subst .lt,,$<) $(CHILD)_docs_11to22m
	#qsub -N "$(CHILD)-docs-$(subst .lt,,$<)-results" -q cpu -cwd results.sh $@ $(subst .prs,.seg,$@) $(CHILD)_11to22m.gold
	#python scripts/trees-words.py -c "^Word" -i "^_d" < $@ > $(subst .prs,.seg,$@)
	#python scripts/eval.py -g $(CHILD)_11to22m.gold < $(subst .prs,.seg,$@)


expand: $(subst .lt,.prs,$(list_of_grammars))
	# just need to expand the list_of_grammars var


all: generate_grammars expand 
	@echo "generated and used all grammars:"
	@echo "$(list_of_grammars)"

