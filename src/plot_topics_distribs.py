import sys
import pylab as pl

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

with open('provi_reseg_lemmatized_tfidf.ldamodel') as f:
    lda = cPickle.load(f)
y = ['\n\n'.join(lda.print_topic(i).split('+')[:4]) for i in topics_distrib.iterkeys()]

#for topic, value in topics_distrib.iteritems():
pl.rcParams['lines.linewidth'] = 2
pl.rcParams['font.family'] = 'sans-serif'
pl.rcParams['font.size'] = 16
pl.pie([x for x in topics_distrib.itervalues()], labels=y, shadow=True, explode=[0.05 for i in xrange(len(topics_distrib))])
pl.show()

    

