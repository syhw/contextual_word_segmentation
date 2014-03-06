Requirements:
  - Adaptor Grammar software (py-cfg) compiled in PY_CFG (Makefile)
    (http://web.science.mq.edu.au/~mjohnson/Software.htm)
  - Python
    - gensim
    - (optional) pattern
 
To launch it on default settings (see in the Makefile, Providence corpus, 
children Naima, start age 11 months, end age 22 months), you need to put a .txt
file in ProvidenceFinal/ToSegment/my_corpus.txt with document boundaries @ 
(known) or @? (possible boundary but unknown). Then run:
  - make prepare_topics
  - make all

You can play with the CHILD / EAGE / SAGE variables in the Makefile. E.g. :

make just_basic_and_single CHILD=naima SAGE=11 EAGE=22 NITER=500
make test_wo_prefix_topic CHILD=naima SAGE=11 EAGE=22 NITER=500
for eage in `range 12 22`; do make just_basic_and_single CHILD=naima SAGE=11 EAGE=$eage NITER=500; done

To get all the data points and plot them, use e.g.:

for eage in `range 12 22`; do make just_basic_and_single CHILD=naima SAGE=11 EAGE=$eage NITER=500; done
python src/plot_AGs_results.py
