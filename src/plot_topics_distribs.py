import sys
import pylab as pl

LDAMODEL = 'provi_reseg_lemmatized_tfidf.ldamodel'
usage = """python src/plot_topics_distrib.py < all_1min_doc_topics_reseg_lemmatized.txt"""

topics_distrib = {}

for line in sys.stdin:
    tuples = line.split('[')[1].split(')')
    tuples = tuples[:-1]
    for t in tuples:
        tmp = t.strip(' (,').split(',')
        tid = int(tmp[0])
        topics_distrib[tid] = topics_distrib.get(tid, 0.0) + float(tmp[1].strip(' ')) 

import gensim
import cPickle

with open(LDAMODEL) as f:
#with open(sys.argv[1]) as f:
    lda = cPickle.load(f)
y = ['\n\n'.join(filter(lambda x: 'NN' in x, lda.print_topic(i).split('+')[:20])) for i in topics_distrib.iterkeys()]

#for topic, value in topics_distrib.iteritems():
pl.rcParams['lines.linewidth'] = 2
pl.rcParams['font.family'] = 'sans-serif'
pl.rcParams['font.size'] = 16
pl.pie([x for x in topics_distrib.itervalues()], labels=y, shadow=True, explode=[0.05 for i in xrange(len(topics_distrib))])
pl.show()

    

