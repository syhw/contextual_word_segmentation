#! /usr/bin/env python

usage = """%prog Version of 2nd September 2008

(c) Mark Johnson

usage: %prog [options]"""

import optparse, re, sys

def filename_key(filename, key_re, key_subst, keys_sofar):
    if key_re and key_subst:
        mo = key_re.match(filename)
        if mo:
            key = mo.expand(key_subst)
        else:
            key = filename
    else:
        key = filename
    if key in keys_sofar:
        return "notitle with lines linetype %s"%keys_sofar[key]
    else:
        keys_sofar[key] = len(keys_sofar)+1
        return 'title "%s" with lines linetype %s'%(key,keys_sofar[key])


if __name__ == '__main__':
    parser = optparse.OptionParser(usage=usage)

    parser.add_option("-k", "--key_re", dest="key_re", default=r"(.*)_[0-9]+\.([^.]*)",
                      help="regex used to map filenames to plot keys")
    parser.add_option("-s", "--key_subst", dest="key_subst", default=r"\1 \2",
                      help="substitution pattern used to map filenames to plot keys")

    parser.add_option("-x", "--xindex", dest="xindex", help="plot x index")
    parser.add_option("-y", "--yindex", dest="yindex", default=1, help="plot y index")
    parser.add_option("--xlabel", dest="xlabel", help="label for x-axis")
    parser.add_option("--ylabel", dest="ylabel", help="label for y-axis")
    parser.add_option("-X", "--xrange", dest="xrange", help="xrange value")
    parser.add_option("-Y", "--yrange", dest="yrange", help="xrange value")
    parser.add_option("-t", "--title", dest="title", help="plot title")
    parser.add_option("-T", "--term", dest="term", default='x11', help="terminal type")
    parser.add_option("-o", "--output", dest="output", help="gnuplot output file")
    parser.add_option("-S", "--xscale", dest="xscale", default=1, help="scale x values")
    
    (options,args) = parser.parse_args()

    key_re = re.compile(options.key_re)
    key_subst = options.key_subst

    if options.term:
        sys.stdout.write('set term %s\n' % options.term)
    if options.output:
        sys.stdout.write('set output "%s"\n' % options.output)

    if options.title:
        sys.stdout.write('set title "%s"\n' % options.title)
    if options.xlabel:
        sys.stdout.write('set xlabel "%s"\n' % options.xlabel)
    if options.ylabel:
        sys.stdout.write('set ylabel "%s"\n' % options.ylabel)
        
    if options.xrange:
        sys.stdout.write("set xrange [%s]\n" % options.xrange)
    if options.yrange:
        sys.stdout.write("set yrange [%s]\n" % options.yrange)

    sys.stdout.write("set border 3\nset xtics nomirror\nset ytics nomirror\n")
                     
    args.sort()
    keys_sofar = {}

    if options.xindex:
        plotindex = "%s:%s"%(options.xindex,options.yindex)
    else:
        plotindex = "(%s*column(0)):%s"%(options.xscale,options.yindex)

    plotcmd = "plot " + ", \\\n	".join("'%s' using %s %s" %
                                       (fn,plotindex,filename_key(fn,key_re,key_subst,keys_sofar))
                                       for fn in args)
    sys.stdout.write(plotcmd)
    sys.stdout.write("\n\n")

    # sys.stdout.write("pause mouse any\n")
