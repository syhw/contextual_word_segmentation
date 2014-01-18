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

You can play with the CHILD / EAGE / SAGE variables in the Makefile.

