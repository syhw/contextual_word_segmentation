#! /usr/bin/env python

usage = """%prog Version of 26th May 2010

(c) Mark Johnson

Extracts a grammar from a CHILDES file

usage: %prog [options]"""

import optparse, re, sys
import lx, tb

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

def write_gold(records, phon_topic, outf):
    for record in records:
        pho = record['pho'].split()
        intent = record.get('int', None)
        line = ' '.join((p if p not in phon_topic or phon_topic[p] != intent else "%s_%s"%(p,phon_topic[p]) for p in pho))
        outf.write("%s\n"%line)

def write_train(records, outf):
    for record in records:
        pho = record['pho']
        pho = ' '.join(pho.replace(' ', ''))
        ref = record.get('ref')
        if ref:
            refs = list(set(ref.split()))
            refs.sort()
            ref = 'T_'+'|'.join(refs)
        else:
            ref = 'T_None'
        outf.write("%s\t%s\n"%(ref, pho))
        
if __name__ == "__main__":
    parser = optparse.OptionParser(usage=usage)
    parser.add_option("-c", "--childes-data", dest="childes_data",
                      help="input file containing CHILDES data")
    parser.add_option("-p", "--phon-topic", dest="phon_topic",
                      help="input file containing phon->topic mapping")
    parser.add_option("-g", "--gold", dest="gold",
                      help="output file containing gold training data")
    parser.add_option("-t", "--train", dest="train",
                      help="output file containing training data")
    (options,args) = parser.parse_args()
    
    assert(len(args) == 0)
    assert(options.childes_data != None)
    childes = list(read_childes(file(options.childes_data, "rU")))
    
    phon_topic = {}
    if options.phon_topic:
        for line in file(options.phon_topic, "rU"):
            ws = line.split()
            assert(len(ws) == 2)
            phon_topic[ws[0]] = ws[1]
    
    if options.gold:
        write_gold(childes, phon_topic, file(options.gold, "w"))

    if options.train:
        write_train(childes, file(options.train, "w"))

    
