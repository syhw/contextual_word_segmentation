#! /usr/bin/env python

usage = """%prog Version of 10th November 2009

(c) Mark Johnson

Extracts words and their counts from adaptor grammar .wlt files, and writes
out lines of the form

Wordtype  Word   Probability   Std-deviation

usage: %prog [options]"""

import optparse, re, sys
import lx, tb

def readwords(fname, wordrex, wordtype_word_fname_count):
    inf = file(fname, "rU")
    for line in inf:
        if len(line) > 0 and line[0] == '(':
            trees = tb.string_trees(line.strip())
            assert(len(trees) == 1)
            tree = trees[0]
            assert(isinstance(tree, list))
            label = tree[0]
            mo = wordrex.match(label)
            if mo:
                wordtype = mo.group(1)
                wordcount = int(mo.group(2))
                word = ''.join(tb.terminals(tree))
                lx.incr3(wordtype_word_fname_count, wordtype, word, fname, wordcount)

def writestats(wordtype_word_fname_counti, nfiles):
    wordtypes = wordtype_word_fname_count.keys()
    wordtypes.sort()
    for wordtype in wordtypes:
        word_fname_count = wordtype_word_fname_count[wordtype]
        words = word_fname_count.keys()
        words.sort()
        pws = []
        for word in words:
            counts = word_fname_count[word].values()
            p = sum(counts)/(nfiles+1e-100)
            pws.append((p,word))
        pws.sort(reverse=True)
        for prob,word in pws:
            print wordtype, prob, word

if __name__ == "__main__":
    parser = optparse.OptionParser(usage=usage)

    (options,args) = parser.parse_args()
    
    wordtype_word_fname_count = {}
    wordrex = re.compile("^(Word[-_a-zA-Z0-9]*)#([0-9]+)$")

    for fname in args:
        readwords(fname, wordrex, wordtype_word_fname_count)

    writestats(wordtype_word_fname_count, len(args))
