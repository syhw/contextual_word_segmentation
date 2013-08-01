#! /usr/bin/env python

usage = """%prog -- evaluate word segmentation and word-topic mappings

Version of 26th May, 2010

(c) Mark Johnson

usage: %prog [options]

"""

import lx, tb
import optparse, re, sys

def read_childes(inf):
    """Reads a CHILDES file, and yields a dictionary for each record
    with key-value pairs for each field"""
    for record in inf.read().split("*mot:\t")[1:]:
        key_val = {}
        fields = record.split("\n%")
        key_val['mot'] = fields[0].strip()
        for field in fields[1:]:
            [key, val] = field.split(":\t", 1)
            key = intern(key.strip())
            val = val.strip()
            if val != '':
                key_val[key] = val
        yield key_val

def tree_words(tree, score_cat_rex, ignore_terminal_rex):
    """maps tree to a list of elements, where each element is a 
    word or a (word,topic) pair"""

    def visit(node, wordssofar, segssofar):
        """Does a preorder visit of the nodes in the tree"""
        if tb.is_terminal(node):
            if not ignore_terminal_rex.match(node):
                segssofar.append(node)
            return wordssofar,segssofar
        for child in tb.tree_children(node):
            wordssofar,segssofar = visit(child, wordssofar, segssofar)
        mo = score_cat_rex.match(tb.tree_label(node))
        if mo:
            if segssofar != []:
                word = ''.join(segssofar)
                segssofar = []
                try:
                    topic = mo.group('topic')
                    if topic != None:
                        wordssofar.append((word,topic))
                    else:
                        wordssofar.append(word)
                except IndexError:
                    wordssofar.append(word)
                
        return wordssofar,segssofar

    wordssofar,segssofar = visit(tree, [], [])

    if segssofar != []:
        sys.stderr.write("!! segssofar = %s, Tree = %s\n"%(segssofar,tree))

    assert(segssofar == [])
    return wordssofar

def string_word(s):
    ws = s.rsplit('_',1)
    if len(ws) == 1:
        return ws[0]
    else:
        return (ws[0],ws[1])

def words_topics(line):
    topics = set()
    for w in line:
        if isinstance(w, tuple):
            topics.add(w[1])
    return topics

def words_stringpos(ws):
    stringpos = set()
    left = 0
    for w in ws:
        if isinstance(w, tuple):
            w = w[0]
        right = left+len(w)
        stringpos.add((left,right))
        left = right
    return stringpos

def words_topicstringpos(ws):
    topicstringpos = set()
    left = 0
    for w in ws:
        if isinstance(w, tuple):
            right = left+len(w[0])
            topicstringpos.add((left,right,w[1]))
        else:
            right = left+len(w)
        left = right
    return topicstringpos
    
def read_data(inf, tree_flag, score_cat_rex, ignore_terminal_rex, debug_level=0, max_lines=0):
    "Reads data from inf, either in tree format or in flat format"
    strippedlines = [line.strip() for line in inf]

    if max_lines > 0:
        if len(strippedlines) < max_lines:
            sys.stderr.write("Warning: max_lines=%d, len(strippedlines) = %d\n"%(max_lines,len(strippedlines)))
        strippedlines = strippedlines[0:max_lines]

    if tree_flag:
        lines = []
        for line in strippedlines:
            trees = tb.string_trees(line)
            trees.insert(0, 'ROOT')
            lines.append(tree_words(trees, score_cat_rex, ignore_terminal_rex))
            if debug_level >= 10000:
                sys.stderr.write("# line = %s,\n# words = %s\n"%(line, lines[-1]))
    else:
        lines = [[string_word(s) for s in line.split()] for line in strippedlines]

    # print "# tree_flag =", tree_flag, "source =", strippedlines[-1], "line =", lines[-1]
    
    sentences = [''.join((w[0] if isinstance(w,tuple) else w for w in ws)) for ws in lines]
    topics = [words_topics(line) for line in lines]
    stringpos = [words_stringpos(ws) for ws in lines]
    topicstringpos = [words_topicstringpos(ws) for ws in lines]
    return (sentences,(stringpos,topics,topicstringpos))

class PrecRec:
    def __init__(self):
        self.test = 0
        self.gold = 0
        self.correct = 0
        self.n = 0
        self.n_exactmatch = 0
    def precision(self):
        return self.correct/(self.test+1e-100)
    def recall(self):
        return self.correct/(self.gold+1e-100)
    def fscore(self):
        return 2*self.correct/(self.test+self.gold+1e-100)
    def exact_match(self):
        return self.n_exactmatch/(self.n+1e-100)
    def update(self, testset, goldset):
        self.n += 1
        if testset == goldset:
            self.n_exactmatch += 1
        self.test += len(testset)
        self.gold += len(goldset)
        self.correct += len(testset & goldset)
#    def __str__(self):
#        return ("%.4g\t%.4g\t%.4g\t%.4g" % (self.exact_match(), self.fscore(), self.precision(), self.recall()))
    def __str__(self):
        return ("%.4g\t%.4g\t%.4g" % (self.fscore(), self.precision(), self.recall()))

def data_precrec(trainwords, goldwords):
    if len(trainwords) != len(goldwords):
        sys.stderr.write("## ** len(trainwords) = %s, len(goldwords) = %s\n" % (len(trainwords), len(goldwords)))
        sys.exit(1)
    pr = PrecRec()
    for (t,g) in zip(trainwords, goldwords):
        pr.update(t, g)
    return pr

def evaluate(trainwords, trainstringpos, goldwords, goldstringpos, debuglevel):
    
    if debuglevel >= 2000:
        for (tw, tsps, gw, gsps) in zip(trainwords, trainstringpos, goldwords, goldstringpos):
            sys.stderr.write("Gold: ")
            for l,r in sorted(list(gsps)):
                sys.stderr.write(" %s"%gw[l:r])
            sys.stderr.write("\nTrain:")
            for l,r in sorted(list(tsps)):
                sys.stderr.write(" %s"%tw[l:r])
            sys.stderr.write("\n")
            
    if goldwords != trainwords:
        sys.stderr.write("## ** gold and train terminal words don't match (so results are bogus)\n")
        sys.stderr.write("## len(goldwords) = %s, len(trainwords) = %s\n" % (len(goldwords), len(trainwords)))
        for i in xrange(min(len(goldwords), len(trainwords))):
            if goldwords[i] != trainwords[i]:
                sys.stderr.write("# first difference at goldwords[%s] = %s\n# first difference at trainwords[%s] = %s\n"%
                                 (i,goldwords[i],i,trainwords[i]))
                break

    pr = str(data_precrec(trainstringpos, goldstringpos))
    sys.stdout.write(pr)

def topicwords_goldpos(topicwords, goldwords, goldstringpos, debug_level=0):
    """remove all the goldstringpos that don't span a string in topicwords, and
    return the locations of the keywords, and the locations of the topicword neighbours"""
    kwglrs = []
    kwgps = []
    nwglrs = []
    nwgps = []
    for (gw,gsps) in zip(goldwords, goldstringpos):
        kwglrs0 = set()
        kwglrs.append(kwglrs0)
        kwgps0 = set()
        kwgps.append(kwgps0)
        nwglrs0 = set()
        nwglrs.append(nwglrs0)
        nwgps0 = set()
        nwgps.append(nwgps0)

        for (l,r) in gsps:
            if gw[l:r] in topicwords:
                kwglrs0.add((l,r))
                for p in xrange(l,r):
                    kwgps0.add(p)

        for (l,r) in gsps:
            if l-1 in kwgps0 or r in kwgps0:
                nwglrs0.add((l,r))
                for p in xrange(l,r):
                    nwgps0.add(p)

        if debug_level >= 2000:
            sys.stderr.write("gold words gw = %s, gold string positions gsps = %s\n"%(gw,gsps))
            sys.stderr.write("key words (left,right) string positions kwglrs0 = %s\n"%kwglrs0)
            sys.stderr.write("key words positions kwgps0 = %s\n"%kwgps0)
            sys.stderr.write("neighbour words (left,right) string positions nwglrs0 = %s\n"%nwglrs0)
            sys.stderr.write("neighbour words positions nwgps0 = %s\n"%nwgps0)
    
    n = len(kwglrs)
    assert(len(kwgps) == n)
    assert(len(nwglrs) == n)
    assert(len(nwgps) == n)
    return ((kwglrs,kwgps), (nwglrs,nwgps))

def topicwords_evaluate(trainlrs, (goldlrs,goldps), goldwords, debug_level=0):
    """remove all trainstringpos that don't overlap with goldposs
    then calculate precision and recall"""
    assert(len(trainlrs) == len(goldlrs))
    pr = PrecRec()
    for (tlrs0,glrs,gps,gws) in zip(trainlrs, goldlrs,goldps, goldwords):
        tlrs = set()
        for (l,r) in tlrs0:
            for p in xrange(l,r):
                if p in gps:
                    tlrs.add((l,r))
                    break
        pr.update(tlrs, glrs)
        if debug_level >= 1500:
            sys.stderr.write("gold words gws = %s\n"%gws)
            sys.stderr.write("gold word (left,right) glrs = %s\n"%sorted(list(glrs)))
            sys.stderr.write("train word (left,right) tlrs0 = %s\n"%sorted(list(tlrs0)))
            sys.stderr.write("train word (left,right) tlrs = %s\n"%sorted(list(tlrs)))
    sys.stdout.write(str(pr))
        
def evaluateall(trainwords, (trainstringpos,traintopics,traintopicstringpos), 
                goldwords, (goldstringpos,goldtopics,goldtopicstringpos), 
                topicdata, options):
    assert(trainwords == goldwords)
    evaluate(trainwords, trainstringpos, goldwords, goldstringpos, options.debug)

    topic_pr = data_precrec(traintopics, goldtopics)
    sys.stdout.write('\t%.4g\t'%topic_pr.exact_match())
    sys.stdout.write(str(topic_pr))
    sys.stdout.flush()

    # sys.stderr.write("# traintopicstringpos[:10] = %s\n"%traintopicstringpos[:10])
    # sys.stderr.write("# goldtopicstringpos[:10] = %s\n"%goldtopicstringpos[:10])

    sys.stdout.write('\t')
    sys.stdout.write(str(data_precrec(traintopicstringpos, goldtopicstringpos)))
    sys.stdout.flush()

    if topicdata:
        sys.stdout.write('\t')
        sys.stdout.flush()
        topicwords_evaluate(trainstringpos, topicdata[0], goldwords, options.debug)
        sys.stdout.write('\t')
        sys.stdout.flush()
        topicwords_evaluate(trainstringpos, topicdata[1], goldwords, options.debug)
    sys.stdout.flush()
    if (options.extra):
        sys.stdout.write('\t')
        sys.stdout.write(options.extra)
    sys.stdout.write('\n')
    sys.stdout.flush()

if __name__ == '__main__':
    parser = optparse.OptionParser(usage=usage)
    parser.add_option("-n", "--nsentences", dest="nsentences", type="int", default=0,
                      help="evaluate only the first n sentences (0=evaluate all)")
    parser.add_option("-g", "--gold", dest="goldfile", help="gold file")
    parser.add_option("-t", "--train", dest="trainfile", help="train file")
    parser.add_option("--gold-trees", dest="goldtree_flag", default=False,
                      action="store_true", help="gold data is in tree format")
    parser.add_option("--train-trees", dest="traintree_flag", default=False,
                      action="store_true", help="train data is in tree format")
    parser.add_option("-c", "--score-cat-re", dest="score_cat_re", default=r"Word(?:_(?P<topic>\S+))?",
                      help="score categories in tree input that match this regex; (?P<topic>XXX) indentifies topics")
    parser.add_option("-i", "--ignore-terminal-re", dest="ignore_terminal_re", default=r"^T_\S+$",
                      help="filter substrings of terminals that match this regex")
    parser.add_option("--extra", dest="extra", help="suffix to print at end of evaluation line")
    parser.add_option("--topicalwordsfile", dest="topicalwordsfile", help="file containing topical words to evaluate specially")
    parser.add_option("-d", "--debug", dest="debug", help="print debugging information", default=0, type="int")
    (options,args) = parser.parse_args()
    
    if options.goldfile == options.trainfile:
        sys.stderr.write("## ** gold and train both read from same source\n")
        sys.exit(2)
    if options.goldfile:
        goldf = file(options.goldfile, "rU")
    else:
        goldf = sys.stdin
    if options.trainfile:
        trainf = file(options.trainfile, "rU")
    else:
        trainf = sys.stdin

    topicalwords = None
    if options.topicalwordsfile:
        topicalwords = file(options.topicalwordsfile,"rU").read().split()

    if options.debug >= 10:
        sys.stderr.write("# score_cat_re = %s\n"%options.score_cat_re)
        sys.stderr.write("# ignore_terminal_re = %s\n"%options.ignore_terminal_re)

    score_cat_rex = re.compile(options.score_cat_re)
    ignore_terminal_rex = re.compile(options.ignore_terminal_re)
    
    (goldwords,goldinfo) = read_data(goldf, 
                                     tree_flag=options.goldtree_flag, 
                                     score_cat_rex=score_cat_rex, 
                                     ignore_terminal_rex=ignore_terminal_rex,
                                     max_lines=options.nsentences)

    topicdata = None
    if topicalwords:
        topicdata = topicwords_goldpos(topicalwords, goldwords, goldinfo[0], options.debug)

    sys.stdout.write("# 1.f-score\t2.precision\t3.recall")
    sys.stdout.write("\t4.topic.accuracy\t5.topic.f-score\t6.topic.precision\t7.topic.recall")
    sys.stdout.write("\t8.wordtopic.f-score\t9.wordtopic.precision\t10.wordtopic.recall")
    if topicdata:
        sys.stdout.write("\t11.topicalword.f-score\t12.topicalword.precision\t13.topicalword.recall")
        sys.stdout.write("\t14.neighbour.f-score\t15.neighbour-precision\t16.neighbour-recall")
    sys.stdout.write("\n")
    sys.stdout.flush()
    
    trainlines = []
    for trainline in trainf:
        trainline = trainline.strip()
        if trainline != "":
            trainlines.append(trainline)
            continue

        (trainwords,traininfo) = read_data(trainlines, 
                                           tree_flag=options.traintree_flag,
                                           score_cat_rex=score_cat_rex, 
                                           ignore_terminal_rex=ignore_terminal_rex,
                                           debug_level=options.debug,
                                           max_lines=options.nsentences)

        evaluateall(trainwords, traininfo, goldwords, goldinfo, topicdata, options)
        trainlines = []

    if trainlines != []:
        (trainwords,traininfo) = read_data(trainlines, 
                                           tree_flag=options.traintree_flag,
                                           score_cat_rex=score_cat_rex, 
                                           ignore_terminal_rex=ignore_terminal_rex,
                                           debug_level=options.debug,
                                           max_lines=options.nsentences)
        evaluateall(trainwords, traininfo, goldwords, goldinfo, topicdata, options)
