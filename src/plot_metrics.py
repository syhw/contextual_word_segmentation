import sys, glob
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict

usage = """python src/plot_metrics.py folder
the folder should contain models_iters_[topic].(type|word)scores,
along with lexscores.csv
e.g. python src/plot_metrics.py naima_11to24m"""

DO_ONLY = {"colloc_syll": "baseline",
           "colloc_syll_sc": "split vocab",
           "readapt_colloc_syll_sc": "share vocab",
           "colloc_common_syll_sc": "with common"}
ITF_FUNC = lambda x: np.log2(1 + x)
#ITF_FUNC = lambda x: x
FIT_GAUSSIAN = False
SCATTER = False
HIST1D = True
FLIP = False
EQUAL_PTS_PER_BIN = True


# TODO search for 11 and 24 ;-)

##############################

from numpy import *
from scipy import optimize

def gaussian(height, center_x, center_y, width_x, width_y):
    """Returns a gaussian function with the given parameters"""
    width_x = float(width_x)
    width_y = float(width_y)
    return lambda x,y: height*exp(
        -(((center_x-x)/width_x)**2+((center_y-y)/width_y)**2)/2)

def moments(data):
    """Returns (height, x, y, width_x, width_y) the gaussian parameters of a 2D distribution by calculating its moments """
    total = data.sum()
    X, Y = indices(data.shape)
    x = (X*data).sum()/total
    y = (Y*data).sum()/total
    col = data[:, int(y)]
    width_x = sqrt(abs((arange(col.size)-y)**2*col).sum()/col.sum())
    row = data[int(x), :]
    width_y = sqrt(abs((arange(row.size)-x)**2*row).sum()/row.sum())
    height = data.max()
    return height, x, y, width_x, width_y

def fitgaussian(data):
    """Returns (height, x, y, width_x, width_y) the gaussian parameters of a 2D distribution found by a fit"""
    params = moments(data)
    errorfunction = lambda p: ravel(gaussian(*p)(*indices(data.shape)) -
    data)
    p, success = optimize.leastsq(errorfunction, params)
    return p

##############################



def condname_topic(filename):
    condname = filename.split('/')[-1]
    condname = condname.split('.')[0]
    condname = condname.replace('_500', '')
    topic = 'all'
    if '_t' in condname:
        topic = condname.split('_')[-1]
        condname = '_'.join(condname.split('_')[:-1])
    return condname, topic


def compute_ttf_itf(P_w_knowing_t, P_t, sum_t):
    """ttf_itf[w_n][t_k] = P(w_n | t_k) / ITF_FUNC( \sum_k P(w_n | t_k).P(t_k) )
    normalized
    """
    ttf_itf = defaultdict(lambda: {})
    sum_w = 0.
    # normalize P_w_knowing_t and compute denominators
    for word, rest in P_w_knowing_t.iteritems():
        denom_w = 0.
        for topic, p in rest.iteritems():
            rest[topic] /= sum_t[topic]
            denom_w += rest[topic] * P_t[topic]
        denom_w = ITF_FUNC(denom_w)
        unormalized_ttf_itf = rest[topic] / denom_w
        ttf_itf[word][topic] = unormalized_ttf_itf 
        sum_w += unormalized_ttf_itf
    # normalize ttf_itf
    ttf_itf_w = {}
    for word, rest in ttf_itf.iteritems():
        sum_ = 0.
        for topic in rest.iterkeys():
            rest[topic] /= sum_w
            sum_ += rest[topic]
        ttf_itf_w[word] = sum_
    return ttf_itf, ttf_itf_w


def corresponding_topics(condname, folder):
    searchstr = "/home/gsynnaeve/topicanalysis/" + folder + condname + "_500*.topics_count"
    for filename in glob.iglob(searchstr):
        with open(filename) as f:
            lines = map(lambda l: l.rstrip('\n'), f.readlines())
        P_t = dict(map(lambda l: (l.split('=')[1].rstrip(')'), float(l.split('=')[2])), lines[:7]))
        P_w_knowing_t = defaultdict(lambda: {})
        sum_t = defaultdict(lambda: 0.)
        current_topic = None
        for line in lines:
            if '---' in line: # end
                break
            if "w=\tP'(w|" in line:
                current_topic = line.split('|')[1][:2]
                continue
            if current_topic == None: # header
                continue
            l = line.strip(' \n').split('\t')
            if len(l[3]):
                word = l[3].lower()
                count = float(l[2])
                P_w_knowing_t[word][current_topic] = count
                sum_t[current_topic] += count
        ttf_itf = compute_ttf_itf(P_w_knowing_t, P_t, sum_t)
    return ttf_itf
    

def plot_tokenscores(folder):
    tokenscores = {}
    #for filename in glob.iglob(folder + '*5??*.tokenscores'):
    for filename in glob.iglob(folder + '*500*.tokenscores'):
        with open(filename) as f:
            lines = map(lambda l: l.rstrip('\n'), f.readlines())
        scores = lines[-1].split('\t') # token f,p,r, boundary f,p,r
        condname, topic = condname_topic(filename)
        if not condname in tokenscores:
            tokenscores[condname] = {}
        if not topic in tokenscores[condname]:
            tokenscores[condname][topic] = {}
        for i, scorename in enumerate(lines[0].split('\t')):
            tokenscores[condname][topic][scorename] = float(scores[i])

    y_pos = []
    s = []
    conds = []
    colors = []
    y = -0.5
    for condname, rest in tokenscores.iteritems():
        if condname not in DO_ONLY:
            continue
        print "doing tokenf:", condname
        y += 1
        for topic, scores in rest.iteritems():
            y_pos.append(y)
            y += 1
            s.append(scores['token_f-score'])
            conds.append(DO_ONLY[condname] + ' ' + topic)
            if 'baseline' in conds[-1]:
                colors.append('grey')
            elif 'with common' in conds[-1]:
                colors.append('g')
            elif 'share vocab' in conds[-1]:
                colors.append('c')
            else:
                colors.append('b')
    matplotlib.rcParams.update({'font.size': 20})
    matplotlib.rcParams.update({'text.color': "black"})
    matplotlib.rcParams.update({'axes.labelcolor': "black"})
    matplotlib.rcParams.update({'xtick.color': "black"})
    matplotlib.rcParams.update({'ytick.color': "black"})
    fig = plt.figure(figsize=(9, y_pos[-1]+1), dpi=1200)
    ax = plt.gca()
    ax.set_ylim([0, y_pos[-1]+1])
    ax.set_xlim([0.6, 0.86])
    plt.barh(y_pos, s, color=colors, alpha=0.8)
    plt.yticks(map(lambda x: x+0.5, y_pos), conds)
    plt.xlabel('Token F-score')
    plt.savefig('tokenf_pertopic_' + str(11) + 'to' + str(24) + 'm.png', bbox_inches='tight')


def plot_typescores(folder):
    typescores = {}
    fulltypes_fscores = defaultdict(lambda: {})
    ttf_itf_w_t = {}
    ttf_itf_w = {}
    types_to_do = ['you/u', 'the', 'yeah', 'mommy', 'daddy', 'doing', 'does', 'going', 'yogurt', 'bare/bear', 'cheese', 'not/knot']
    #for filename in glob.iglob(folder + '*5??*.typescores'):
    for filename in glob.iglob(folder + '*500*.typescores'):
        with open(filename) as f:
            lines = map(lambda l: l.rstrip('\n'), f.readlines())
        condname, topic = condname_topic(filename)
        if '_sc' in condname:
            ttf_itf_w_t[condname], ttf_itf_w[condname] = corresponding_topics(condname, folder) # TODO [folder]
        keys = lines[0].split(',')
        for line in lines[1:]:
            l = line.split(',')
            type = l[0]
            for i, scorename in enumerate(keys[1:]):
                if topic == 'all' and scorename == 'tf':
                    fulltypes_fscores[condname][type] = float(l[i+1])
            if type not in types_to_do:
                continue
            if condname not in typescores:
                typescores[condname] = {}
            if topic not in typescores[condname]:
                typescores[condname][topic] = {}
            typescores[condname][topic][type] = {}
            for i, scorename in enumerate(keys[1:]):
                typescores[condname][topic][type][scorename] = float(l[i+1])

    y_pos = []
    s = []
    conds = []
    colors = []
    y = -0.5
    for condname, rest in typescores.iteritems():
        if condname not in DO_ONLY:
            continue
        print "doing typef:", condname
        y += 1
        for type in types_to_do:
            y += 0.5
            for topic, scores in rest.iteritems():
                y_pos.append(y)
                y += 0.5
                #s.append(scores[type]['tf']) TODO
                s.append(np.log(1. + scores[type]['tf']))
                conds.append('"' + type + '" ' + DO_ONLY[condname] + ' ' + topic)
                if 'baseline' in conds[-1]:
                    colors.append('grey')
                elif 'with common' in conds[-1]:
                    colors.append('g')
                elif 'share vocab' in conds[-1]:
                    colors.append('c')
                else:
                    colors.append('b')
    matplotlib.rcParams.update({'font.size': 10})
    matplotlib.rcParams.update({'text.color': "black"})
    matplotlib.rcParams.update({'axes.labelcolor': "black"})
    matplotlib.rcParams.update({'xtick.color': "black"})
    matplotlib.rcParams.update({'ytick.color': "black"})
    #fig = plt.figure(figsize=(y_pos[-1]+1, 11), dpi=1200)
    fig = plt.figure(figsize=(9, y_pos[-1]+1), dpi=1200)
    ax = plt.gca()
    #ax.set_xlim([0, y_pos[-1]+1])
    ax.set_ylim([0, y_pos[-1]+1])
    #ax.set_ylim([0.6, 0.86])
    plt.barh(y_pos, s, color=colors, height=0.4, alpha=0.8)
    #plt.bar(y_pos, s, color=colors, width=0.4, alpha=0.8)
    plt.yticks(map(lambda x: x+0.2, y_pos), conds)
    #plt.xticks(map(lambda x: x+0.2, y_pos), conds)
    #plt.title('type f-score') TODO
    plt.title('type log(1 + F-score)')
    plt.savefig('typef_pertopic_' + str(11) + 'to' + str(24) + 'm.png', bbox_inches='tight')

    plt.clf()
    fig = plt.figure(figsize=(9, 9), dpi=1200)
    XMIN = -0.00005
    XMAX = 0.00105 
    YMIN = -0.01
    YMAX = 1.01
    dataset = []
    colors = []
    condis = []
    if SCATTER:
        plt.xlim([XMIN, XMAX])
        plt.ylim([YMIN, YMAX])
    for condname, word_fscore in fulltypes_fscores.iteritems():
        if condname not in DO_ONLY:
            continue
        cond = DO_ONLY[condname]
        if 'baseline' in cond:
            continue
        print "doing scatter ttf-itf vs typef:", cond
        type_f_l = []
        ttf_itf_l = []
        for word, fscore in word_fscore.iteritems():
            for w in word.split('/'):
                #print w
                #print ttf_itf_w[condname].keys()
                if w in ttf_itf_w[condname]:
                    type_f_l.append(fscore)
                    ttf_itf_l.append(ttf_itf_w[condname][w])
        #print ttf_itf_l
        #print type_f_l
        data = np.array(zip(ttf_itf_l, type_f_l))
        cmaps = {'b': 'Blues', 'g': 'BuGn', 'c': 'OrRd', 'grey': 'binary'}
        color = 'b'
        if 'baseline' in cond:
            color = 'grey'
        elif 'with common' in cond:
            color = 'g'
        elif 'share vocab' in cond:
            color = 'c'

        if SCATTER:
            plt.scatter(ttf_itf_l, type_f_l, s=10, c=color, label=cond, alpha=0.6)
        elif HIST1D:
            if FLIP:
                dataset.append(np.array([data[:,1], data[:,0]])) # data[:,::-1]
            else:
                dataset.append(data)
            colors.append(color)
            condis.append(cond)
        else:
            H, xedges, yedges = np.histogram2d(ttf_itf_l, type_f_l, bins=64)
            H = np.rot90(H)
            H = np.flipud(H)
            #H = H.T
            Hmasked = np.ma.masked_where(H==0,H)
            plt.pcolormesh(xedges,yedges,Hmasked,cmap=cmaps[color],alpha=0.5)
        if FIT_GAUSSIAN:
            # TODO
            pass
#                from sklearn import mixture
#                clf = mixture.GMM(n_components=1, covariance_type='full')
#                clf.fit(data)
#                x = np.linspace(XMIN, XMAX)
#                y = np.linspace(YMIN, YMAX)
#                X, Y = np.meshgrid(x, y)
#                XX = np.c_[X.ravel(), Y.ravel()]
#                Z = np.log(-clf.score_samples(XX)[0])
#                Z = Z.reshape(X.shape)
#                CS = plt.contour(X, Y, Z)
            #from pylab import *
            #params = fitgaussian(data)
            #fit = gaussian(*params)
            #plt.contour(fit(*indices(data.shape)), cmap=cm.copper)
###                from matplotlib.mlab import griddata
###                # define grid.
###                xi = np.linspace(XMIN,XMAX,200)
###                yi = np.linspace(YMIN,YMAX,200)
###                # grid the data.
###                zi = griddata(ttf_itf_l,type_f_l,z,xi,yi,interp='linear')
###                CS = plt.contour(xi,yi,zi,15,linewidths=0.5,colors='k')

    x_label = 'TTF-ITF'
    y_label = 'Type F-score'
    if HIST1D:
        if EQUAL_PTS_PER_BIN:
            from scipy import stats
            nbins = 3
            #bin_edges = zip(map(lambda x: stats.mstats.mquantiles(x, [i/(1.*nbins) for i in range(nbins+1)]), dataset))
            dataset = map(lambda x: np.array([np.log(1+np.log(1+data[:,0])), data[:,1]]), dataset)
            x_label += ' (log log)'
            fulldata = np.concatenate(dataset, axis=0)
            mi = np.min(fulldata)
            ma = np.max(fulldata)
            bin_edges = stats.mstats.mquantiles(fulldata, [i/(1.*nbins) for i in [k for k in np.arange(mi, ma, step=(ma-mi)/nbins)] + [ma]])
            print bin_edges
            plt.hist(dataset, bin_edges, stacked=1, histtype='bar', color=colors, label=condis)
        else:
            plt.hist(dataset, 24, normed=1, histtype='bar', color=colors, label=condis)
    if SCATTER or HIST1D:
        plt.legend(bbox_to_anchor=(0.5, 1.05), ncol=3, loc=9, borderaxespad=0.)
    if FLIP:
        x_label, y_label = y_label, x_label
    if HIST1D:
        y_label = '$\sum$ ' + y_label
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.savefig('ttf_itf_vs_typef_' + str(11) + 'to' + str(24) + 'm.png', bbox_inches='tight')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print usage
        sys.exit(-1)
    folder = sys.argv[1].rstrip('/') + '/' 
    plot_tokenscores(folder)
    plot_typescores(folder)
    # TODO: plot_lexiconscores(folder)
    # TODO: plot for a series of folders in increasing age

