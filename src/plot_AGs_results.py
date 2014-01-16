import numpy as np
import pylab as pl
import matplotlib.pyplot as plt
from collections import defaultdict
import glob

SAGE_XPS = 11
SAGE = 12
EAGE = 22
N_MONTHS = EAGE-SAGE+1
TYPES = ["basic", "single-context", "topics"]
#TYPES = ["basic", "topics"]
ITERS = [500]
#ITERS = [100, 500]
PREFIX = ""
#PREFIX = "old_naima_XPs/"
TAKE_MAX_SCORE = True # in case of several results

results = defaultdict(lambda: np.zeros(N_MONTHS))

for month in xrange(SAGE, EAGE+1):
    for fname in glob.iglob(PREFIX+'naima_' + str(SAGE_XPS) + 'to' + str(month) 
            + 'm/nai*-' + str(SAGE_XPS) + '-' + str(month) + '*.o*'):
        if "-sc" in fname and not "single-context" in TYPES:
            continue
        if "docs" in fname and not "topics" in TYPES:
            continue
        # always plots basic results currently
        doit = False
        with open (fname.replace(".o", ".e")) as f:
            line = ""
            for line in f:
                pass
            for iternumber in ITERS:
                if str(iternumber) + " iterations" in line:
                    doit = True
                    break
        if not doit:
            continue
        print fname
        fscore = None # token f-score
        with open(fname) as f:
            line = ""
            for line in f:
                pass
            try:
                fscore = float(line.split('\t')[0])
            except:
                pass
        fname = '/'.join(fname.split('/')[1:])
        if 'docs' in fname:
            condname = '_'.join(fname.split('/')[1].split('-')[-1].split('.')[0].split('_')[2:])
            if condname == '': # topics-based unigram
                condname = 'uni'
            condname = 'd_' + condname
        elif '-sc' in fname:
            fname = fname.replace('-sc', '')
            condname = 't'
            if '-r' in fname:
                condname = 't_readapt'
                fname = fname.replace('-r', '')
            condname = '_'.join([condname] + fname.split('/')[1].split('-')[3:]).split('.')[0]
        else:
            condname = '_'.join(fname.split('/')[1].split('-')[3:]).split('.')[0]

        if TAKE_MAX_SCORE:
            if results[condname][month-SAGE] != 0:
                results[condname][month-SAGE] = max(fscore, results[condname][month-SAGE])
            else:
                results[condname][month-SAGE] = fscore
        else:
            results[condname][month-SAGE] = fscore

print results
        

fig = plt.figure(figsize=(12, 9), dpi=300)
plt.xticks(xrange(N_MONTHS))

ax = plt.gca()
ax.set_ylim([0.5, 0.95])
ax.set_xlim([-0.1, N_MONTHS - 0.9])
ax.set_xticklabels(map(str, range(SAGE, EAGE+1)))
for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] +
        ax.get_xticklabels() + ax.get_yticklabels()):
    item.set_fontsize(16)
for cond, a in results.iteritems():
    linetype = ''
    if "syll" in cond:
        linetype = '^:'
    else:
        linetype = 'v:'
    if "d_" in cond:
        linetype = linetype[0] + '--'
    plt.plot(a, linetype, linewidth=3.5)#, alpha=0.8)
    
plt.xlabel('months')
plt.ylabel('token f-score')
plt.legend([l for l in results.iterkeys()], loc='best', ncol=4)
plt.setp(ax.get_legend().get_texts(), fontsize=12)
plt.savefig('progress.png')
