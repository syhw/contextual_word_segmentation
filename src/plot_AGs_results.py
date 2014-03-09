import numpy as np
import pylab as pl
import matplotlib
import matplotlib.pyplot as plt
from collections import defaultdict
import glob
import readline # otherwise the wrong readline is imported by rpy2

SAGE_XPS = 11
SAGE = 12
EAGE = 23
N_MONTHS = EAGE-SAGE+1
#TYPES = ["basic", "single-context", "topics"]
#TYPES = ["basic", "topics"]
TYPES = ["basic", "single-context"]
TEST = False # if True, just use the values evaluated on a test test
ITERS = range(500, 520)
#ITERS = range(1000,1005)
PREFIX = ""
#PREFIX = "old_naima_XPs/"
TAKE_MAX_SCORE = False # in case of several results, otherwise do the mean+std
SORTED = True # sort the histograms by score
FACTOR_STD = 1. # 1.96 for 95% confidence interval
FULL = False # try and plot all simple + t_ (single-context) grammars

DO_ONLY = {'syll': 'syll', 'colloc': 'colloc', 
        't_readapt_colloc': 't_colloc_shr_vocab', 
        't_syll': 't_syll_spl_vocab', 
        't_readapt_colloc+': 't_colloc_w/_common', 
        'colloc_syll': 'colloc_syll', 
        't_colloc_syll': 't_colloc_syll_spl_vocab',
        't_readapt_colloc_syll': 't_colloc_syll_shr_vocab',
        't_colloc_syll+': 't_colloc_syll_w/_common'}
if FULL:
    DO_ONLY = {'unigram': 'unigram', 'syll': 'syll', 'colloc': 'colloc', 
            't_readapt_colloc': 't_colloc_shr_vocab', 
            't_colloc': 't_colloc_spl_vocab', 
            't_syll': 't_syll_spl_vocab',
            't_readapt_colloc+': 't_colloc_w/_common', 
            'colloc_syll': 'colloc_syll', 
            't_colloc_syll': 't_colloc_syll_spl_vocab',
            't_readapt_colloc_syll': 't_colloc_syll_shr_vocab',
            't_colloc_syll+': 't_colloc_syll_w/_common'}
if TEST:
    DO_ONLY = {'t_nopfx_coll_syll+': 't_colloc_syll_w/_common_nopfx',
            't_test_coll_syll+': 't_colloc_syll_w/_common_test',
            't_nopfx_coll_syll': 't_colloc_syll_spl_vocab_nopfx',
            'test_coll_syll': 'colloc_syll_test',
            't_test_coll_syll': 't_colloc_syll_spl_vocab_test'}
#DO_ONLY = {}
# for cosmetics when preparing figures for papers
# e.g. DO_ONLY = {'t_colloc': 'colloc with topics'}

scores_order = "token_f-score token_precision token_recall boundary_f-score boundary_precision boundary_recall".split()
results = defaultdict(lambda: [dict(zip(scores_order, [[] for i in range(len(scores_order))])) for tmp_i in range(N_MONTHS)])
if TAKE_MAX_SCORE:
    results = defaultdict(lambda: [dict(zip(scores_order, [0 for i in range(len(scores_order))])) for tmp_i in range(N_MONTHS)])

for month in xrange(SAGE, EAGE+1):
    for fname in glob.iglob(PREFIX+'naima_' + str(SAGE_XPS) + 'to' + str(month) 
            + 'm/nai*-' + str(SAGE_XPS) + '-' + str(month) + '*.o*'):
        if TEST and (not "test" in fname and not "nopfx" in fname):
            continue
        elif not TEST and ("test" in fname or "nopfx" in fname):
            continue
        if "-sc" in fname and not "single-context" in TYPES:
            continue
        if "docs" in fname and not "topics" in TYPES:
            continue
        # always plots basic results currently
        doit = False
        with open (fname.replace(".o", ".e")) as f:
            line = ""
            for line in f:
                for iternumber in ITERS:
                    if str(iternumber) + " iterations" in line:
                        doit = True
                        break
        if not doit:
            print "NOT DOING:", fname
            continue
        print fname
        scores = []
        s_dict = {}

        with open(fname) as f:
            last_lines = []
            for line in f:
                last_lines.append(line)
                if len(last_lines) > 5: # just for smoothing results a little
                    last_lines.pop(0)
            try:
                if TEST:
                    scores = [np.mean(map(lambda x: float(x.split('\t')[i]), last_lines)) for i in range(6)]
                else:
                    scores = [float(last_lines[-1].split('\t')[i]) for i in range(6)]
                s_dict = dict(zip(scores_order, scores))
            except:
                pass
        fname = '/'.join(fname.split('/')[1:])
        if 'docs' in fname:
            condname = '_'.join(fname.split('/')[-1].split('-')[-1].split('.')[0].split('_')[2:])
            if condname == '': # topics-based unigram
                condname = 'uni'
            condname = 'd_' + condname
        elif '-sc' in fname:
            fname = fname.replace('-sc', '')
            condname = 't'
            if '-r' in fname:
                condname = 't_readapt'
                fname = fname.replace('-r', '')
            condname = '_'.join([condname] + fname.split('/')[-1].split('-')[3:]).split('.')[0]
        else:
            condname = '_'.join(fname.split('/')[-1].split('-')[3:]).split('.')[0]

        ##########  cosmetic (for legends) ##########
        if len(DO_ONLY):
            if condname in DO_ONLY:
                condname = DO_ONLY[condname]
            else:
                continue
        ########## /cosmetic (for legends) ##########

        if len(s_dict) == 6:
            if TAKE_MAX_SCORE:
                if results[condname][month-SAGE]['token_f-score'] == 0 or s_dict['token_f-score'] > results[condname][month-SAGE]['token_f-score']:
                    results[condname][month-SAGE] = s_dict
            else:
                for k, v in s_dict.iteritems():
                    results[condname][month-SAGE][k].append(v)

print results
        

fig = plt.figure(figsize=(12, 9), dpi=1200)
plt.xticks(xrange(N_MONTHS))

ax = plt.gca()
ax.set_ylim([0.55, 0.90])
ax.set_xlim([-0.1, N_MONTHS - 0.9])
ax.set_xticklabels(map(str, range(SAGE, EAGE+1)))
for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] +
        ax.get_xticklabels() + ax.get_yticklabels()):
    item.set_fontsize(24)
for cond, a in results.iteritems():
    linetype = ''
    if "syll" in cond:
        linetype = '^-.'
    else:
        linetype = 'v-.'
    if "d_" or "t_" in cond:
        linetype = linetype[0] + '--'
    vals = None
    stddevs = None
    if TAKE_MAX_SCORE:
        vals = [x['token_f-score'] for x in a]
    else:
        vals = [np.mean(x['token_f-score']) for x in a]
        stddevs = [FACTOR_STD*np.std(x['token_f-score']) for x in a] # TODO (gaussian process or some smoothing)
    plt.plot(map(lambda x: 'NaN' if x <= 0.0 else x, vals), linetype, linewidth=3.5, alpha=0.8)
    
plt.xlabel('months')
plt.ylabel('token f-score')
plt.legend([l for l in results.iterkeys()], loc='best', ncol=4)
plt.setp(ax.get_legend().get_texts(), fontsize=20)
plt.savefig('progress_ages.png')

matplotlib.rcParams.update({'font.size': 20})
matplotlib.rcParams.update({'text.color': "black"})
matplotlib.rcParams.update({'axes.labelcolor': "black"})
matplotlib.rcParams.update({'xtick.color': "black"})
matplotlib.rcParams.update({'ytick.color': "black"})

plotted_results = {} # plotted_results[month][cond][score_type] = mean

for month in xrange(SAGE, EAGE+1):
    y_pos = [0.5]
    scores = []
    stddevs = []
    conds = []
    s_dicts = []
    for cond, a in results.iteritems():
        score = 0
        stddev = 0
        if TAKE_MAX_SCORE:
            score = a[month-SAGE]['token_f-score']
        else:
            score = np.mean(a[month-SAGE]['token_f-score'])
            stddev = FACTOR_STD*np.std(a[month-SAGE]['token_f-score'])
        if score > 0:
            y_pos.append(y_pos[-1] + 1)
            scores.append(score)
            stddevs.append(stddev)
            conds.append(cond)
            s_dicts.append({'token_f-score': score,
                'token_precision': np.mean(a[month-SAGE]['token_precision']),
                'token_recall': np.mean(a[month-SAGE]['token_recall']),
                'boundary_f-score': np.mean(a[month-SAGE]['boundary_f-score']),
                'boundary_precision': np.mean(a[month-SAGE]['boundary_precision']),
                'boundary_recall': np.mean(a[month-SAGE]['boundary_recall'])})
    plotted_results[month] = dict(zip(conds, s_dicts))
    if len(conds) == 0:
        continue
    y_pos = y_pos[:-1]
    fig = plt.figure(figsize=(9, len(y_pos)), dpi=1200)
    ax = plt.gca()
    ax.set_ylim([0, len(y_pos)+1])
    ax.set_xlim([0.6, 0.86])
    if TEST:
        ax.set_xlim([0.7, 0.86])
    tmp = ()
    if TAKE_MAX_SCORE:
        tmp = zip(y_pos, scores, conds, ['g' for tmp_i in range(len(y_pos))])
        tmp = map(lambda (y, s, cond, color): (y, s, cond, 'b') if 't' == cond[0] or 'd' == cond[0] else (y, s, cond, color), tmp)
    else:
        tmp = zip(y_pos, scores, stddevs, conds, ['g' for tmp_i in range(len(y_pos))])
        tmp = map(lambda (y, s, sd, cond, color): (y, s, sd, cond, 'b') if 't' == cond[0] or 'd' == cond[0] else (y, s, sd, cond, color), tmp)
    if SORTED:
        ys = map(lambda x: x[0], tmp)
        tmp = sorted(tmp, key=lambda x: x[1])
        tmp = map(lambda y,t: sum(((y,), t[1:]), ()), ys, tmp)
    if TAKE_MAX_SCORE:
        y_pos, scores, conds, colors = zip(*tmp)
        plt.barh(y_pos, scores, color=colors, ecolor='r', alpha=0.7)
    else:
        y_pos, scores, stddev, conds, colors = zip(*tmp)
        plt.barh(y_pos, scores, xerr=stddev, color=colors, ecolor='r', alpha=0.7)
    plt.yticks(map(lambda x: x+0.5, y_pos), conds)
    plt.xlabel('token f-score')
    #plt.title('')
    plt.savefig('histogram_' + str(SAGE_XPS) + 'to' + str(month) + 'm.png', bbox_inches='tight')


from pandas import DataFrame
from copy import deepcopy
import pandas as pd
mydata = defaultdict(lambda: [])
ages_max_points = [0 for i in xrange(SAGE, EAGE+1)]
results_m = deepcopy(results)
for cond, a in results_m.iteritems():
    for i, x in enumerate(a):
        if len(x['token_f-score']) > ages_max_points[i]:
            ages_max_points[i] = len(x['token_f-score'])
        mydata[cond].append(x['token_f-score'])
mydata['months'] = [[m for i in range(ages_max_points[m-SAGE])] for m in xrange(SAGE, EAGE+1)]
#mydata['months'] = [[str(m) for i in range(ages_max_points[m-SAGE])] for m in xrange(SAGE, EAGE+1)] # TODO if we don't want the stat_smooth to know about X (months)
for key, value in mydata.iteritems():
    for i, l in enumerate(value):
        value[i] = l + [np.nan for j in range(ages_max_points[i] - len(l))]
    mydata[key] = [j for i in value for j in i]
print mydata
mydataframe = DataFrame(mydata)
my_lng = pd.melt(mydataframe[['months', 't_colloc_syll_shr_vocab', 'colloc_syll', 't_colloc_syll_w/_common', 't_colloc_syll_spl_vocab']], id_vars='months')
if FULL:
    my_lng = pd.melt(mydataframe[['months', 'unigram', 'colloc', 'syll', 't_colloc_spl_vocab', 't_colloc_shr_vocab', 't_colloc_w/_common', 't_syll_spl_vocab', 't_colloc_syll_shr_vocab', 'colloc_syll', 't_colloc_syll_w/_common', 't_colloc_syll_spl_vocab']], id_vars='months')

# from ggplot_import_*
# #p = ggplot(aes(x='months', y='colloc'), data=mydataframe) + geom_point(color='lightgreen') + stat_smooth(se=True) + xlab('age in months') + ylab('token f-score')
# my_lng = pd.melt(mydataframe[['months', 't_colloc syll shr vocab', 'colloc syll', 't_colloc_syll_w/_common', 't_colloc_syll_spl_vocab', 'colloc', 'syll', 't_syll_spl_vocab']], id_vars='months')
# #p = ggplot(aes(x='months', y='value', color='variable'), data=my_lng) + stat_smooth(se=True, method='lm', level=0.95) + xlab('age in months') + ylab('token f-score')
# p = ggplot(aes(x='months', y='value', color='variable'), data=my_lng) + stat_smooth(se=False) + xlab('age in months') + ylab('token f-score')
# ggsave(p, 'ggplot_progress.png')


import rpy2.robjects as robj
import rpy2.robjects.pandas2ri # for dataframe conversion
from rpy2.robjects.packages import importr
from rpy2.robjects import globalenv
import pandas.rpy.common as com

#grdevices = importr('grDevices')
#robj.pandas2ri.activate()

#data_r = robj.conversion.py2ri(mydata)
lng_r = com.convert_to_r_dataframe(my_lng)
data_r = com.convert_to_r_dataframe(mydataframe)
globalenv['lng_r'] = lng_r
globalenv['data_r'] = data_r
globalenv['eage'] = EAGE
globalenv['sage'] = SAGE
print "==================="
print "and now for the R part"
print "==================="
plotFunc_2 = robj.r("""
                library("ggplot2")
                library("grid")

                #print(lng_r)
                #print(factor(lng_r$months))
                #print(factor(lng_r$variable))

                cLevels <- levels(lng_r$variable)

                p <- ggplot(data=lng_r, aes(x=months, y=value, group=variable, colour=variable, fill=variable))\
                + scale_y_continuous(name='token f-score')\
                + scale_x_discrete('age in months', breaks=seq(eage,sage), labels=seq(eage,sage))\
                + coord_cartesian(xlim = c(eage, sage))\
                + theme_bw()\
                + scale_colour_discrete("model", drop=TRUE, limits=cLevels)\
                + scale_fill_discrete("model", drop=TRUE, limits=cLevels)\
                + stat_smooth(level=0.68, size=1.2)\
                + opts(legend.position = c(0.98, 0.5),
                       legend.justification = c(1, 0.5),
                       legend.background = element_rect(colour = "grey70", fill = "white"),
                       legend.text=element_text(size=44),
                       legend.title=element_text(size=44),
                       legend.key.size=unit(2, "cm"),
                       plot.margin=unit(c(1,1,1,1), "cm"))\
                + theme(text = element_text(size=44))
                #+ geom_point()
                #+ xlab('age in months')\
                #+ ylab('token f-score')\
                #+ scale_x_continuous('age in months', breaks=seq(eage,sage), limits=c(eage,sage))\

                ggsave('ggplot2_progress.pdf', plot=p, width=22, height=16)

                """)
# + scale_x_discrete('age in months') 


print "==================="
print "and now for the LaTeX tables"
print "==================="


header_table = """
\begin{table*}[ht] \caption{Mean f-scores (f), precisions (p), and recalls (r) for different models depending on the size of dataset}
\vspace{-0.5cm}
\begin{center}
\begin{scriptsize}
\begin{tabular}{|c|ccc|ccc|ccc|ccc|ccc|ccc|ccc|ccc|}
\hline
& \multicolumn{3}{|c|}{syll}
& \multicolumn{3}{|c|}{t\_syll}
& \multicolumn{3}{|c|}{colloc}
& \multicolumn{3}{|c|}{t\_coll\_w/\_common}
& \multicolumn{3}{|c|}{coll\_syll}
& \multicolumn{3}{|c|}{t\_coll\_syll\_shr\_voc}
& \multicolumn{3}{|c|}{t\_coll\_syll\_spl\_voc}
& \multicolumn{3}{|c|}{t\_coll\_syll\_w/\_com}\\\\
"""
print header_table
for typ in ['token', 'boundary']:
    print typ + """ & f & p & r & f & p & r & f & p & r & f & p & r & f & p & r & f & p & r & f & p & r & f & p & r \\\\
        \hline """

    for month, d in plotted_results.iteritems():
        print str(SAGE_XPS) + "-" + str(month),
        for cond in ['syll', 't_syll_spl_vocab', 'colloc', 't_colloc_w/_common', 'colloc_syll', 't_colloc_syll_shr_vocab', 't_colloc_syll_spl_vocab', 't_colloc_syll_w/_common']:
            s_dict = d[cond]
            f = s_dict[typ+'_f-score']
            p = s_dict[typ+'_precision']
            r = s_dict[typ+'_recall']
            print " & ",
            print "%.3f" % f,
            print " & ",
            print "%.3f" % p,
            print " & ",
            print "%.3f" % r,
        print "\\\\"
    print "\hline"

footer_table = """
\end{tabular}
\label{results}
\end{scriptsize}
\end{center}
\end{table*}
"""
print footer_table
