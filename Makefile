CHILD=naima
CHI=$(shell echo $(CHILD) | cut -c 1-3)
SAGE=11
EAGE=22
NITER=10
QUEUE=all.q
PY_CFG=./py-cfg/py-cfg
list_of_grammars=$(shell echo $(CHILD)_$(SAGE)to$(EAGE)m_*.lt)


all:
	# make prepare_topics has still to be done by hand (once for all)
	@echo ">>> creating the $(CHILD)_$(SAGE)to$(EAGE)m folder with needed data"
	$(MAKE) $(CHILD)_$(SAGE)to$(EAGE)m
	@echo ">>> launching basic grammars"
	$(MAKE) basic_AGs
	@echo ">>> launching single context ("_sc") grammars"
	$(MAKE) single_context_AGs
	@echo ">>> generating all grammars as once"
	$(MAKE) generate_grammars
	@echo ">>> now launching adaptor grammars jobs using all those grammars:"
	$(MAKE) launch_jobs


prepare_topics:
	./topics_do_all.sh $(CHILD)


remove_long_lines:
	# and now a hack to remove too long lines, UNCHECKED!!!
	mv $(CHILD)_docs_$(SAGE)to$(EAGE)m.ylt full_$(CHILD)_docs_$(SAGE)to$(EAGE)m.ylt
	mv $(CHILD)_$(SAGE)to$(EAGE)m.gold full_$(CHILD)_$(SAGE)to$(EAGE)m.gold
	awk 'length<=600' full_$(CHILD)_docs_$(SAGE)to$(EAGE)m.ylt > $(CHILD)_docs_$(SAGE)to$(EAGE)m.ylt
	awk 'length<=300' full_$(CHILD)_$(SAGE)to$(EAGE)m.gold > $(CHILD)_$(SAGE)to$(EAGE)m.gold


generate_grammars:
	# TODO remove * in *_doc_topics_reseg_lemmatized_tfidf.pickle
	python src/write_grammar.py $(CHILD)_$(SAGE)to$(EAGE)m/$(CHILD)_docs_$(SAGE)to$(EAGE)m.ylt ProvidenceFinal/Final/*_doc_topics_reseg_lemmatized_tfidf.pickle $(CHILD)_$(SAGE)to$(EAGE)m # writes $(CHILD)_$(SAGE)to$(EAGE)m.lt
	python src/write_grammar.py $(CHILD)_$(SAGE)to$(EAGE)m/$(CHILD)_docs_$(SAGE)to$(EAGE)m.ylt ProvidenceFinal/Final/*_doc_topics_reseg_lemmatized_tfidf.pickle -a $(CHILD)_$(SAGE)to$(EAGE)m # writes $(CHILD)_$(SAGE)to$(EAGE)m_readapt.lt
	python src/write_grammar.py $(CHILD)_$(SAGE)to$(EAGE)m/$(CHILD)_docs_$(SAGE)to$(EAGE)m.ylt ProvidenceFinal/Final/*_doc_topics_reseg_lemmatized_tfidf.pickle -d $(CHILD)_$(SAGE)to$(EAGE)m # writes $(CHILD)_$(SAGE)to$(EAGE)m_doc_colloc.lt
	python src/write_grammar.py $(CHILD)_$(SAGE)to$(EAGE)m/$(CHILD)_docs_$(SAGE)to$(EAGE)m.ylt ProvidenceFinal/Final/*_doc_topics_reseg_lemmatized_tfidf.pickle -t $(CHILD)_$(SAGE)to$(EAGE)m # writes $(CHILD)_$(SAGE)to$(EAGE)m_topics_colloc.lt
	python src/write_grammar.py $(CHILD)_$(SAGE)to$(EAGE)m/$(CHILD)_docs_$(SAGE)to$(EAGE)m.ylt ProvidenceFinal/Final/*_doc_topics_reseg_lemmatized_tfidf.pickle -s $(CHILD)_$(SAGE)to$(EAGE)m # writes $(CHILD)_$(SAGE)to$(EAGE)m_syll.lt
	python src/write_grammar.py $(CHILD)_$(SAGE)to$(EAGE)m/$(CHILD)_docs_$(SAGE)to$(EAGE)m.ylt ProvidenceFinal/Final/*_doc_topics_reseg_lemmatized_tfidf.pickle -a -d $(CHILD)_$(SAGE)to$(EAGE)m # writes $(CHILD)_$(SAGE)to$(EAGE)m_readapt_doc_colloc.lt
	python src/write_grammar.py $(CHILD)_$(SAGE)to$(EAGE)m/$(CHILD)_docs_$(SAGE)to$(EAGE)m.ylt ProvidenceFinal/Final/*_doc_topics_reseg_lemmatized_tfidf.pickle -a -t $(CHILD)_$(SAGE)to$(EAGE)m # writes $(CHILD)_$(SAGE)to$(EAGE)m_readapt_topics_colloc.lt
	python src/write_grammar.py $(CHILD)_$(SAGE)to$(EAGE)m/$(CHILD)_docs_$(SAGE)to$(EAGE)m.ylt ProvidenceFinal/Final/*_doc_topics_reseg_lemmatized_tfidf.pickle -a -s $(CHILD)_$(SAGE)to$(EAGE)m # writes $(CHILD)_$(SAGE)to$(EAGE)m_readapt_syll.lt
	python src/write_grammar.py $(CHILD)_$(SAGE)to$(EAGE)m/$(CHILD)_docs_$(SAGE)to$(EAGE)m.ylt ProvidenceFinal/Final/*_doc_topics_reseg_lemmatized_tfidf.pickle -a -d -s $(CHILD)_$(SAGE)to$(EAGE)m # writes $(CHILD)_$(SAGE)to$(EAGE)m_readapt_doc_colloc_syll.lt
	python src/write_grammar.py $(CHILD)_$(SAGE)to$(EAGE)m/$(CHILD)_docs_$(SAGE)to$(EAGE)m.ylt ProvidenceFinal/Final/*_doc_topics_reseg_lemmatized_tfidf.pickle -a -t -s $(CHILD)_$(SAGE)to$(EAGE)m # writes $(CHILD)_$(SAGE)to$(EAGE)m_readapt_topics_colloc_syll.lt
	python src/write_grammar.py $(CHILD)_$(SAGE)to$(EAGE)m/$(CHILD)_docs_$(SAGE)to$(EAGE)m.ylt ProvidenceFinal/Final/*_doc_topics_reseg_lemmatized_tfidf.pickle -d -s $(CHILD)_$(SAGE)to$(EAGE)m # writes $(CHILD)_$(SAGE)to$(EAGE)m_doc_colloc_syll.lt
	python src/write_grammar.py $(CHILD)_$(SAGE)to$(EAGE)m/$(CHILD)_docs_$(SAGE)to$(EAGE)m.ylt ProvidenceFinal/Final/*_doc_topics_reseg_lemmatized_tfidf.pickle -t -s $(CHILD)_$(SAGE)to$(EAGE)m # writes $(CHILD)_$(SAGE)to$(EAGE)m_topics_colloc_syll.lt


$(CHILD)_$(SAGE)to$(EAGE)m:
	./prepare_child_months.sh $(CHILD) $(SAGE) $(EAGE)


basic_AGs: $(CHILD)_$(SAGE)to$(EAGE)m
	cut -d " " -f 2- $(CHILD)_$(SAGE)to$(EAGE)m/$(CHILD)_docs_$(SAGE)to$(EAGE)m.ylt > $(CHILD)_$(SAGE)to$(EAGE)m.ylt
	# for qsub with Open-MPI, use -pe openmpi_ib 8-16
	qsub -N "$(CHI)-$(SAGE)-$(EAGE)-unigram" -q cpu -cwd -o `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m -e `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m launch_adaptor.sh $(PY_CFG) unigram $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(NITER)
	qsub -N "$(CHI)-$(SAGE)-$(EAGE)-colloc" -q cpu -cwd -o `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m -e `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m launch_adaptor.sh $(PY_CFG) colloc $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(NITER)
	qsub -N "$(CHI)-$(SAGE)-$(EAGE)-syll" -q cpu -cwd -o `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m -e `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m launch_adaptor.sh $(PY_CFG) syll $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(NITER)
	qsub -N "$(CHI)-$(SAGE)-$(EAGE)-colloc-syll" -q cpu -cwd -o `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m -e `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m launch_adaptor.sh $(PY_CFG) colloc_syll $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(NITER)


%.prs: %.lt $(CHILD)_$(SAGE)to$(EAGE)m
	qsub -N "$(CHI)-$(SAGE)-$(EAGE)-docs-$(subst .lt,,$<)" -q $(QUEUE) -cwd -o `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m -e `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m launch_adaptor.sh $(PY_CFG) $(subst .lt,,$<) $(CHILD)_docs_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(NITER)
	#qsub -N "$(CHILD)-docs-$(subst .lt,,$<)" -q cpu -cwd launch_adaptor.sh $(PY_CFG) $(subst .lt,,$<) $(CHILD)_splits_docs_$(SAGE)to$(EAGE)m $(CHILD)_splits_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(NITER)


launch_jobs: $(subst .lt,.prs,$(list_of_grammars))
	@echo "$(list_of_grammars)"
	# this rule is just need to expand the list_of_grammars var after generation


single_context_AGs: $(CHILD)_$(SAGE)to$(EAGE)m
	qsub -N "$(CHI)-$(SAGE)-$(EAGE)-unigram-sc" -q $(QUEUE) -cwd -o `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m -e `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m launch_adaptor.sh $(PY_CFG) unigram_sc $(CHILD)_topic_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(NITER)
	qsub -N "$(CHI)-$(SAGE)-$(EAGE)-colloc-sc" -q $(QUEUE) -cwd -o `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m -e `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m launch_adaptor.sh $(PY_CFG) colloc_sc $(CHILD)_topic_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(NITER)
	qsub -N "$(CHI)-$(SAGE)-$(EAGE)-syll-sc" -q $(QUEUE) -cwd -o `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m -e `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m launch_adaptor.sh $(PY_CFG) syll_sc $(CHILD)_topic_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(NITER)
	qsub -N "$(CHI)-$(SAGE)-$(EAGE)-colloc-syll-sc" -q $(QUEUE) -cwd -o `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m -e `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m launch_adaptor.sh $(PY_CFG) colloc_syll_sc $(CHILD)_topic_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(NITER)
	qsub -N "$(CHI)-$(SAGE)-$(EAGE)-unigram-sc-r" -q $(QUEUE) -cwd -o `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m -e `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m launch_adaptor.sh $(PY_CFG) readapt_unigram_sc $(CHILD)_topic_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(NITER)
	qsub -N "$(CHI)-$(SAGE)-$(EAGE)-colloc-sc-r" -q $(QUEUE) -cwd -o `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m -e `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m launch_adaptor.sh $(PY_CFG) readapt_colloc_sc $(CHILD)_topic_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(NITER)
	qsub -N "$(CHI)-$(SAGE)-$(EAGE)-syll-sc-r" -q $(QUEUE) -cwd -o `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m -e `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m launch_adaptor.sh $(PY_CFG) readapt_syll_sc $(CHILD)_topic_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(NITER)
	qsub -N "$(CHI)-$(SAGE)-$(EAGE)-colloc-syll-sc-r" -q $(QUEUE) -cwd -o `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m -e `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m launch_adaptor.sh $(PY_CFG) readapt_colloc_syll_sc $(CHILD)_topic_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(NITER)


clean:
	rm -rf $(CHILD)_$(SAGE)to$(EAGE)m
	rm $(CHILD)_$(SAGE)to$(EAGE)m_*.lt
