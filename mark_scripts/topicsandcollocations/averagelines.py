#! /usr/bin/env python

usage = """%prog Version of 27th May 2010

(c) Mark Johnson

usage: %prog [options]"""

import optparse, re, sys

        
def average(xs):
    return sum(xs)/len(xs)

def transpose(matrix):
    return map(None, *matrix)

def filename_key(filename, key_re, key_subst):
    if key_re and key_subst:
        mo = key_re.match(filename)
        if mo:
            key = mo.expand(key_subst)
        else:
            key = filename
    else:
        key = filename
    return key

if __name__ == '__main__':
    parser = optparse.OptionParser(usage=usage)
    parser.add_option("-i", "--ignore_re", dest="ignore_re", default=r"^[#]",
                      help="ignore lines that match this regex")
    parser.add_option("-l", "--lineno", dest="lineno", type='int', default=-10,
                      help="line no to start reading from files (negative => count from end)")
    parser.add_option("-n", "--nlines", dest="nlines", type='int', default=0,
                      help="number of lines to read from files (0 = all lines)")
    parser.add_option("-k", "--key_re", dest="key_re", default=r"(.*)_[0-9]+\.([^.]*)",
                      help="regex used to collapse filenames")
    parser.add_option("-s", "--key_subst", dest="key_subst", default=r"\1 \2",
                      help="substitution pattern used to generate collapsed filenames")
    (options, args) = parser.parse_args()
    outf = sys.stdout
    ignore_re = re.compile(options.ignore_re)
    key_re = re.compile(options.key_re)
    key_subst = options.key_subst
    lineno = options.lineno
    nlines = options.nlines
    if nlines == 0:
        nlines = None
    key_lines = {}
    for infn in args:
        # lines = file(infn, "rU").read().strip().split('\n')[lineno:nlines]
        lines = [line for line in file(infn, "rU") if not ignore_re.search(line)][lineno:nlines]
        key = filename_key(infn, key_re, key_subst)
        if key in key_lines:
            key_lines[key].append(lines)
        else:
            key_lines[key] = [lines]
    keys = key_lines.keys()
    keys.sort()
    for key in keys:
        lines0 = key_lines[key]
        lines = (line for ls in lines0 for line in ls)
        vm = ((float(v) for v in line.strip().split()) for line in lines)
        tvm = transpose(vm)
        for vs in tvm:
            outf.write('%s '%average(vs))
        outf.write('%s %s\n'%(key,len(lines0)))
