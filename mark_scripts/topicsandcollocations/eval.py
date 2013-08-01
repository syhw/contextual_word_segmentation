#! /usr/bin/env python

usage = """%prog -- evaluate word segmentation

Version of 14th February 2010

(c) Mark Johnson

usage: %prog [options]

"""

import lx, tb
import optparse, re, sys

def tree_words(tree, score_cat_rex, ignore_terminal_rex):

    def visit(node, wordssofar, segssofar):
        """Does a preorder visit of the nodes in the tree"""
        if tb.is_terminal(node):
            if not ignore_terminal_rex.match(node):
                segssofar.append(node)
            return wordssofar,segssofar
        for child in tb.tree_children(node):
            wordssofar,segssofar = visit(child, wordssofar, segssofar)
        if score_cat_rex.match(tb.tree_label(node)):
            if segssofar != []:
                wordssofar.append(''.join(segssofar))
                segssofar = []
        return wordssofar,segssofar

    wordssofar,segssofar = visit(tree, [], [])
    assert(segssofar == [])
    return wordssofar

def words_stringpos(ws):
    stringpos = set()
    left = 0
    for w in ws:
        right = left+len(w)
        stringpos.add((left,right))
        left = right
    return stringpos
    
def read_data(inf, tree_flag, types_flag, score_cat_rex, ignore_terminal_rex, word_split_rex, debug_level=0, max_lines=0):
    "Reads data from inf, either in tree format or in flat format"
    strippedlines = [line.strip() for line in inf]

    if max_lines > 0:
        if len(strippedlines) < max_lines:
            sys.stderr.write("Warning: max_lines=%d, len(strippedlines) = %d\n"%(max_lines,len(strippedlines)))
        strippedlines = strippedlines[0:max_lines]

    if tree_flag:
        lines0 = []
        for line in strippedlines:
            trees = tb.string_trees(line)
            trees.insert(0, 'ROOT')
            lines0.append(tree_words(trees, score_cat_rex, ignore_terminal_rex))
            if debug_level >= 10000:
                sys.stderr.write("# line = %s,\n# words = %s\n"%(line, lines0[-1]))
    else:
        lines0 = [[word for word in word_split_rex.split(line) if word != ""] for line in strippedlines]

    if types_flag:
        lines = []
        dejavu = set()
        for words in lines0:
            word = ''.join(words)
            if word not in dejavu:
                dejavu.add(word)
                lines.append(words)
    else:
        lines = lines0
        
    # print "# tree_flag =", tree_flag, "source =", strippedlines[-1], "line =", lines[-1]
    
    sentences = [''.join(ws) for ws in lines]
    stringpos = [words_stringpos(ws) for ws in lines]
    return (sentences,stringpos)

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
        
def evaluateall(trainwords, trainstringpos, goldwords, goldstringpos, topicdata, options):
    assert(trainwords == goldwords)
    evaluate(trainwords, trainstringpos, goldwords, goldstringpos, options.debug)
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
    parser.add_option("-c", "--score-cat-re", dest="score_cat_re", default=r"$",
                      help="score categories in tree input that match this regex")
    parser.add_option("-i", "--ignore-terminal-re", dest="ignore_terminal_re", default=r"^[$]{3}$",
                      help="filter substrings of terminals that match this regex")
    parser.add_option("-m", "--word-split-re", dest="word_split_re", default=r"[- \t]+",
                      help="regex used to split words with non-tree input")
    parser.add_option("--types", dest="types_flag", default=False,
                      action="store_true", help="ignore multiple lines with same yield")
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

    score_cat_rex = re.compile(options.score_cat_re)
    ignore_terminal_rex = re.compile(options.ignore_terminal_re)
    word_split_rex = re.compile(options.word_split_re)
    
    (goldwords,goldstringpos) = read_data(goldf, tree_flag=options.goldtree_flag, types_flag=options.types_flag,
                                          score_cat_rex=score_cat_rex, ignore_terminal_rex=ignore_terminal_rex,
                                          word_split_rex=word_split_rex, max_lines=options.nsentences)

    topicdata = None
    if topicalwords:
        topicdata = topicwords_goldpos(topicalwords, goldwords, goldstringpos, options.debug)

    sys.stdout.write("# f-score\tprecision\trecall");
    if topicdata:
        sys.stdout.write("\ttopic-f-score\ttopic-precision\ttopic-recall\tneighbour-f-score\tneighbour-precision\tneighbour-recall")
    sys.stdout.write("\n")
    sys.stdout.flush()
    
    trainlines = []
    for trainline in trainf:
        trainline = trainline.strip()
        if trainline != "":
            trainlines.append(trainline)
            continue

        (trainwords,trainstringpos) = read_data(trainlines, tree_flag=options.traintree_flag, types_flag=options.types_flag,
                                                score_cat_rex=score_cat_rex, ignore_terminal_rex=ignore_terminal_rex,
                                                word_split_rex=word_split_rex, debug_level=options.debug,
                                                max_lines=options.nsentences)

        evaluateall(trainwords, trainstringpos, goldwords, goldstringpos, topicdata, options)
        trainlines = []

    if trainlines != []:
        (trainwords,trainstringpos) = read_data(trainlines, tree_flag=options.traintree_flag, types_flag=options.types_flag,
                                                score_cat_rex=score_cat_rex, ignore_terminal_rex=ignore_terminal_rex,
                                                word_split_rex=word_split_rex, debug_level=options.debug,
                                                max_lines=options.nsentences)
        evaluateall(trainwords, trainstringpos, goldwords, goldstringpos, topicdata, options)
