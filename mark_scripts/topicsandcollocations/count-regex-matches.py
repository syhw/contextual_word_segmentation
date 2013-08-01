#! /usr/bin/env python

usage = """%prog

(c) Mark Johnson, 26th October 2010

Counts the number of times an instance of the regular expression <rex>
is found in a set of files (<rex> must match within a single line).  

It writes to standard output a sorted list of the form

<Count> <Instance>

where <Instance> is a substring that matches the regular expression rex
and <Count> is the number of times <Instance> was seen.

The input is read from the file names given on the command line, or
standard input if none are given.

usage: %prog [options] file*"""

import optparse, re, sys

nonblank_rex = re.compile(r"[^ \t\n\r\f\v]")

def count_patterns(inf, pattern_rex, skip_epochs, pattern_count):
    if skip_epochs > 0:
        epoch = 0
        for line in inf:
            if nonblank_rex.search(line):
                epoch += 1
                if epoch >= skip_epochs:
                    break
    for line in inf:            
        for mo in pattern_rex.finditer(line):
            key = mo.group()
            if key in pattern_count:
                pattern_count[key] += 1
            else:
                pattern_count[key] = 1
    return pattern_count

def write_pattern_count(pattern_count, mincount, outf):
    if mincount > 1:
        patterncounts = [pc for pc in pattern_count.iteritems() if pc[1] >= mincount]
    else:
        patterncounts = pattern_count.items()
    patterncounts.sort()
    for pattern, count in patterncounts:
        outf.write(str(count))
        outf.write('\t')
        outf.write(pattern)
        outf.write('\n')

if __name__ == '__main__':
    parser = optparse.OptionParser(usage=usage)

    rp1_re = r"[(][^()]*[)]"
    rp2_re = r"[(](?:[^()]*[(][^()]*[)])+[^()]*[)]"
    rp3_re = r"[(](?:[^()]*"+rp2_re+")+[^()]*[)]"

    parser.add_option("-m", "--min-count", dest="min_count", default=0, type="int",
                      help="ignore pattern instances with a count less than min-count")
    parser.add_option("-r", "--regex", dest="regex", 
                      help="regex to count matches of")
    parser.add_option("--rp1", dest="regex", action="store_const", const=rp1_re,
                      help = "use predefined regex "+rp1_re)
    parser.add_option("--rp2", dest="regex", action="store_const", const=rp2_re,
                      help = "use predefined regex "+rp2_re)
    parser.add_option("--rp3", dest="regex", action="store_const", const=rp3_re,
                      help = "use predefined regex "+rp3_re)

    parser.add_option("-n", "--nepochs", type="int", dest="nepochs", default=0, 
                      help="total number of epochs (epochs segmented by blank lines) (0=ignore epochs)")
    parser.add_option("-s", "--skip-epochs", type="float", dest="skip_epochs", default=0, 
                      help="initial fraction of epochs to skip")
    parser.add_option("-e", "--epoch-rate", type="int", dest="epoch_rate", default=1, 
                      help="input provides samples every rate epochs")


    (options,args) = parser.parse_args()    

    assert(options.regex)
    regex_rex = re.compile(options.regex)

    skip_epochs = int(options.nepochs*options.skip_epochs/options.epoch_rate)

    pattern_count = {}
    if len(args) > 0:
        for arg in args:
            count_patterns(file(arg, "rU"), regex_rex, skip_epochs, pattern_count)
    else:
        count_patterns(sys.stdin, regex_rex, skip_epochs, pattern_count)

    write_pattern_count(pattern_count, options.min_count, sys.stdout)

            
