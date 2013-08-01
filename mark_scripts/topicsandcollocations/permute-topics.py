#! /usr/bin/env python

usage = """%prog Version of 4th March 2010

(c) Mark Johnson

Randomly permuts the topics on the fm_corpus_tier.adp

usage: %prog [options]"""

import optparse, random, re, sys
import lx


def read_data(inf):
    return [line.strip().split() for line in inf]

if __name__ == "__main__":
    parser = optparse.OptionParser(usage=usage)
    parser.add_option("-s", "--seed", dest="seed",
                      help="seed for random number generator")
    (options,args) = parser.parse_args()

    if options.seed:
        random.seed(options.seed)
    else:
        random.seed(2121)

    if len(args) == 0:
        data = read_data(sys.stdin)
    elif len(args) == 1:
        data = read_data(file(args[0], "rU"))
    else:
        sys.stderr.write("## Error -- too many command line arguments: %s\n"%args)
        exit()

    topics = [line[0] for line in data]
    random.shuffle(topics)
    for topic,line in zip(topics,data):
        print topic, ' '.join(line[1:])

    
