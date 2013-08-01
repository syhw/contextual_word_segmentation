################################################################################
#                                                                              #
#              Makefile for TopicModels/word-segmentation                      #
#                                                                              #
#                  (c) Mark Johnson, 9th August, 2011                          #
#                                                                              #
################################################################################

################################################################################
#                                                                              #
#                            parameters                                        #
#                                                                              #
################################################################################

# PROGRAM is the name of the program that will be run
PROGRAM=./py-cfg

# OUTPUTDIR is the directory in which all files are produced
#
OUTPUTDIR=firstwordsr

# OUTPUTPREFIX is the prefix on all files in OUTPUTDIR associated with this run
OUTPUTPREFIX=a1

# CORPUS is the corpus we're going to learn from
CORPUS=fm_corpus_tier.adp
# CORPUS=permuted_fm_corpus_tier.adp
# CORPUS=permuted2_fm_corpus_tier.adp

# GRAMMARS is a list of grammars we're going to try (without the .lt suffix)
#
GRAMMARS=unigram Tunigram TunigramX1 colloc Tcolloc Tcolloc1 TcollocX1

# Fraction of corpus to train on
#
PYSS=0.0000 0.0002 0.0005 0.0010 0.0020 0.0050 0.0100 0.0200 0.0500 0.1000 0.2000 0.5000 1.0000

# BURNINSKIP is the fraction of the sample to be discarded before collecting 
#  samples for evaluation
#
BURNINSKIP=0.5

# PYFLAGS specify flags to be given to py-cfg
#
PYFLAGS=-P -d 10

# OUTS is a list of types of output files we're going to produce
#
# OUTS=avprs
OUTS=score

# Each fold is a different run; to do 4 runs set FOLDS=0 1 2 3
#
FOLDS=00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15

PYAS=1e-4
PYES=2
PYFS=1

PYBS=1e4
# PYGS=0
# PYHS=0
PYGS=100
PYHS=0.01

PYWS=1

PYTS=1
PYMS=0

# PYNS is the number of iterations
#
PYNS=2000

# PYRS=0
PYRS=-1

PYD=D_
PYE=E_
PYS=S_

# GOLD is the evaluation data
#
GOLD=fm_corpus_tier_gold.seg

# TOPICALWORDSFILE is a file containing all the topical words
#
TOPICALWORDSFILE=evalseg/fm_phone_content_words.txt

# rate at which model's output is evaluated
#
TRACEEVERY=10

EXEC=time
# EXEC=valgrind

IGNORETERMINALRE=\"^T_\\S+$$\"

# EVALREGEX is the regular expression given to eval.py in the evaluation script (may depend on grammar)
# EVALREGEX=Colloc\\b
#
# SCORECATRE=\"^Word(?:_(?P<topic>\\S+))?$$\"
SCORECATRE=\"^Word[0-9]*(?:_(?P<topic>\\S+))?$$\"

################################################################################
#                                                                              #
#                     everything below this should be generic                  #
#                                                                              #
################################################################################


# The list of files we will make

OUTPUTS=$(foreach GRAMMAR,$(GRAMMARS), \
	$(foreach s,$(PYSS), \
	$(foreach e,$(PYES), \
	$(foreach f,$(PYFS), \
	$(foreach g,$(PYGS), \
	$(foreach h,$(PYHS), \
	$(foreach a,$(PYAS), \
	$(foreach b,$(PYBS), \
	$(foreach w,$(PYWS), \
	$(foreach t,$(PYTS), \
	$(foreach m,$(PYMS), \
	$(foreach n,$(PYNS), \
	$(foreach R,$(PYRS), \
	$(foreach out,$(OUTS), \
	$(OUTPUTDIR)/$(OUTPUTPREFIX)_G$(GRAMMAR)_$(PYD)$(PYE)n$(n)_s$(s)_m$(m)_t$(t)_w$(w)_a$(a)_b$(b)_e$(e)_f$(f)_g$(g)_h$(h)_R$(R).$(out)))))))))))))))

TARGETS=$(PROGRAM) $(OUTPUTS)

.PHONY: top
top: $(TARGETS)

py-cfg:
	ln -s ~/research/py-cfg/py-cfg py-cfg

# PRSFILES=$(patsubst $(OUTPUTDIR)/$(OUTPUTPREFIX)_%.$(out),$(OUTPUTDIR)/$(OUTPUTPREFIX)_%.prs,$(OUTPUTS))
# .SECONDARY: $(PRSFILES)
# .PRECIOUS: $(PRSFILES)

.SECONDARY:
.DELETE_ON_ERROR:

getarg=$(patsubst $(1)%,%,$(filter $(1)%,$(filter-out $(OUTPUTDIR)/$(OUTPUTPREFIX),$(subst _, ,$(2)))))

keyword=$(patsubst $(1),-$(1),$(filter $(1),$(filter-out $(OUTPUTDIR)/$(OUTPUTPREFIX),$(subst _, ,$(2)))))

GRAMMARFILES=$(foreach g,$(GRAMMARS),$(OUTPUTDIR)/$(g).lt)

# $(OUTPUTDIR)/$(OUTPUTPREFIX)_%.score: score_seg.prl $(CORPUS) $(OUTPUTDIR)/$(OUTPUTPREFIX)_%.avprs
#	$^ > $@	

$(OUTPUTDIR)/$(OUTPUTPREFIX)_%.score: $(OUTPUTDIR)/$(OUTPUTPREFIX)_%.avprs eval.py $(GOLD) $(TOPICALWORDSFILE)
	eval-topics.py --gold $(GOLD) --train $< --topicalwordsfile $(TOPICALWORDSFILE) > $@	

# $(OUTPUTDIR)/$(OUTPUTPREFIX)_%.score: $(OUTPUTDIR)/$(OUTPUTPREFIX)_%.avprs evalseg/evalseg.exe evalseg/fm_corpus_tier_gold.seg evalseg/fm_phone_content_words.txt 
#	evalseg/evalseg.exe $< evalseg/fm_corpus_tier_gold.seg evalseg/fm_phone_content_words.txt > $@

$(OUTPUTDIR)/$(OUTPUTPREFIX)_%.avprs: mbr.py $(foreach fold,$(FOLDS),$(OUTPUTDIR)/$(OUTPUTPREFIX)_%_$(fold).sws)
	$^ > $@

$(OUTPUTDIR)/$(OUTPUTPREFIX)_%.sws  $(OUTPUTDIR)/$(OUTPUTPREFIX)_%.wlt: $(PROGRAM) $(GRAMMARFILES) $(CORPUS) trees-words.py eval-topics.py
	mkdir -p $(OUTPUTDIR)
	echo "Starting $@"
	date
	$(EXEC) $(PROGRAM) $(PYFLAGS) \
		-A $(basename $@).prs \
		-x $(TRACEEVERY) \
		-F $(basename $@).trace \
		-G $(basename $@).wlt \
		-C \
		$(call keyword,D,$@) \
		$(call keyword,E,$@) \
		$(call keyword,S,$@) \
		-r $$RANDOM$$RANDOM \
		-a $(call getarg,a,$@) \
		-b $(call getarg,b,$@) \
		-e $(call getarg,e,$@) \
		-f $(call getarg,f,$@) \
		-g $(call getarg,g,$@) \
		-h $(call getarg,h,$@) \
		-w $(call getarg,w,$@) \
		-T $(call getarg,t,$@) \
		-m $(call getarg,m,$@) \
		-n $(call getarg,n,$@) \
		-R $(call getarg,R,$@) \
		-s $(call getarg,s,$@) \
		-X "eval-topics.py --gold $(GOLD) --train-trees --score-cat-re=$(SCORECATRE) --ignore-terminal-re=$(IGNORETERMINALRE) --topicalwordsfile=$(TOPICALWORDSFILE) > $(basename $@).weval" \
		-X "trees-words.py --ignore-terminal-re=$(IGNORETERMINALRE) --score-cat-re=$(SCORECATRE) --nepochs $(call getarg,n,$@) --rate $(TRACEEVERY) --skip $(BURNINSKIP) > $(basename $@).sws" \
		$(OUTPUTDIR)/$(call getarg,G,$@).lt \
		< $(CORPUS)

grammarfiles: $(GRAMMARFILES)

permuted_fm_corpus_tier.adp: permute-topics.py fm_corpus_tier.adp
	./permute-topics.py fm_corpus_tier.adp > permuted_fm_corpus_tier.adp

permuted2_fm_corpus_tier.adp: permute-topics.py fm_corpus_tier.adp
	./permute-topics.py --seed 2179 fm_corpus_tier.adp > permuted2_fm_corpus_tier.adp

fm_corpus_tier.adp: childes-data.py fm_corpus_tier.txt phon-topic.txt
	childes-data.py -c fm_corpus_tier.txt -p phon-topic.txt -g $(GOLD) -t fm_corpus_tier.adp

$(OUTPUTDIR)/%.lt: write-grammar.py $(CORPUS)
	mkdir -p $(OUTPUTDIR)
	write-grammar.py --grammar $* $(CORPUS) > $@

.PHONY: clean
clean: data-clean
	rm -fr *.o *.d *~ core *.out *.lt

.PHONY: real-clean
real-clean: clean 
	rm -fr $(TARGETS)

