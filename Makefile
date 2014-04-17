CHILD=ana
CHI=$(shell echo $(CHILD) | cut -c 1-3)
SAGE=12
EAGE=23
NITER=10
QUEUE=cpu
PY_CFG=./py-cfg/py-cfg
list_of_grammars=$(shell echo $(CHILD)_$(SAGE)to$(EAGE)m_*.lt)
NTOPICS=7
# NTOPICS is just for topic-learning grammars
NLEVELS=4
# NLEVELS is just for topic-learning grammars


just_basic_and_single:
	# make prepare_topics_* has still to be done by hand (once for all)
	@echo ">>> creating the $(CHILD)_$(SAGE)to$(EAGE)m folder with needed data"
	$(MAKE) $(CHILD)_$(SAGE)to$(EAGE)m
	@echo ">>> launching basic grammars"
	$(MAKE) basic_AGs
	@echo ">>> launching single context ("_sc") grammars"
	$(MAKE) single_context_AGs


just_basic_and_single_fr:
	# make prepare_topics_* has still to be done by hand (once for all)
	@echo ">>> creating the $(CHILD)_fr_$(SAGE)to$(EAGE)m folder with needed data"
	$(MAKE) $(CHILD)_fr_$(SAGE)to$(EAGE)m
	@echo ">>> launching basic grammars"
	$(MAKE) basic_AGs_fr
	#@echo ">>> launching single context ("_sc") grammars"
	#$(MAKE) single_context_AGs_fr


all_Providence: 
	$(MAKE) just_basic_and_single
	@echo ">>> generating all grammars as once"
	$(MAKE) generate_grammars
	@echo ">>> now launching adaptor grammars jobs using all those grammars:"
	$(MAKE) launch_jobs


prepare_topics_Providence:
	./topics_do_all_Providence.sh $(CHILD)


prepare_topics_Lyon:
	./topics_do_all_Lyon.sh $(CHILD)


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
	./prepare_child_months.sh $(CHILD) $(SAGE) $(EAGE) ProvidenceFinal


$(CHILD)_fr_$(SAGE)to$(EAGE)m:
	./prepare_child_months.sh $(CHILD) $(SAGE) $(EAGE) LyonFinal


basic_AGs: $(CHILD)_$(SAGE)to$(EAGE)m
	cut -d " " -f 2- $(CHILD)_$(SAGE)to$(EAGE)m/$(CHILD)_docs_$(SAGE)to$(EAGE)m.ylt > $(CHILD)_$(SAGE)to$(EAGE)m.ylt
	# for qsub with Open-MPI, use -pe openmpi_ib 8-16
	qsub -N "$(CHI)-$(SAGE)-$(EAGE)-unigram" -q $(QUEUE) -cwd -o `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m -e `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m launch_adaptor_mean.sh $(PY_CFG) unigram $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(NITER)
	qsub -N "$(CHI)-$(SAGE)-$(EAGE)-colloc" -q $(QUEUE) -cwd -o `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m -e `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m launch_adaptor_mean.sh $(PY_CFG) colloc $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(NITER)
	qsub -N "$(CHI)-$(SAGE)-$(EAGE)-syll" -q $(QUEUE) -cwd -o `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m -e `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m launch_adaptor_mean.sh $(PY_CFG) syll $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(NITER)
	qsub -N "$(CHI)-$(SAGE)-$(EAGE)-colloc-syll" -q $(QUEUE) -cwd -o `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m -e `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m launch_adaptor_mean.sh $(PY_CFG) colloc_syll $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(NITER)
	qsub -N "$(CHI)-$(SAGE)-$(EAGE)-colloc3-syll" -q $(QUEUE) -cwd -o `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m -e `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m launch_adaptor_mean.sh $(PY_CFG) colloc3_syll $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(NITER)


basic_AGs_fr: $(CHILD)_fr_$(SAGE)to$(EAGE)m
	cut -d " " -f 2- $(CHILD)_$(SAGE)to$(EAGE)m/$(CHILD)_docs_$(SAGE)to$(EAGE)m.ylt > $(CHILD)_$(SAGE)to$(EAGE)m.ylt
	# for qsub with Open-MPI, use -pe openmpi_ib 8-16
	qsub -N "$(CHI)-$(SAGE)-$(EAGE)-unigram" -q $(QUEUE) -cwd -o `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m -e `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m launch_adaptor.sh $(PY_CFG) unigram_fr $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(NITER)
	qsub -N "$(CHI)-$(SAGE)-$(EAGE)-colloc" -q $(QUEUE) -cwd -o `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m -e `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m launch_adaptor.sh $(PY_CFG) colloc_fr $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(NITER)
	qsub -N "$(CHI)-$(SAGE)-$(EAGE)-syll" -q $(QUEUE) -cwd -o `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m -e `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m launch_adaptor.sh $(PY_CFG) syll_fr $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(NITER)
	qsub -N "$(CHI)-$(SAGE)-$(EAGE)-colloc-syll" -q $(QUEUE) -cwd -o `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m -e `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m launch_adaptor.sh $(PY_CFG) colloc_syll_fr $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(NITER)


%.prs: %.lt $(CHILD)_$(SAGE)to$(EAGE)m
	qsub -N "$(CHI)-$(SAGE)-$(EAGE)-docs-$(subst .lt,,$<)" -q $(QUEUE) -cwd -o `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m -e `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m launch_adaptor.sh $(PY_CFG) $(subst .lt,,$<) $(CHILD)_docs_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(NITER)
	#qsub -N "$(CHILD)-docs-$(subst .lt,,$<)" -q $(QUEUE) -cwd launch_adaptor.sh $(PY_CFG) $(subst .lt,,$<) $(CHILD)_splits_docs_$(SAGE)to$(EAGE)m $(CHILD)_splits_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(NITER)


launch_jobs: $(subst .lt,.prs,$(list_of_grammars))
	@echo "$(list_of_grammars)"
	# this rule is just need to expand the list_of_grammars var after generation


unigram_grammars: $(CHILD)_$(SAGE)to$(EAGE)m
	#qsub -N "$(CHI)-$(SAGE)-$(EAGE)-syll-sc+" -q $(QUEUE) -cwd -o `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m -e `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m launch_adaptor_mean.sh $(PY_CFG) syll_common_sc $(CHILD)_topic_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(NITER)
	qsub -N "$(CHI)-$(SAGE)-$(EAGE)-unigram" -q $(QUEUE) -cwd -o `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m -e `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m launch_adaptor_mean.sh $(PY_CFG) unigram $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(NITER)
	qsub -N "$(CHI)-$(SAGE)-$(EAGE)-unigram-sc" -q $(QUEUE) -cwd -o `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m -e `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m launch_adaptor_mean.sh $(PY_CFG) unigram_sc $(CHILD)_topic_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(NITER)
	qsub -N "$(CHI)-$(SAGE)-$(EAGE)-unigram-sc-r" -q $(QUEUE) -cwd -o `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m -e `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m launch_adaptor_mean.sh $(PY_CFG) readapt_unigram_sc $(CHILD)_topic_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(NITER)
	qsub -N "$(CHI)-$(SAGE)-$(EAGE)-unigram-sc+" -q $(QUEUE) -cwd -o `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m -e `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m launch_adaptor_mean.sh $(PY_CFG) unigram_common_sc $(CHILD)_topic_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(NITER)
    # TODO grammars with different Word --> Phon Phons values


single_context_AGs: $(CHILD)_$(SAGE)to$(EAGE)m
	qsub -N "$(CHI)-$(SAGE)-$(EAGE)-unigram-sc" -q $(QUEUE) -cwd -o `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m -e `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m launch_adaptor_mean.sh $(PY_CFG) unigram_sc $(CHILD)_topic_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(NITER)
	qsub -N "$(CHI)-$(SAGE)-$(EAGE)-colloc-sc" -q $(QUEUE) -cwd -o `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m -e `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m launch_adaptor_mean.sh $(PY_CFG) colloc_sc $(CHILD)_topic_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(NITER)
	qsub -N "$(CHI)-$(SAGE)-$(EAGE)-syll-sc" -q $(QUEUE) -cwd -o `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m -e `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m launch_adaptor_mean.sh $(PY_CFG) syll_sc $(CHILD)_topic_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(NITER)
	qsub -N "$(CHI)-$(SAGE)-$(EAGE)-colloc-syll-sc" -q $(QUEUE) -cwd -o `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m -e `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m launch_adaptor_mean.sh $(PY_CFG) colloc_syll_sc $(CHILD)_topic_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(NITER)
	qsub -N "$(CHI)-$(SAGE)-$(EAGE)-unigram-sc-r" -q $(QUEUE) -cwd -o `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m -e `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m launch_adaptor_mean.sh $(PY_CFG) readapt_unigram_sc $(CHILD)_topic_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(NITER)
	qsub -N "$(CHI)-$(SAGE)-$(EAGE)-colloc-sc-r" -q $(QUEUE) -cwd -o `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m -e `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m launch_adaptor_mean.sh $(PY_CFG) readapt_colloc_sc $(CHILD)_topic_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(NITER)
	qsub -N "$(CHI)-$(SAGE)-$(EAGE)-syll-sc-r" -q $(QUEUE) -cwd -o `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m -e `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m launch_adaptor_mean.sh $(PY_CFG) readapt_syll_sc $(CHILD)_topic_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(NITER)
	qsub -N "$(CHI)-$(SAGE)-$(EAGE)-colloc-syll-sc-r" -q $(QUEUE) -cwd -o `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m -e `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m launch_adaptor_mean.sh $(PY_CFG) readapt_colloc_syll_sc $(CHILD)_topic_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(NITER)
	$(MAKE) single_context_with_neutral_words


single_context_AGs_fr: $(CHILD)_fr_$(SAGE)to$(EAGE)m
	# TODO 
	qsub -N "$(CHI)-$(SAGE)-$(EAGE)-unigram-sc" -q $(QUEUE) -cwd -o `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m -e `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m launch_adaptor_mean.sh $(PY_CFG) unigram_sc_fr $(CHILD)_topic_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(NITER)
	qsub -N "$(CHI)-$(SAGE)-$(EAGE)-colloc-sc" -q $(QUEUE) -cwd -o `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m -e `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m launch_adaptor_mean.sh $(PY_CFG) colloc_sc_fr $(CHILD)_topic_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(NITER)
	qsub -N "$(CHI)-$(SAGE)-$(EAGE)-syll-sc" -q $(QUEUE) -cwd -o `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m -e `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m launch_adaptor_mean.sh $(PY_CFG) syll_sc_fr $(CHILD)_topic_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(NITER)
	qsub -N "$(CHI)-$(SAGE)-$(EAGE)-colloc-syll-sc" -q $(QUEUE) -cwd -o `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m -e `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m launch_adaptor_mean.sh $(PY_CFG) colloc_syll_sc_fr $(CHILD)_topic_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(NITER)
	qsub -N "$(CHI)-$(SAGE)-$(EAGE)-colloc-syll-sc-r" -q $(QUEUE) -cwd -o `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m -e `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m launch_adaptor_mean.sh $(PY_CFG) readapt_colloc_syll_sc_fr $(CHILD)_topic_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(NITER)
	#$(MAKE) single_context_with_neutral_words TODO


single_context_with_neutral_words: $(CHILD)_$(SAGE)to$(EAGE)m
	qsub -N "$(CHI)-$(SAGE)-$(EAGE)-colloc-sc+" -q $(QUEUE) -cwd -o `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m -e `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m launch_adaptor_mean.sh $(PY_CFG) colloc_common_sc $(CHILD)_topic_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(NITER)
	qsub -N "$(CHI)-$(SAGE)-$(EAGE)-colloc-syll-sc+" -q $(QUEUE) -cwd -o `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m -e `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m launch_adaptor_mean.sh $(PY_CFG) colloc_common_syll_sc $(CHILD)_topic_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(NITER)
	qsub -N "$(CHI)-$(SAGE)-$(EAGE)-colloc-sc-r+" -q $(QUEUE) -cwd -o `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m -e `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m launch_adaptor_mean.sh $(PY_CFG) readapt_colloc_common_sc $(CHILD)_topic_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(NITER)
	qsub -N "$(CHI)-$(SAGE)-$(EAGE)-colloc-syll-sc-r+" -q $(QUEUE) -cwd -o `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m -e `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m launch_adaptor_mean.sh $(PY_CFG) readapt_colloc_common_syll_sc $(CHILD)_topic_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(NITER)
	qsub -N "$(CHI)-$(SAGE)-$(EAGE)-colloc-syll-sc-r+2" -q $(QUEUE) -cwd -o `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m -e `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m launch_adaptor_mean.sh $(PY_CFG) readapt_colloc_common2_syll_sc $(CHILD)_topic_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(NITER)
	qsub -N "$(CHI)-$(SAGE)-$(EAGE)-colloc-syll-sc-w+" -q $(QUEUE) -cwd -o `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m -e `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m launch_adaptor_mean.sh $(PY_CFG) colloc_syll_sc_common_words $(CHILD)_topic_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(NITER)
	qsub -N "$(CHI)-$(SAGE)-$(EAGE)-colloc-syll-sc-c+" -q $(QUEUE) -cwd -o `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m -e `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m launch_adaptor_mean.sh $(PY_CFG) colloc_syll_sc_common_collocs $(CHILD)_topic_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(NITER)


$(CHILD)_$(SAGE)to$(EAGE)m/$(CHILD)_topic_$(SAGE)to$(EAGE)m_train.ylt:
	python src/split_train_test.py $(CHILD)_$(SAGE)to$(EAGE)m/$(CHILD)_topic_$(SAGE)to$(EAGE)m.ylt $(CHILD)_$(SAGE)to$(EAGE)m/$(CHILD)_$(SAGE)to$(EAGE)m.gold 0.2


$(CHILD)_$(SAGE)to$(EAGE)m/$(CHILD)_$(SAGE)to$(EAGE)m_train.ylt: $(CHILD)_$(SAGE)to$(EAGE)m/$(CHILD)_topic_$(SAGE)to$(EAGE)m_train.ylt
	cut -d " " -f 2- $(CHILD)_$(SAGE)to$(EAGE)m/$(CHILD)_topic_$(SAGE)to$(EAGE)m_test.ylt > $(CHILD)_$(SAGE)to$(EAGE)m/$(CHILD)_$(SAGE)to$(EAGE)m_train.ylt
	cut -d " " -f 2- $(CHILD)_$(SAGE)to$(EAGE)m/$(CHILD)_topic_$(SAGE)to$(EAGE)m_test.ylt > $(CHILD)_$(SAGE)to$(EAGE)m/$(CHILD)_$(SAGE)to$(EAGE)m_test.ylt


test: $(CHILD)_$(SAGE)to$(EAGE)m/$(CHILD)_topic_$(SAGE)to$(EAGE)m_train.ylt $(CHILD)_$(SAGE)to$(EAGE)m/$(CHILD)_$(SAGE)to$(EAGE)m_train.ylt
	# Train on not prefixed and test on not prefixed
	qsub -N "$(CHI)-$(SAGE)-$(EAGE)-test-colloc-syll" -q $(QUEUE) -cwd -o `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m -e `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m launch_adaptor_test.sh $(PY_CFG) colloc_syll $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(NITER)
	# Train on prefixed and test on prefixed
	qsub -N "$(CHI)-$(SAGE)-$(EAGE)-test-colloc-syll-sc+" -q $(QUEUE) -cwd -o `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m -e `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m launch_adaptor_test.sh $(PY_CFG) colloc_common_syll_sc $(CHILD)_topic_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(NITER)
	qsub -N "$(CHI)-$(SAGE)-$(EAGE)-test-colloc-syll-sc-r+" -q $(QUEUE) -cwd -o `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m -e `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m launch_adaptor_test.sh $(PY_CFG) readapt_colloc_common_syll_sc $(CHILD)_topic_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(NITER)
	qsub -N "$(CHI)-$(SAGE)-$(EAGE)-test-colloc-syll-sc" -q $(QUEUE) -cwd -o `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m -e `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m launch_adaptor_test.sh $(PY_CFG) colloc_syll_sc $(CHILD)_topic_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(NITER)


randomize_t: $(CHILD)_$(SAGE)to$(EAGE)m
	python src/randomize_topics.py $(CHILD)_$(SAGE)to$(EAGE)m/$(CHILD)_topic_$(SAGE)to$(EAGE)m.ylt > $(CHILD)_$(SAGE)to$(EAGE)m/$(CHILD)_random_topic_$(SAGE)to$(EAGE)m.ylt
	qsub -N "$(CHI)-$(SAGE)-$(EAGE)-random-colloc-syll-sc+" -q $(QUEUE) -cwd -o `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m -e `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m launch_adaptor_mean.sh $(PY_CFG) colloc_common_syll_sc $(CHILD)_random_topic_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(NITER)
	qsub -N "$(CHI)-$(SAGE)-$(EAGE)-random-colloc-syll-sc-r+" -q $(QUEUE) -cwd -o `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m -e `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m launch_adaptor_mean.sh $(PY_CFG) readapt_colloc_common_syll_sc $(CHILD)_random_topic_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(NITER)
	qsub -N "$(CHI)-$(SAGE)-$(EAGE)-random-colloc-syll-sc" -q $(QUEUE) -cwd -o `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m -e `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m launch_adaptor_mean.sh $(PY_CFG) colloc_syll_sc $(CHILD)_random_topic_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(NITER)


permute_t: $(CHILD)_$(SAGE)to$(EAGE)m
	python src/permute_topics.py $(CHILD)_$(SAGE)to$(EAGE)m/$(CHILD)_topic_$(SAGE)to$(EAGE)m.ylt > $(CHILD)_$(SAGE)to$(EAGE)m/$(CHILD)_permuted_topic_$(SAGE)to$(EAGE)m.ylt
	qsub -N "$(CHI)-$(SAGE)-$(EAGE)-permuted-colloc-syll-sc+" -q $(QUEUE) -cwd -o `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m -e `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m launch_adaptor_mean.sh $(PY_CFG) colloc_common_syll_sc $(CHILD)_permuted_topic_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(NITER)
	qsub -N "$(CHI)-$(SAGE)-$(EAGE)-permuted-colloc-syll-sc-r+" -q $(QUEUE) -cwd -o `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m -e `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m launch_adaptor_mean.sh $(PY_CFG) readapt_colloc_common_syll_sc $(CHILD)_permuted_topic_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(NITER)
	qsub -N "$(CHI)-$(SAGE)-$(EAGE)-permuted-colloc-syll-sc" -q $(QUEUE) -cwd -o `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m -e `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m launch_adaptor_mean.sh $(PY_CFG) colloc_syll_sc $(CHILD)_permuted_topic_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(NITER)


test_wo_prefix_topic: test 
	# Trains on prefixed, test on not prefixed
	qsub -N "$(CHI)-$(SAGE)-$(EAGE)-nopfx-colloc-syll-sc+" -q $(QUEUE) -cwd -o `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m -e `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m launch_adaptor_nopfx.sh $(PY_CFG) colloc_common_syll_sc_nopfx $(CHILD)_topic_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(NITER)
	qsub -N "$(CHI)-$(SAGE)-$(EAGE)-nopfx-colloc-syll-sc-r+" -q $(QUEUE) -cwd -o `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m -e `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m launch_adaptor_nopfx.sh $(PY_CFG) readapt_colloc_common_syll_sc_nopfx $(CHILD)_topic_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(NITER)
	qsub -N "$(CHI)-$(SAGE)-$(EAGE)-nopfx-colloc-syll-sc" -q $(QUEUE) -cwd -o `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m -e `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m launch_adaptor_nopfx.sh $(PY_CFG) colloc_syll_sc_nopfx $(CHILD)_topic_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(NITER)


topics_learn_topics: $(CHILD)_$(SAGE)to$(EAGE)m
	python src/topics_learning_grammars.py $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m/$(CHILD)_docs_$(SAGE)to$(EAGE)m.ylt $(NTOPICS) $(NLEVELS)
	qsub -N "$(CHI)-$(SAGE)-$(EAGE)-colloc-syll-learn-topics" -q $(QUEUE) -cwd -o `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m -e `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m launch_adaptor_mean_samefolder.sh $(PY_CFG) $(CHILD)_$(SAGE)to$(EAGE)m/colloc_syll_learn_topics $(CHILD)_docs_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(NITER)
	qsub -N "$(CHI)-$(SAGE)-$(EAGE)-colloc-common-syll-learn-topics" -q $(QUEUE) -cwd -o `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m -e `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m launch_adaptor_mean_samefolder.sh $(PY_CFG) $(CHILD)_$(SAGE)to$(EAGE)m/colloc_common_syll_learn_topics $(CHILD)_docs_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(NITER)
	qsub -N "$(CHI)-$(SAGE)-$(EAGE)-$(NLEVELS)-levels-learn-topics" -q $(QUEUE) -cwd -o `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m -e `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m launch_adaptor_generic_samefolder.sh $(PY_CFG) $(CHILD)_$(SAGE)to$(EAGE)m/levels_$(NLEVELS)_learn_topics $(CHILD)_docs_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(NITER)


multiple_levels: $(CHILD)_$(SAGE)to$(EAGE)m
	qsub -N "$(CHI)-$(SAGE)-$(EAGE)-three-levels" -q $(QUEUE) -cwd -o `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m -e `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m launch_adaptor_mean.sh $(PY_CFG) three_levels $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(NITER)
	qsub -N "$(CHI)-$(SAGE)-$(EAGE)-three-levels-one-lower" -q $(QUEUE) -cwd -o `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m -e `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m launch_adaptor_mean.sh $(PY_CFG) three_levels_one_lower $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(NITER)
	qsub -N "$(CHI)-$(SAGE)-$(EAGE)-three-levels-sc" -q $(QUEUE) -cwd -o `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m -e `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m launch_adaptor_mean.sh $(PY_CFG) three_levels_sc $(CHILD)_topic_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(NITER)
	qsub -N "$(CHI)-$(SAGE)-$(EAGE)-three-levels-one-lower-sc" -q $(QUEUE) -cwd -o `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m -e `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m launch_adaptor_mean.sh $(PY_CFG) three_levels_one_lower_sc $(CHILD)_topic_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(NITER)


generic_levels: $(CHILD)_$(SAGE)to$(EAGE)m
	qsub -N "$(CHI)-$(SAGE)-$(EAGE)-four-levels" -q $(QUEUE) -cwd -o `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m -e `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m launch_adaptor_generic.sh $(PY_CFG) four_levels $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(NITER)
	qsub -N "$(CHI)-$(SAGE)-$(EAGE)-four-levels-sc" -q $(QUEUE) -cwd -o `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m -e `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m launch_adaptor_generic.sh $(PY_CFG) four_levels_sc $(CHILD)_topic_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(NITER)


mbr_single_context_bests: $(CHILD)_$(SAGE)to$(EAGE)m
	qsub -N "$(CHI)-$(SAGE)-$(EAGE)-mbr-colloc-syll" -q $(QUEUE) -cwd -o `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m -e `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m launch_adaptor_mean.sh $(PY_CFG) colloc_syll $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(NITER)
	qsub -N "$(CHI)-$(SAGE)-$(EAGE)-mbr-colloc-syll-sc" -q $(QUEUE) -cwd -o `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m -e `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m launch_adaptor_mean.sh $(PY_CFG) colloc_syll_sc $(CHILD)_topic_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(NITER)
	qsub -N "$(CHI)-$(SAGE)-$(EAGE)-mbr-colloc-syll-sc+" -q $(QUEUE) -cwd -o `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m -e `pwd`/$(CHILD)_$(SAGE)to$(EAGE)m launch_adaptor_mean.sh $(PY_CFG) colloc_common_syll_sc $(CHILD)_topic_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(CHILD)_$(SAGE)to$(EAGE)m $(NITER)
	

clean:
	rm -rf $(CHILD)_$(SAGE)to$(EAGE)m
	rm $(CHILD)_$(SAGE)to$(EAGE)m_*.lt
