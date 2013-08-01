#! /bin/env python

description = """
word-count.py version of 20th August, 2011.

Writes to stdout a list of word types and their frequencies.
"""

import argparse, collections, csv, re, sys

def count_words(inf, simplify_rex, simplify_template, word_count):
    for line in inf:
        for word in line.split():
            mo = simplify_rex.match(word)
            if mo:
                word_count[mo.expand(simplify_template)] += 1
            else:
                word_count[word] += 1

def binned_count(count):
    if count > 1000:
        return 1000
    elif count > 500:
        return 500
    elif count > 200:
        return 200
    elif count > 100:
        return 100
    elif count > 50:
        return 50
    elif count > 20:
        return 20
    elif count > 10:
        return 10
    else:
        return None

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument("datafiles", nargs='+',
                        help="read words from these files (default=stdin)")
    parser.add_argument("--bin-counts", default=False, action='store_true',
                        help="output binned counts rather than raw counts")
    parser.add_argument("--output-field-separator", 
                        dest="output_field_separator", default="\t",
                        help="separator between output fields")
    parser.add_argument("--simplify-re", "-s", dest="simplify_re", 
                        default=r"^([^_]*)(?:_.*)?$",
                        help="regex used to simplify tokens during reading")
    parser.add_argument("--simplify-template", "-S", dest="simplify_template", 
                        default=r"\1",
                        help="template used to simplify tokens during reading")

    args = parser.parse_args()
    simplify_rex = re.compile(args.simplify_re)
    simplify_template = args.simplify_template

    word_count = collections.Counter()

    if len(args.datafiles) == 0:
        count_words(sys.stdin, simplify_rex, simplify_template, word_count)
    else:
        for datafile in args.datafiles:
            count_words(file(datafile, "rU"), simplify_rex, simplify_template, word_count)

    os = csv.writer(sys.stdout, 
                    delimiter=args.output_field_separator, 
                    lineterminator='\n')

    # os.writerow(('word','count'))
    if args.bin_counts:
        for word, count in word_count.most_common():
            bc = binned_count(count)
            if bc:
                os.writerow((word,bc))
    else:
        for word, count in word_count.most_common():
            os.writerow((word,count))
