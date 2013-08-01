#! /usr/bin/env python

import optparse, sys

def filenameline(infn, lineno=-1, outf=sys.stdout):
    lines = file(infn, "rU").read().strip().split('\n')
    outf.write('%s %s\n'%(lines[lineno], infn))
               
if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option("-l", "--lineno", dest="lineno",
                      help="line to read from files", type='int', default=-1)
    (options, args) = parser.parse_args()
    for infn in sorted(args):
        filenameline(infn, lineno=options.lineno)
