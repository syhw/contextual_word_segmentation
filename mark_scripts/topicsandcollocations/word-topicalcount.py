#! /bin/env python

description = """
word-topicalcount.py version of 20th August, 2011

Produces a file mapping words to binnedcount-topic labels
"""

import argparse, collections, csv, re, sys

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--output-field-separator", 
                        dest="output_field_separator", default="\t",
                        help="separator between output fields")
    parser.add_argument("--word-counts", 
                        default="fm_corpus_tier_gold.wbc.txt",
                        help="file to read word count pairs from")
    parser.add_argument("--word-topics",
                        default="phon-topic.txt",
                        help="file to read word topic pairs from")
    args = parser.parse_args()

    word_counts = dict(line.split() for line in file(args.word_counts, "rU"))
    word_topics = dict(line.split() for line in file(args.word_topics, "rU"))

    os = csv.writer(sys.stdout, 
                    delimiter=args.output_field_separator, 
                    lineterminator='\n')

    for word, count in word_counts.iteritems():
        if word in word_topics:
            os.writerow((word,'Topical_'+count))
        else:
            os.writerow((word,'Nontopical_'+count))



    
