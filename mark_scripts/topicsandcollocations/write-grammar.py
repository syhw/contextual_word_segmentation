#! /usr/bin/env python

usage = """%prog Version of 6th September, 2011

(c) Mark Johnson

Usage: %prog [options]"""

import optparse, re, sys
import lx

consonants = "bcdDfghGklmnNprsStTvwyzZ4"
vowels = "a&AOQ69EeIio7UuR2"
syllabicconsonants = "mnNS"

def read_data(inf, max_nlines=0):
    prefixes = set()
    topics = set()
    segs = set()
    nlines = 0
    for line in inf:
        line = line.strip().split()
        prefix = line[0]
        assert(prefix[:2] == "T_")
        prefix = prefix[2:]
        segments = line[1:]
        prefixes.add(prefix)
        for topic in prefix.split('|'):
            topics.add(topic)
        segs.update(segments)
        nlines += 1
        if nlines == max_nlines:
            break
    return (prefixes,topics,segs)

def bevanunigramtopic(outf, (prefixes,topics,segments)):
    for topic in topics:
        outf.write("1 1 Sentence --> Topic_%s\n"%topic)
        outf.write("1 1 Topic_%s --> Topic_%s Word\n"%(topic,topic))
        for prefix in prefixes:
            if topic in prefix.split('|'):
                outf.write("1 1 Topic_%s --> T_%s\n"%(topic,prefix))
        if topic == 'None':
            outf.write("1 1 Topic_None --> T_None\n")
        else:
            outf.write("1 1 Topic_%s --> Topic_%s Word_%s\n"%(topic,topic,topic))
            outf.write("1 0 0.01 Word_%s --> Segments\n"%topic)
    outf.write("1 0 20 Word --> Segments\n")
    outf.write("1 1 Segments --> Segment\n")
    outf.write("1 1 Segments --> Segments Segment\n")
    for segment in segments:
        outf.write("1e9 1 Segment --> %s\n"%segment)

def Tunigram(outf, (prefixes,topics,segments)):
    """topic-based unigram model, like bevanunigramtopic but
    estimates all adaptor parameters (rather than fixing them)"""
    for topic in topics:
        outf.write("1 1 Sentence --> Topic_%s\n"%topic)
        outf.write("1 1 Topic_%s --> Topic_%s Word\n"%(topic,topic))
        for prefix in prefixes:
            if topic in prefix.split('|'):
                outf.write("1 1 Topic_%s --> T_%s\n"%(topic,prefix))
        if topic == 'None':
            outf.write("1 1 Topic_None --> T_None\n")
        else:
            outf.write("1 1 Topic_%s --> Topic_%s Word_%s\n"%(topic,topic,topic))
            outf.write("Word_%s --> Segments\n"%topic)
    outf.write("Word --> Segments\n")
    outf.write("1 1 Segments --> Segment\n")
    outf.write("1 1 Segments --> Segments Segment\n")
    for segment in segments:
        outf.write("1 1 Segment --> %s\n"%segment)

def HTunigram(outf, (prefixes,topics,segments)):
    """hierarchical topic-based unigram model based on TUnigram
    (all words share a common base Word distribution)"""
    for topic in topics:
        outf.write("1 1 Sentence --> Topic_%s\n"%topic)
        outf.write("1 1 Topic_%s --> Topic_%s Word\n"%(topic,topic))
        for prefix in prefixes:
            if topic in prefix.split('|'):
                outf.write("1 1 Topic_%s --> T_%s\n"%(topic,prefix))
        if topic == 'None':
            outf.write("1 1 Topic_None --> T_None\n")
        else:
            outf.write("1 1 Topic_%s --> Topic_%s Word_%s\n"%(topic,topic,topic))
            outf.write("Word_%s --> BaseWord\n"%topic)
    outf.write("Word --> BaseWord\n")
    outf.write("BaseWord --> Segments\n")
    outf.write("1 1 Segments --> Segment\n")
    outf.write("1 1 Segments --> Segments Segment\n")
    for segment in segments:
        outf.write("1 1 Segment --> %s\n"%segment)

def TunigramX1(outf, (prefixes,topics,segments)):
    """topic-based unigram model that requires at most one occurence
    of a topic word per sentence"""
    outf.write("1 1 Sentence --> Words\n")
    outf.write("1 1 Words --> Words Word\n")
    for prefix in prefixes:
        outf.write("1 1 Words --> T_%s\n"%prefix)
    for topic in topics:
        if topic != "None":
            outf.write("1 1 Words --> Topic_%s Word_%s\n"%(topic,topic))
            outf.write("1 1 Topic_%s --> Topic_%s Word\n"%(topic,topic))
            outf.write("Word_%s --> Segments\n"%topic)
            for prefix in prefixes:
                if topic in prefix.split('|'):
                    outf.write("1 1 Topic_%s --> T_%s\n"%(topic,prefix))
    outf.write("Word --> Segments\n")
    outf.write("1 1 Segments --> Segment\n")
    outf.write("1 1 Segments --> Segments Segment\n")
    for segment in segments:
        outf.write("1 1 Segment --> %s\n"%segment)

def HTunigramX1(outf, (prefixes,topics,segments)):
    """hierarchical topic-based unigram model that requires at most one occurence
    of a topic word per sentence (all words share a common base Word distribution)"""
    outf.write("1 1 Sentence --> Words\n")
    outf.write("1 1 Words --> Words Word\n")
    for prefix in prefixes:
        outf.write("1 1 Words --> T_%s\n"%prefix)
    for topic in topics:
        if topic != "None":
            outf.write("1 1 Words --> Topic_%s Word_%s\n"%(topic,topic))
            outf.write("1 1 Topic_%s --> Topic_%s Word\n"%(topic,topic))
            outf.write("Word_%s --> BaseWord\n"%topic)
            for prefix in prefixes:
                if topic in prefix.split('|'):
                    outf.write("1 1 Topic_%s --> T_%s\n"%(topic,prefix))
    outf.write("Word --> BaseWord\n")
    outf.write("BaseWord --> Segments\n")
    outf.write("1 1 Segments --> Segment\n")
    outf.write("1 1 Segments --> Segments Segment\n")
    for segment in segments:
        outf.write("1 1 Segment --> %s\n"%segment)

def unigram(outf, (prefixes,topics,segments)):
    """this is the regular colloc grammar.
    it ignores topics."""
    outf.write("1 1 Words --> Words Word\n")
    for prefix in prefixes:
        outf.write("1 1 Words --> T_%s\n"%prefix)
    outf.write("Word --> Segments\n")
    outf.write("1 1 Segments --> Segment\n")
    outf.write("1 1 Segments --> Segments Segment\n")
    for segment in segments:
        outf.write("1 1 Segment --> %s\n"%segment)

def Hunigram(outf, (prefixes,topics,segments)):
    """this is the regular colloc grammar.
    it ignores topics.
    Hunigram generates words through 2 levels of hierarchy (as a control for HT models)"""
    outf.write("1 1 Words --> Words Word\n")
    for prefix in prefixes:
        outf.write("1 1 Words --> T_%s\n"%prefix)
    outf.write("Word --> BaseWord\n")
    outf.write("BaseWord --> Segments\n")
    outf.write("1 1 Segments --> Segment\n")
    outf.write("1 1 Segments --> Segments Segment\n")
    for segment in segments:
        outf.write("1 1 Segment --> %s\n"%segment)

def colloc(outf, (prefixes,topics,segments)):
    """this is the regular colloc grammar
    it ignores topics"""
    outf.write("1 1 Collocs --> Collocs Colloc\n")
    for prefix in prefixes:
        outf.write("1 1 Collocs --> T_%s\n"%prefix)
    outf.write("Colloc --> Words\n")
    outf.write("1 1 Words --> Word\n")
    outf.write("1 1 Words --> Words Word\n")
    outf.write("Word --> Segments\n")
    outf.write("1 1 Segments --> Segment\n")
    outf.write("1 1 Segments --> Segments Segment\n")
    for segment in segments:
        outf.write("1 1 Segment --> %s\n"%segment)

def colloc2(outf, (prefixes,topics,segments)):
    """this is the regular colloc grammar
    it ignores topics"""
    outf.write("1 1 Colloc2s --> Colloc2s Colloc2\n")
    for prefix in prefixes:
        outf.write("1 1 Colloc2s --> T_%s\n"%prefix)
    outf.write("Colloc2 --> Collocs\n")
    outf.write("1 1 Collocs --> Colloc\n")
    outf.write("1 1 Collocs --> Collocs Colloc\n")
    outf.write("Colloc --> Words\n")
    outf.write("1 1 Words --> Word\n")
    outf.write("1 1 Words --> Words Word\n")
    outf.write("Word --> Segments\n")
    outf.write("1 1 Segments --> Segment\n")
    outf.write("1 1 Segments --> Segments Segment\n")
    for segment in segments:
        outf.write("1 1 Segment --> %s\n"%segment)

def Hcolloc(outf, (prefixes,topics,segments)):
    """this is the regular colloc grammar.
    it ignores topics.
    It generates words via two levels of hierarchy (as a control for the HT models)."""
    outf.write("1 1 Collocs --> Collocs Colloc\n")
    for prefix in prefixes:
        outf.write("1 1 Collocs --> T_%s\n"%prefix)
    outf.write("Colloc --> Words\n")
    outf.write("1 1 Words --> Word\n")
    outf.write("1 1 Words --> Words Word\n")
    outf.write("Word --> BaseWord\n")
    outf.write("BaseWord --> Segments\n")
    outf.write("1 1 Segments --> Segment\n")
    outf.write("1 1 Segments --> Segments Segment\n")
    for segment in segments:
        outf.write("1 1 Segment --> %s\n"%segment)

def Hcolloc2(outf, (prefixes,topics,segments)):
    """this is the regular colloc grammar.
    it ignores topics.
    It generates words via two levels of hierarchy (as a control for the HT models)."""
    outf.write("1 1 Colloc2s --> Colloc2s Colloc2\n")
    for prefix in prefixes:
        outf.write("1 1 Colloc2s --> T_%s\n"%prefix)
    outf.write("Colloc2 --> Collocs\n")
    outf.write("1 1 Collocs --> Collocs Colloc\n")
    outf.write("1 1 Collocs --> Colloc\n")
    outf.write("Colloc --> Words\n")
    outf.write("1 1 Words --> Word\n")
    outf.write("1 1 Words --> Words Word\n")
    outf.write("Word --> BaseWord\n")
    outf.write("BaseWord --> Segments\n")
    outf.write("1 1 Segments --> Segment\n")
    outf.write("1 1 Segments --> Segments Segment\n")
    for segment in segments:
        outf.write("1 1 Segment --> %s\n"%segment)

def Hcolloc3(outf, (prefixes,topics,segments)):
    """this is the regular colloc grammar.
    it ignores topics.
    It generates words via two levels of hierarchy (as a control for the HT models)."""
    outf.write("1 1 Colloc3s --> Colloc3s Colloc3\n")
    for prefix in prefixes:
        outf.write("1 1 Colloc3s --> T_%s\n"%prefix)
    outf.write("Colloc3 --> Colloc2s\n")
    outf.write("1 1 Colloc2s --> Colloc2s Colloc2\n")
    outf.write("1 1 Colloc2s --> Colloc2\n")
    outf.write("Colloc2 --> Collocs\n")
    outf.write("1 1 Collocs --> Collocs Colloc\n")
    outf.write("1 1 Collocs --> Colloc\n")
    outf.write("Colloc --> Words\n")
    outf.write("1 1 Words --> Word\n")
    outf.write("1 1 Words --> Words Word\n")
    outf.write("Word --> BaseWord\n")
    outf.write("BaseWord --> Segments\n")
    outf.write("1 1 Segments --> Segment\n")
    outf.write("1 1 Segments --> Segments Segment\n")
    for segment in segments:
        outf.write("1 1 Segment --> %s\n"%segment)


def Tcolloc(outf, (prefixes,topics,segments)):
    """non-linguistic context topics
    topics can generate any number of topical collocations
    topical collocations don't actually need to contain topical words"""
    for topic in topics:
        outf.write("1 1 Sentence --> Topic_%s\n"%topic)
        outf.write("1 1 Topic_%s --> Topic_%s Colloc\n"%(topic,topic))
        for prefix in prefixes:
            if topic in prefix.split('|'):
                outf.write("1 1 Topic_%s --> T_%s\n"%(topic,prefix))
        if topic == 'None':
            outf.write("1 1 Topic_None --> T_None\n")
        else:
            outf.write("1 1 Topic_%s --> Topic_%s Colloc_%s\n"%(topic,topic,topic))
            outf.write("Colloc_%s --> Words_%s\n"%(topic,topic))
            outf.write("1 1 Words_%s --> Word\n"%(topic))
            outf.write("1 1 Words_%s --> Word_%s\n"%(topic,topic))
            outf.write("1 1 Words_%s --> Words_%s Word\n"%(topic,topic))
            outf.write("1 1 Words_%s --> Words_%s Word_%s\n"%(topic,topic,topic))
            outf.write("Word_%s --> Segments\n"%topic)
    outf.write("Colloc --> Words\n")
    outf.write("1 1 Words --> Word\n")
    outf.write("1 1 Words --> Words Word\n")
    outf.write("Word --> Segments\n")
    outf.write("1 1 Segments --> Segment\n")
    outf.write("1 1 Segments --> Segments Segment\n")
    for segment in segments:
        outf.write("1 1 Segment --> %s\n"%segment)


def HTcolloc(outf, (prefixes,topics,segments)):
    """non-linguistic context topics
    topics can generate any number of topical collocations
    topical collocations don't actually need to contain topical words.
    All words are generated from a common base Word distribution"""
    for topic in topics:
        outf.write("1 1 Sentence --> Topic_%s\n"%topic)
        outf.write("1 1 Topic_%s --> Topic_%s Colloc\n"%(topic,topic))
        for prefix in prefixes:
            if topic in prefix.split('|'):
                outf.write("1 1 Topic_%s --> T_%s\n"%(topic,prefix))
        if topic == 'None':
            outf.write("1 1 Topic_None --> T_None\n")
        else:
            outf.write("1 1 Topic_%s --> Topic_%s Colloc_%s\n"%(topic,topic,topic))
            outf.write("Colloc_%s --> Words_%s\n"%(topic,topic))
            outf.write("1 1 Words_%s --> Word\n"%(topic))
            outf.write("1 1 Words_%s --> Word_%s\n"%(topic,topic))
            outf.write("1 1 Words_%s --> Words_%s Word\n"%(topic,topic))
            outf.write("1 1 Words_%s --> Words_%s Word_%s\n"%(topic,topic,topic))
            outf.write("Word_%s --> BaseWord\n"%topic)
    outf.write("Colloc --> Words\n")
    outf.write("1 1 Words --> Word\n")
    outf.write("1 1 Words --> Words Word\n")
    outf.write("Word --> BaseWord\n")
    outf.write("BaseWord --> Segments\n")
    outf.write("1 1 Segments --> Segment\n")
    outf.write("1 1 Segments --> Segments Segment\n")
    for segment in segments:
        outf.write("1 1 Segment --> %s\n"%segment)


def Tcolloc1(outf, (prefixes,topics,segments), uniformTopics=False):
    """non-linguistic context topics.
    Topics can generate any number of topical collocations.
    Topical collocations contain exactly one topical word.

    If uniformTopics is not false, set Dirichlet priors on topic
    rules to ensure that all topics are equi-probable."""
    if uniformTopics:
        topic_count = dict()
        for prefix in prefixes:
            for topic in prefix.split('|'):
                lx.incr(topic_count, topic)
        max_topiccount = max(topic_count.itervalues())
    for topic in topics:
        outf.write("1 1 Sentence --> Topic_%s\n"%topic)
        outf.write("1 1 Topic_%s --> Topic_%s Colloc\n"%(topic,topic))
        if topic == 'None':
            outf.write("1 1 Topic_None --> T_None\n")
        else:
            if uniformTopics:
                outf.write("1 1 Topic_%s --> TT_%s\n"%(topic,topic))
                for prefix in prefixes:
                    if topic in prefix.split('|'):
                        outf.write("1e7 1 TT_%s --> T_%s\n"%(topic,prefix))
                excesscount = max_topiccount - topic_count[topic]
                if excesscount > 0:
                    outf.write("%se7 1 TT_%s --> T_IgnoreMe\n"%(excesscount,topic))
            else: # non-uniform topics
                for prefix in prefixes:
                    if topic in prefix.split('|'):
                        outf.write("1 1 Topic_%s --> T_%s\n"%(topic,prefix))
            outf.write("1 1 Topic_%s --> Topic_%s Colloc_%s\n"%(topic,topic,topic))
            outf.write("Colloc_%s --> Words_%s\n"%(topic,topic))
            outf.write("1 1 Words_%s --> Word_%s\n"%(topic,topic))
            outf.write("1 1 Words_%s --> Words_%s Word\n"%(topic,topic))
            outf.write("1 1 Words_%s --> Words Word_%s\n"%(topic,topic))
            outf.write("Word_%s --> Segments\n"%topic)
    outf.write("Colloc --> Words\n")
    outf.write("1 1 Words --> Word\n")
    outf.write("1 1 Words --> Words Word\n")
    outf.write("Word --> Segments\n")
    outf.write("1 1 Segments --> Segment\n")
    outf.write("1 1 Segments --> Segments Segment\n")
    for segment in segments:
        outf.write("1 1 Segment --> %s\n"%segment)

def Tcolloc1NoLearn(outf, (prefixes,topics,segments)):
    """non-linguistic context topics
    topics can generate any number of topical collocations
    topical collocations contain exactly one topical word"""
    for topic in topics:
        outf.write("1 1 Sentence --> Topic_%s\n"%topic)
        outf.write("1 1 Topic_%s --> Topic_%s Colloc\n"%(topic,topic))
        for prefix in prefixes:
            if topic in prefix.split('|'):
                outf.write("1 1 Topic_%s --> T_%s\n"%(topic,prefix))
        if topic == 'None':
            outf.write("1 1 Topic_None --> T_None\n")
        else:
            outf.write("1 1 Topic_%s --> Topic_%s Colloc_%s\n"%(topic,topic,topic))
            outf.write("Colloc_%s --> Words_%s\n"%(topic,topic))
            outf.write("1e7 1 Words_%s --> Word_%s\n"%(topic,topic))
            outf.write("1e7 1 Words_%s --> Words_%s Word\n"%(topic,topic))
            outf.write("1e7 1 Words_%s --> Words Word_%s\n"%(topic,topic))
            outf.write("Word_%s --> Segments\n"%topic)
    outf.write("Colloc --> Words\n")
    outf.write("1 1 Words --> Word\n")
    outf.write("1 1 Words --> Words Word\n")
    outf.write("Word --> Segments\n")
    outf.write("1 1 Segments --> Segment\n")
    outf.write("1 1 Segments --> Segments Segment\n")
    for segment in segments:
        outf.write("1 1 Segment --> %s\n"%segment)

def Tcolloc1F(outf, (prefixes,topics,segments)):
    """non-linguistic context topics
    topics can generate any number of topical collocations
    topical collocations contain exactly one topical word
    the topical word always appears at the end of the collocation"""
    for topic in topics:
        outf.write("1 1 Sentence --> Topic_%s\n"%topic)
        outf.write("1 1 Topic_%s --> Topic_%s Colloc\n"%(topic,topic))
        for prefix in prefixes:
            if topic in prefix.split('|'):
                outf.write("1 1 Topic_%s --> T_%s\n"%(topic,prefix))
        if topic == 'None':
            outf.write("1 1 Topic_None --> T_None\n")
        else:
            outf.write("1 1 Topic_%s --> Topic_%s Colloc_%s\n"%(topic,topic,topic))
            outf.write("Colloc_%s --> Words_%s\n"%(topic,topic))
            outf.write("1 1 Words_%s --> Word_%s\n"%(topic,topic))
#           outf.write("1 1 Words_%s --> Words_%s Word\n"%(topic,topic))
            outf.write("1 1 Words_%s --> Words Word_%s\n"%(topic,topic))
            outf.write("Word_%s --> Segments\n"%topic)
    outf.write("Colloc --> Words\n")
    outf.write("1 1 Words --> Word\n")
    outf.write("1 1 Words --> Words Word\n")
    outf.write("Word --> Segments\n")
    outf.write("1 1 Segments --> Segment\n")
    outf.write("1 1 Segments --> Segments Segment\n")
    for segment in segments:
        outf.write("1 1 Segment --> %s\n"%segment)

def HTcolloc1(outf, (prefixes,topics,segments)):
    """non-linguistic context topics
    topics can generate any number of topical collocations
    topical collocations contain exactly one topical word.
    All words are generated from a common base Word distribution"""
    for topic in topics:
        outf.write("1 1 Sentence --> Topic_%s\n"%topic)
        outf.write("1 1 Topic_%s --> Topic_%s Colloc\n"%(topic,topic))
        for prefix in prefixes:
            if topic in prefix.split('|'):
                outf.write("1 1 Topic_%s --> T_%s\n"%(topic,prefix))
        if topic == 'None':
            outf.write("1 1 Topic_None --> T_None\n")
        else:
            outf.write("1 1 Topic_%s --> Topic_%s Colloc_%s\n"%(topic,topic,topic))
            outf.write("Colloc_%s --> Words_%s\n"%(topic,topic))
            outf.write("1 1 Words_%s --> Word_%s\n"%(topic,topic))
            outf.write("1 1 Words_%s --> Words_%s Word\n"%(topic,topic))
            outf.write("1 1 Words_%s --> Words Word_%s\n"%(topic,topic))
            outf.write("Word_%s --> BaseWord\n"%topic)
    outf.write("Colloc --> Words\n")
    outf.write("1 1 Words --> Word\n")
    outf.write("1 1 Words --> Words Word\n")
    outf.write("Word --> BaseWord\n")
    outf.write("BaseWord --> Segments\n")
    outf.write("1 1 Segments --> Segment\n")
    outf.write("1 1 Segments --> Segments Segment\n")
    for segment in segments:
        outf.write("1 1 Segment --> %s\n"%segment)

def HTcolloc21S(outf, (prefixes,topics,segments), IFflag=False):
    """non-linguistic context topics
    topics can generate any number of topical collocations
    topical collocations2 contain exactly one topical collocation
    a topical collocation contains exactly one topical word"""
    for topic in topics:
        outf.write("1 1 Sentence --> Topic_%s\n"%topic)
        outf.write("1 1 Topic_%s --> Topic_%s Colloc2\n"%(topic,topic))
        for prefix in prefixes:
            if topic in prefix.split('|'):
                outf.write("1 1 Topic_%s --> T_%s\n"%(topic,prefix))
        if topic == 'None' and topic not in prefixes:
            outf.write("1 1 Topic_None --> T_None\n")
        else:
            outf.write("1 1 Topic_%s --> Topic_%s Colloc2_%s\n"%(topic,topic,topic))
            outf.write("Colloc2_%s --> Collocs_%s\n"%(topic,topic))
            outf.write("1 1 Collocs_%s --> Colloc_%s\n"%(topic,topic))
            outf.write("1 1 Collocs_%s --> Collocs_%s Colloc\n"%(topic,topic))
            outf.write("1 1 Collocs_%s --> Collocs Colloc_%s\n"%(topic,topic))
            outf.write("Colloc_%s --> Words_%s\n"%(topic,topic))
            outf.write("1 1 Words_%s --> Word_%s\n"%(topic,topic))
            outf.write("1 1 Words_%s --> Words_%s Word\n"%(topic,topic))
            outf.write("1 1 Words_%s --> Words Word_%s\n"%(topic,topic))
            outf.write("Word_%s --> BaseWord\n"%(topic))
    outf.write("Colloc2 --> Collocs\n")
    outf.write("1 1 Collocs --> Colloc\n")
    outf.write("1 1 Collocs --> Collocs Colloc\n")
    outf.write("Colloc --> Words\n")
    outf.write("1 1 Words --> Word\n")
    outf.write("1 1 Words --> Words Word\n")
    outf.write("Word --> BaseWord\n")
    WordSyllables(outf, ['BaseWord'], segments, IFflag=IFflag)

def TcollocX1(outf, (prefixes,topics,segments)):
    """non-linguistic context topics
    topics can generate exactly one topical collocation
    topical collocations contain exactly one topical word"""
    outf.write("1 1 Collocs --> Collocs Colloc\n")
    for topic in topics:
        if topic != "None":
            outf.write("1 1 Collocs --> Topic_%s Colloc_%s\n"%(topic,topic))
    for prefix in prefixes:
        outf.write("1 1 Collocs --> T_%s\n"%prefix)
    outf.write("Colloc --> Words\n")
    outf.write("1 1 Words --> Words Word\n")
    outf.write("1 1 Words --> Word\n")
    outf.write("Word --> Segments\n")
    outf.write("1 1 Segments --> Segment\n")
    outf.write("1 1 Segments --> Segments Segment\n")
    for segment in segments:
        outf.write("1 1 Segment --> %s\n"%segment)
    for topic in topics:
        if topic != "None":
            outf.write("1 1 Topic_%s --> Topic_%s Colloc\n"%(topic,topic))
            for prefix in prefixes:
                if topic in prefix.split('|'):
                    outf.write("1 1 Topic_%s --> T_%s\n"%(topic,prefix))
    for topic in topics:
        if topic != "None":
            outf.write("Colloc_%s --> Words_%s\n"%(topic,topic))
            outf.write("1 1 Words_%s --> Word_%s\n"%(topic,topic))
            outf.write("1 1 Words_%s --> Words Word_%s\n"%(topic,topic))
            outf.write("1 1 Words_%s --> Words_%s Word\n"%(topic,topic))
            outf.write("Word_%s --> Segments\n"%(topic))

def HTcollocX1(outf, (prefixes,topics,segments)):
    """non-linguistic context topics
    topics can generate exactly one topical collocation
    topical collocations contain exactly one topical word.
    All words are generated from a common base Word distribution"""
    outf.write("1 1 Collocs --> Collocs Colloc\n")
    for topic in topics:
        if topic != "None":
            outf.write("1 1 Collocs --> Topic_%s Colloc_%s\n"%(topic,topic))
    for prefix in prefixes:
        outf.write("1 1 Collocs --> T_%s\n"%prefix)
    outf.write("Colloc --> Words\n")
    outf.write("1 1 Words --> Words Word\n")
    outf.write("1 1 Words --> Word\n")
    outf.write("Word --> BaseWord\n")
    outf.write("BaseWord --> Segments\n")
    outf.write("1 1 Segments --> Segment\n")
    outf.write("1 1 Segments --> Segments Segment\n")
    for segment in segments:
        outf.write("1 1 Segment --> %s\n"%segment)
    for topic in topics:
        if topic != "None":
            outf.write("1 1 Topic_%s --> Topic_%s Colloc\n"%(topic,topic))
            for prefix in prefixes:
                if topic in prefix.split('|'):
                    outf.write("1 1 Topic_%s --> T_%s\n"%(topic,prefix))
    for topic in topics:
        if topic != "None":
            outf.write("Colloc_%s --> Words_%s\n"%(topic,topic))
            outf.write("1 1 Words_%s --> Word_%s\n"%(topic,topic))
            outf.write("1 1 Words_%s --> Words Word_%s\n"%(topic,topic))
            outf.write("1 1 Words_%s --> Words_%s Word\n"%(topic,topic))
            outf.write("Word_%s --> BaseWord\n"%(topic))


def CVs(outf, segments):
    """writes out a grammar defining Consonants, Vowels and SyllabicConsonants"""
    outf.write("1 1 Consonants --> Consonant\n")
    outf.write("1 1 Consonants --> Consonants Consonant\n")
    outf.write("1 1 Vowels --> Vowel\n")
    outf.write("1 1 Vowels --> Vowels Vowel\n")
    outf.write("1 1 SyllabicConsonants --> SyllabicConsonant\n")
    outf.write("1 1 SyllabicConsonants --> SyllabicConsonants SyllabicConsonant\n")
    for segment in segments:
        if segment in consonants:
            outf.write("1 1 Consonant --> %s\n"%segment)
        elif segment in vowels:
            outf.write("1 1 Vowel --> %s\n"%segment)
        else:
            sys.stderr.write("## Error in write-grammar.py: segment %s is not in list of consonants or vowels\n"%segment)
            sys.exit(1)
        if segment in syllabicconsonants:
            outf.write("1 1 SyllabicConsonant --> %s\n"%segment)

def WordSyllables(outf, words, segments, IFflag=False, Adaptflag=True):
    """writes out a grammar defining Word* in terms of Syllables.  words should be a sequence of Word symbols"""
    if IFflag=='Segments':
        for word in words:
            if Adaptflag:
                ruleprefix = word
            else:
                ruleprefix = "1 1 "+word
            outf.write("%s --> Segments\n"%ruleprefix)
        outf.write("1 1 Segments --> Segment\n")
        outf.write("1 1 Segments --> Segment Segments\n")
        for segment in segments:
            outf.write("1 1 Segment --> %s\n"%segment)
        return
    for word in words:
        if Adaptflag:
            ruleprefix = word
        else:
            ruleprefix = "1 1 "+word
        if IFflag:
            outf.write("%s --> SyllableIF\n"%ruleprefix)
            outf.write("%s --> SyllableI SyllableF\n"%ruleprefix)
            outf.write("%s --> SyllableI Syllable SyllableF\n"%ruleprefix)
            outf.write("%s --> SyllableI Syllable Syllable SyllableF\n"%ruleprefix)
        else:
            outf.write("%s --> Syllable\n"%ruleprefix)
            outf.write("%s --> Syllable Syllable\n"%ruleprefix)
            outf.write("%s --> Syllable Syllable Syllable\n"%ruleprefix)
            outf.write("%s --> Syllable Syllable Syllable Syllable\n"%ruleprefix)
    outf.write("1 1 Syllable --> Onset Rhyme\n")
    outf.write("1 1 Syllable --> Rhyme\n")
    outf.write("1 1 Rhyme --> Nucleus Coda\n")
    outf.write("1 1 Rhyme --> Nucleus\n")
    outf.write("Onset --> Consonants\n")
    outf.write("Nucleus --> Vowels\n")
    outf.write("Nucleus --> SyllabicConsonants\n")
    outf.write("Coda --> Consonants\n")
    if IFflag:
        outf.write("1 1 SyllableIF --> OnsetI RhymeF\n")
        outf.write("1 1 SyllableIF --> RhymeF\n")
        outf.write("1 1 SyllableI --> OnsetI Rhyme\n")
        outf.write("1 1 SyllableI --> Rhyme\n")
        outf.write("1 1 SyllableF --> Onset RhymeF\n")
        outf.write("1 1 SyllableF --> RhymeF\n")
        outf.write("OnsetI --> Consonants\n")
        outf.write("1 1 RhymeF --> Nucleus CodaF\n")
        outf.write("1 1 RhymeF --> Nucleus\n")
        outf.write("1 1 CodaF --> Consonants\n")
    CVs(outf, segments)


def collocS(outf, (prefixes,topics,segments), IFflag=False):
    """this is the regular colloc grammar
    it ignores topics"""
    outf.write("1 1 Collocs --> Collocs Colloc\n")
    for prefix in prefixes:
        outf.write("1 1 Collocs --> T_%s\n"%prefix)
    outf.write("Colloc --> Words\n")
    outf.write("1 1 Words --> Word\n")
    outf.write("1 1 Words --> Words Word\n")
    WordSyllables(outf, ['Word'], segments, IFflag=IFflag)

def colloc2S(outf, (prefixes,topics,segments), IFflag=False):
    """this is the regular colloc grammar
    it ignores topics"""
    outf.write("1 1 Colloc2s --> Colloc2s Colloc2\n")
    for prefix in prefixes:
        outf.write("1 1 Colloc2s --> T_%s\n"%prefix)
    outf.write("Colloc2 --> Collocs\n")
    outf.write("1 1 Collocs --> Colloc\n")
    outf.write("1 1 Collocs --> Collocs Colloc\n")
    outf.write("Colloc --> Words\n")
    outf.write("1 1 Words --> Word\n")
    outf.write("1 1 Words --> Words Word\n")
    WordSyllables(outf, ['Word'], segments, IFflag=IFflag)


def Tcolloc1S(outf, (prefixes,topics,segments), IFflag=False):
    """non-linguistic context topics
    topics can generate any number of topical collocations
    topical collocations contain exactly one topical word"""
    for topic in topics:
        outf.write("1 1 Sentence --> Topic_%s\n"%topic)
        outf.write("1 1 Topic_%s --> Topic_%s Colloc\n"%(topic,topic))
        for prefix in prefixes:
            if topic in prefix.split('|'):
                outf.write("1 1 Topic_%s --> T_%s\n"%(topic,prefix))
        if topic == 'None':
            outf.write("1 1 Topic_None --> T_None\n")
        else:
            outf.write("1 1 Topic_%s --> Topic_%s Colloc_%s\n"%(topic,topic,topic))
            outf.write("Colloc_%s --> Words_%s\n"%(topic,topic))
            outf.write("1 1 Words_%s --> Word_%s\n"%(topic,topic))
            outf.write("1 1 Words_%s --> Words_%s Word\n"%(topic,topic))
            outf.write("1 1 Words_%s --> Words Word_%s\n"%(topic,topic))
    outf.write("Colloc --> Words\n")
    outf.write("1 1 Words --> Word\n")
    outf.write("1 1 Words --> Words Word\n")
    WordSyllables(outf, ['Word']+['Word_'+t for t in topics], segments, IFflag=IFflag)


def Tcolloc2S(outf, (prefixes,topics,segments), IFflag=False):
    """non-linguistic context topics
    topics can generate any number of topical collocations
    topical collocations contain any number of topical words"""
    for topic in topics:
        outf.write("1 1 Sentence --> Topic_%s\n"%topic)
        for prefix in prefixes:
            if topic in prefix.split('|'):
                outf.write("1 1 Topic_%s --> T_%s\n"%(topic,prefix))
        outf.write("1 1 Topic_%s --> Topic_%s Colloc2\n"%(topic,topic))
        if topic == 'None':
            outf.write("1 1 Topic_None --> T_None\n")
        else:
            outf.write("1 1 Topic_%s --> Topic_%s Colloc2_%s\n"%(topic,topic,topic))
            outf.write("Colloc2_%s --> Collocs_%s\n"%(topic,topic))
            outf.write("1 1 Collocs_%s --> Colloc_%s\n"%(topic,topic))
            outf.write("1 1 Collocs_%s --> Colloc\n"%(topic,))
            outf.write("1 1 Collocs_%s --> Collocs_%s Colloc\n"%(topic,topic))
            outf.write("1 1 Collocs_%s --> Collocs_%s Colloc_%s\n"%(topic,topic,topic))
            outf.write("Colloc_%s --> Words_%s\n"%(topic,topic))
            outf.write("1 1 Words_%s --> Word_%s\n"%(topic,topic))
            outf.write("1 1 Words_%s --> Word\n"%(topic,))
            outf.write("1 1 Words_%s --> Words_%s Word\n"%(topic,topic))
            outf.write("1 1 Words_%s --> Words_%s Word_%s\n"%(topic,topic,topic))
    outf.write("Colloc2 --> Collocs\n")
    outf.write("1 1 Collocs --> Colloc\n")
    outf.write("1 1 Collocs --> Collocs Colloc\n")
    outf.write("Colloc --> Words\n")
    outf.write("1 1 Words --> Word\n")
    outf.write("1 1 Words --> Words Word\n")
    WordSyllables(outf, ['Word']+['Word_'+t for t in topics], segments, IFflag=IFflag)

def Tcolloc2NS(outf, (prefixes,topics,segments), IFflag=False):
    """non-linguistic context topics
    topics can generate any number of topical collocations
    topical collocations contain exactly one topical word"""
    for topic in topics:
        outf.write("1 1 Sentence --> Topic_%s\n"%topic)
        outf.write("1 1 Topic_%s --> Topic_%s Colloc2\n"%(topic,topic))
        for prefix in prefixes:
            if topic in prefix.split('|'):
                outf.write("1 1 Topic_%s --> T_%s\n"%(topic,prefix))
        if topic == 'None':
            outf.write("1 1 Topic_None --> T_None\n")
        else:
            outf.write("1 1 Topic_%s --> Topic_%s Colloc2_%s\n"%(topic,topic,topic))
            outf.write("Colloc2_%s --> Collocs_%s\n"%(topic,topic))
            outf.write("1 1 Collocs_%s --> Colloc_%s\n"%(topic,topic))
            outf.write("1 1 Collocs_%s --> Collocs_%s Colloc\n"%(topic,topic))
            outf.write("1 1 Collocs_%s --> Collocs_%s Colloc_%s\n"%(topic,topic,topic))
            outf.write("Colloc_%s --> Words_%s\n"%(topic,topic))
            outf.write("1 1 Words_%s --> Word_%s\n"%(topic,topic))
            outf.write("1 1 Words_%s --> Words_%s Word\n"%(topic,topic))
            outf.write("1 1 Words_%s --> Words Word_%s\n"%(topic,topic))
    outf.write("Colloc2 --> Collocs\n")
    outf.write("1 1 Collocs --> Colloc\n")
    outf.write("1 1 Collocs --> Collocs Colloc\n")
    outf.write("Colloc --> Words\n")
    outf.write("1 1 Words --> Word\n")
    outf.write("1 1 Words --> Words Word\n")
    WordSyllables(outf, ['Word']+['Word_'+t for t in topics], segments, IFflag=IFflag)

def Tcolloc21S(outf, (prefixes,topics,segments), IFflag=False):
    """non-linguistic context topics
    topics can generate any number of topical collocations
    topical collocations2 contain exactly one topical collocation
    a topical collocation contains exactly one topical word"""
    for topic in topics:
        outf.write("1 1 Sentence --> Topic_%s\n"%topic)
        outf.write("1 1 Topic_%s --> Topic_%s Colloc2\n"%(topic,topic))
        for prefix in prefixes:
            if topic in prefix.split('|'):
                outf.write("1 1 Topic_%s --> T_%s\n"%(topic,prefix))
        if topic == 'None':
            outf.write("1 1 Topic_None --> T_None\n")
        else:
            outf.write("1 1 Topic_%s --> Topic_%s Colloc2_%s\n"%(topic,topic,topic))
            outf.write("Colloc2_%s --> Collocs_%s\n"%(topic,topic))
            outf.write("1 1 Collocs_%s --> Colloc_%s\n"%(topic,topic))
            outf.write("1 1 Collocs_%s --> Collocs_%s Colloc\n"%(topic,topic))
            outf.write("1 1 Collocs_%s --> Collocs Colloc_%s\n"%(topic,topic))
            outf.write("Colloc_%s --> Words_%s\n"%(topic,topic))
            outf.write("1 1 Words_%s --> Word_%s\n"%(topic,topic))
            outf.write("1 1 Words_%s --> Words_%s Word\n"%(topic,topic))
            outf.write("1 1 Words_%s --> Words Word_%s\n"%(topic,topic))
    outf.write("Colloc2 --> Collocs\n")
    outf.write("1 1 Collocs --> Colloc\n")
    outf.write("1 1 Collocs --> Collocs Colloc\n")
    outf.write("Colloc --> Words\n")
    outf.write("1 1 Words --> Word\n")
    outf.write("1 1 Words --> Words Word\n")
    WordSyllables(outf, ['Word']+['Word_'+t for t in topics], segments, IFflag=IFflag)

def TcollocX1S(outf, (prefixes,topics,segments), IFflag=False):
    """non-linguistic context topics
    topics can generate exactly one topical collocation
    topical collocations contain exactly one topical word"""
    outf.write("1 1 Collocs --> Collocs Colloc\n")
    for topic in topics:
        if topic != "None":
            outf.write("1 1 Collocs --> Topic_%s Colloc_%s\n"%(topic,topic))
    for prefix in prefixes:
        outf.write("1 1 Collocs --> T_%s\n"%prefix)
    outf.write("Colloc --> Words\n")
    outf.write("1 1 Words --> Words Word\n")
    outf.write("1 1 Words --> Word\n")
    for topic in topics:
        if topic != "None":
            outf.write("1 1 Topic_%s --> Topic_%s Colloc\n"%(topic,topic))
            for prefix in prefixes:
                if topic in prefix.split('|'):
                    outf.write("1 1 Topic_%s --> T_%s\n"%(topic,prefix))
    for topic in topics:
        if topic != "None":
            outf.write("Colloc_%s --> Words_%s\n"%(topic,topic))
            outf.write("1 1 Words_%s --> Word_%s\n"%(topic,topic))
            outf.write("1 1 Words_%s --> Words Word_%s\n"%(topic,topic))
            outf.write("1 1 Words_%s --> Words_%s Word\n"%(topic,topic))
    WordSyllables(outf, ['Word']+['Word_'+t for t in topics], segments, IFflag=IFflag)

def Tcolloc2X1S(outf, (prefixes,topics,segments), IFflag=False):
    """non-linguistic context topics
    topics can generate exactly one topical collocation
    topical collocations contain exactly one topical word"""
    outf.write("1 1 Colloc2s --> Colloc2s Colloc2\n")
    for topic in topics:
        if topic != "None":
            outf.write("1 1 Colloc2s --> Topic_%s Colloc2_%s\n"%(topic,topic))
    for prefix in prefixes:
        outf.write("1 1 Colloc2s --> T_%s\n"%prefix)
    outf.write("Colloc2 --> Collocs\n")
    outf.write("1 1 Collocs --> Colloc\n")
    outf.write("1 1 Collocs --> Collocs Colloc\n")
    outf.write("Colloc --> Words\n")
    outf.write("1 1 Words --> Words Word\n")
    outf.write("1 1 Words --> Word\n")
    for topic in topics:
        if topic != "None":
            outf.write("1 1 Topic_%s --> Topic_%s Colloc2\n"%(topic,topic))
            for prefix in prefixes:
                if topic in prefix.split('|'):
                    outf.write("1 1 Topic_%s --> T_%s\n"%(topic,prefix))
    for topic in topics:
        if topic != "None":
            outf.write("Colloc2_%s --> Collocs_%s\n"%(topic,topic))
            outf.write("1 1 Collocs_%s --> Colloc_%s\n"%(topic,topic))
            outf.write("1 1 Collocs_%s --> Collocs Colloc_%s\n"%(topic,topic))
            outf.write("1 1 Collocs_%s --> Collocs_%s Colloc\n"%(topic,topic)) 
            outf.write("Colloc_%s --> Words_%s\n"%(topic,topic))
            outf.write("1 1 Words_%s --> Word_%s\n"%(topic,topic))
            outf.write("1 1 Words_%s --> Words Word_%s\n"%(topic,topic))
            outf.write("1 1 Words_%s --> Words_%s Word\n"%(topic,topic))
    WordSyllables(outf, ['Word']+['Word_'+t for t in topics], segments, IFflag=IFflag)

def fixed(outf, (prefixes,topics,segments)):
    """this grammar generates collocations where there are different
    distributions for words in each position.  Hopefully this will 
    generate something that looks like phrases."""
    outf.write("1 1 Collocs --> Collocs Fixed\n")
    for prefix in prefixes:
        outf.write("1 1 Collocs --> T_%s\n"%prefix)
    outf.write("Fixed --> Word11\n")
    outf.write("Fixed --> Word21 Word22\n")
    outf.write("Fixed --> Word31 Word32 Word33\n")
    outf.write("Word11 --> Segments\n")
    outf.write("Word21 --> Segments\n")
    outf.write("Word22 --> Segments\n")
    outf.write("Word31 --> Segments\n")
    outf.write("Word32 --> Segments\n")
    outf.write("Word33 --> Segments\n")
    outf.write("1 1 Segments --> Segment\n")
    outf.write("1 1 Segments --> Segments Segment\n")
    for segment in segments:
        outf.write("1 1 Segment --> %s\n"%segment)

def Hfixed(outf, (prefixes,topics,segments)):
    """this grammar generates collocations where there are different
    distributions for words in each position.  Hopefully this will 
    generate something that looks like phrases."""
    outf.write("1 1 Collocs --> Collocs Fixed\n")
    for prefix in prefixes:
        outf.write("1 1 Collocs --> T_%s\n"%prefix)
    outf.write("Fixed --> Wrd1_1\n")
    outf.write("Fixed --> Wrd2_1 Wrd2_2\n")
    outf.write("Fixed --> Wrd3_1 Wrd3_2 Wrd3_3\n")
    outf.write("Wrd1_1 --> Word\n")
    outf.write("Wrd2_1 --> Word\n")
    outf.write("Wrd2_2 --> Word\n")
    outf.write("Wrd3_1 --> Word\n")
    outf.write("Wrd3_2 --> Word\n")
    outf.write("Wrd3_3 --> Word\n")
    outf.write("Word --> Segments\n")
    outf.write("1 1 Segments --> Segment\n")
    outf.write("1 1 Segments --> Segments Segment\n")
    for segment in segments:
        outf.write("1 1 Segment --> %s\n"%segment)

def fixedfree(outf, (prefixes,topics,segments)):
    """this grammar generates collocations where there are different
    distributions for words in each position.  Hopefully this will 
    generate something that looks like phrases."""
    outf.write("1 1 Collocs --> Collocs Fixed\n")
    outf.write("1 1 Collocs --> Collocs Free\n")
    for prefix in prefixes:
        outf.write("1 1 Collocs --> T_%s\n"%prefix)
    outf.write("Fixed --> Word11\n")
    outf.write("Fixed --> Word21 Word22\n")
    outf.write("Fixed --> Word31 Word32 Word33\n")
    outf.write("Word11 --> Segments\n")
    outf.write("Word21 --> Segments\n")
    outf.write("Word22 --> Segments\n")
    outf.write("Word31 --> Segments\n")
    outf.write("Word32 --> Segments\n")
    outf.write("Word33 --> Segments\n")
    outf.write("Free --> Words\n")
    outf.write("1 1 Words --> Word\n")
    outf.write("1 1 Words --> Words Word\n")
    outf.write("Word --> Segments\n")
    outf.write("1 1 Segments --> Segment\n")
    outf.write("1 1 Segments --> Segments Segment\n")
    for segment in segments:
        outf.write("1 1 Segment --> %s\n"%segment)

def Hfixedfree(outf, (prefixes,topics,segments)):
    """this grammar generates collocations where there are different
    distributions for words in each position.  Hopefully this will 
    generate something that looks like phrases."""
    outf.write("1 1 Collocs --> Collocs Fixed\n")
    outf.write("1 1 Collocs --> Collocs Free\n")
    for prefix in prefixes:
        outf.write("1 1 Collocs --> T_%s\n"%prefix)
    outf.write("Fixed --> Wrd1_1\n")
    outf.write("Fixed --> Wrd2_1 Wrd2_2\n")
    outf.write("Fixed --> Wrd3_1 Wrd3_2 Wrd3_3\n")
    outf.write("Wrd1_1 --> Word\n")
    outf.write("Wrd2_1 --> Word\n")
    outf.write("Wrd2_2 --> Word\n")
    outf.write("Wrd3_1 --> Word\n")
    outf.write("Wrd3_2 --> Word\n")
    outf.write("Wrd3_3 --> Word\n")
    outf.write("Free --> Words\n")
    outf.write("1 1 Words --> Word\n")
    outf.write("1 1 Words --> Words Word\n")
    outf.write("Word --> Segments\n")
    outf.write("1 1 Segments --> Segment\n")
    outf.write("1 1 Segments --> Segments Segment\n")
    for segment in segments:
        outf.write("1 1 Segment --> %s\n"%segment)

def fixedfreef(outf, (prefixes,topics,segments)):
    """this grammar generates collocations where there are different
    distributions for words in each position.  Hopefully this will 
    generate something that looks like phrases.
    Final words in fixed phrases are shared"""
    outf.write("1 1 Collocs --> Collocs Fixed\n")
    outf.write("1 1 Collocs --> Collocs Free\n")
    for prefix in prefixes:
        outf.write("1 1 Collocs --> T_%s\n"%prefix)
    outf.write("Fixed --> Word0\n")
    outf.write("Fixed --> Word21 Word0\n")
    outf.write("Fixed --> Word31 Word32 Word0\n")
    outf.write("Word0 --> Segments\n")
    outf.write("Word21 --> Segments\n")
    outf.write("Word31 --> Segments\n")
    outf.write("Word32 --> Segments\n")
    outf.write("Free --> Words\n")
    outf.write("1 1 Words --> Word\n")
    outf.write("1 1 Words --> Words Word\n")
    outf.write("Word --> Segments\n")
    outf.write("1 1 Segments --> Segment\n")
    outf.write("1 1 Segments --> Segments Segment\n")
    for segment in segments:
        outf.write("1 1 Segment --> %s\n"%segment)

def Tfixedfreef(outf, (prefixes,topics,segments)):
    """non-linguistic context topics
    topical words are always phrase-final
    all other words in a phrase are non-topic words"""
    for topic in topics:
        outf.write("1 1 Sentence --> Topic_%s\n"%topic)
        outf.write("1 1 Topic_%s --> Topic_%s Fixed\n"%(topic,topic))
        outf.write("1 1 Topic_%s --> Topic_%s Free\n"%(topic,topic))
        for prefix in prefixes:
            if topic in prefix.split('|'):
                outf.write("1 1 Topic_%s --> T_%s\n"%(topic,prefix))
        if topic == 'None':
            outf.write("1 1 Topic_None --> T_None\n")
        else:
            outf.write("1 1 Topic_%s --> Topic_%s Fixed_%s\n"%(topic,topic,topic))
            outf.write("1 1 Topic_%s --> Topic_%s Free_%s\n"%(topic,topic,topic))
            outf.write("Fixed_%s --> Word0_%s\n"%(topic,topic))
            outf.write("Fixed_%s --> Word21 Word0_%s\n"%(topic,topic))
            outf.write("Fixed_%s --> Word31 Word32 Word0_%s\n"%(topic,topic))
            outf.write("Word0_%s --> Segments\n"%topic)
            outf.write("Free_%s --> Words Word_%s\n"%(topic,topic))
            outf.write("Word_%s --> Segments\n"%topic)
    outf.write("Fixed --> Word0\n")
    outf.write("Fixed --> Word21 Word0\n")
    outf.write("Fixed --> Word31 Word32 Word0\n")
    outf.write("Word0 --> Segments\n")
    outf.write("Word21 --> Segments\n")
    outf.write("Word31 --> Segments\n")
    outf.write("Word32 --> Segments\n")
    outf.write("Free --> Words\n")
    outf.write("1 1 Words --> Word\n")
    outf.write("1 1 Words --> Words Word\n")
    outf.write("1 1 Segments --> Segment\n")
    outf.write("1 1 Segments --> Segments Segment\n")
    for segment in segments:
        outf.write("1 1 Segment --> %s\n"%segment)

def Tfinal(outf, (prefixes,topics,segments)):
    """non-linguistic context topics
    topical words are always phrase-final
    all other words in a phrase are non-topic words"""
    for topic in topics:
        outf.write("1 1 Sentence --> Topic_%s\n"%topic)
        outf.write("1 1 Topic_%s --> Topic_%s Colloc\n"%(topic,topic))
        outf.write("1 1 Topic_%s --> Topic_%s Phrase\n"%(topic,topic))
        for prefix in prefixes:
            if topic in prefix.split('|'):
                outf.write("1 1 Topic_%s --> T_%s\n"%(topic,prefix))
        if topic == 'None':
            outf.write("1 1 Topic_None --> T_None\n")
        else:
            outf.write("1 1 Topic_%s --> Topic_%s Phrase_%s\n"%(topic,topic,topic))
            outf.write("Phrase_%s --> Word1 Word2_%s\n"%(topic,topic))
            outf.write("Word2_%s --> Segments\n"%topic)
    outf.write("Colloc --> Words\n")
    outf.write("1 1 Words --> Word\n")
    outf.write("1 1 Words --> Words Word\n")
    outf.write("1 1 Phrase --> Word1 Word2\n")
    outf.write("Word --> Segments\n")
    outf.write("Word1 --> Segments\n")
    outf.write("Word2 --> Segments\n")
    outf.write("1 1 Segments --> Segment\n")
    outf.write("1 1 Segments --> Segments Segment\n")
    for segment in segments:
        outf.write("1 1 Segment --> %s\n"%segment)

def HTfinal(outf, (prefixes,topics,segments)):
    """non-linguistic context topics
    topical words are always phrase-final
    all other words in a phrase are non-topic words.
    All words are generated from a common base Word distribution"""
    for topic in topics:
        outf.write("1 1 Sentence --> Topic_%s\n"%topic)
        outf.write("1 1 Topic_%s --> Topic_%s Colloc\n"%(topic,topic))
        outf.write("1 1 Topic_%s --> Topic_%s Phrase\n"%(topic,topic))
        for prefix in prefixes:
            if topic in prefix.split('|'):
                outf.write("1 1 Topic_%s --> T_%s\n"%(topic,prefix))
        if topic == 'None':
            outf.write("1 1 Topic_None --> T_None\n")
        else:
            outf.write("1 1 Topic_%s --> Topic_%s Phrase_%s\n"%(topic,topic,topic))
            outf.write("Phrase_%s --> Word1 Word2_%s\n"%(topic,topic))
            outf.write("Word2_%s --> BaseWord\n"%topic)
    outf.write("Colloc --> Words\n")
    outf.write("1 1 Words --> Word\n")
    outf.write("1 1 Words --> Words Word\n")
    outf.write("1 1 Phrase --> Word1 Word2\n")
    outf.write("Word --> BaseWord\n")
    outf.write("Word1 --> BaseWord\n")
    outf.write("Word2 --> BaseWord\n")
    outf.write("BaseWord --> Segments\n")
    outf.write("1 1 Segments --> Segment\n")
    outf.write("1 1 Segments --> Segments Segment\n")
    for segment in segments:
        outf.write("1 1 Segment --> %s\n"%segment)

if __name__ == "__main__":
    parser = optparse.OptionParser(usage=usage)
    parser.add_option("-g", "--grammar", dest="grammar", default="bevanunigramtopic",
                      help="type of grammar to produce (bevanunigramtopic,bevanunigramopttopic)")
    parser.add_option("-n", "--nsentences", dest="nsentences", default=0,
                      help="number of sentences in input to use (0=all)")

    (options,args) = parser.parse_args()

    if len(args) == 0:
        data = read_data(sys.stdin, options.nsentences)
    elif len(args) == 1:
        data = read_data(file(args[0], "rU"), options.nsentences)
    else:
        sys.stderr.write("## Error -- too many command line arguments: %s\n",args)
        exit()

    if options.grammar == "bevanunigramtopic":
        bevanunigramtopic(sys.stdout, data)
    elif options.grammar == "unigram":
        unigram(sys.stdout, data)
    elif options.grammar == "Hunigram":
        Hunigram(sys.stdout, data)
    elif options.grammar == "Tunigram":
        Tunigram(sys.stdout, data)
    elif options.grammar == "HTunigram":
        HTunigram(sys.stdout, data)
    elif options.grammar == "TunigramX1":
        TunigramX1(sys.stdout, data)
    elif options.grammar == "HTunigramX1":
        HTunigramX1(sys.stdout, data)
    elif options.grammar == "colloc":
        colloc(sys.stdout, data)
    elif options.grammar == "colloc2":
        colloc2(sys.stdout, data)
    elif options.grammar == "Hcolloc":
        Hcolloc(sys.stdout, data)
    elif options.grammar == "Hcolloc2":
        Hcolloc2(sys.stdout, data)
    elif options.grammar == "Hcolloc3":
        Hcolloc3(sys.stdout, data)
    elif options.grammar == "Tcolloc":
        Tcolloc(sys.stdout, data)
    elif options.grammar == "HTcolloc":
        HTcolloc(sys.stdout, data)
    elif options.grammar == "Tcolloc1":
        Tcolloc1(sys.stdout, data)
    elif options.grammar == "Tcolloc1NoLearn":
        Tcolloc1NoLearn(sys.stdout, data)
    elif options.grammar == "Tcolloc1F":
        Tcolloc1F(sys.stdout, data)
    elif options.grammar == "Tcolloc1U":
        Tcolloc1(sys.stdout, data, uniformTopics=True)
    elif options.grammar == "HTcolloc1":
        HTcolloc1(sys.stdout, data)
    elif options.grammar == "TcollocX1":
        TcollocX1(sys.stdout, data)
    elif options.grammar == "HTcollocX1":
        HTcollocX1(sys.stdout, data)
    elif options.grammar == "collocS":
        collocS(sys.stdout, data, IFflag=False)
    elif options.grammar == "collocSIF":
        collocS(sys.stdout, data, IFflag=True)
    elif options.grammar == "colloc2S":
        colloc2S(sys.stdout, data, IFflag=False)
    elif options.grammar == "colloc2SIF":
        colloc2S(sys.stdout, data, IFflag=True)
    elif options.grammar == "Tcolloc1S":
        Tcolloc1S(sys.stdout, data, IFflag=False)
    elif options.grammar == "Tcolloc1SIF":
        Tcolloc1S(sys.stdout, data, IFflag=True)
    elif options.grammar == "TcollocX1S":
        TcollocX1S(sys.stdout, data, IFflag=False)
    elif options.grammar == "TcollocX1SIF":
        TcollocX1S(sys.stdout, data, IFflag=True)
    elif options.grammar == "Tcolloc2":
        Tcolloc2S(sys.stdout, data, IFflag='Segments')
    elif options.grammar == "Tcolloc2S":
        Tcolloc2S(sys.stdout, data, IFflag=False)
    elif options.grammar == "Tcolloc2SIF":
        Tcolloc2S(sys.stdout, data, IFflag=True)
    elif options.grammar == "Tcolloc21":
        Tcolloc21S(sys.stdout, data, IFflag='Segments')
    elif options.grammar == "Tcolloc21S":
        Tcolloc21S(sys.stdout, data, IFflag=False)
    elif options.grammar == "Tcolloc21SIF":
        Tcolloc21S(sys.stdout, data, IFflag=True)
    elif options.grammar == "HTcolloc21":
        HTcolloc21S(sys.stdout, data, IFflag='Segments')
    elif options.grammar == "HTcolloc21S":
        HTcolloc21S(sys.stdout, data, IFflag=False)
    elif options.grammar == "HTcolloc21SIF":
        HTcolloc21S(sys.stdout, data, IFflag=True)
    elif options.grammar == "Tcolloc2X1":
        Tcolloc2X1S(sys.stdout, data, IFflag='Segments')
    elif options.grammar == "Tcolloc2X1S":
        Tcolloc2X1S(sys.stdout, data, IFflag=False)
    elif options.grammar == "Tcolloc2X1SIF":
        Tcolloc2X1S(sys.stdout, data, IFflag=True)
    elif options.grammar == "Tcolloc2N":
        Tcolloc2NS(sys.stdout, data, IFflag='Segments')
    elif options.grammar == "Tcolloc2NS":
        Tcolloc2NS(sys.stdout, data, IFflag=False)
    elif options.grammar == "Tcolloc2NSIF":
        Tcolloc2NS(sys.stdout, data, IFflag=True)
    elif options.grammar == "fixed":
        fixed(sys.stdout, data)
    elif options.grammar == "Hfixed":
        Hfixed(sys.stdout, data)
    elif options.grammar == "fixedfree":
        fixedfree(sys.stdout, data)
    elif options.grammar == "Hfixedfree":
        Hfixedfree(sys.stdout, data)
    elif options.grammar == "fixedfreef":
        fixedfreef(sys.stdout, data)
    elif options.grammar == "Tfixedfreef":
        Tfixedfreef(sys.stdout, data)
    elif options.grammar == "Hfixedfree":
        Hfixedfree(sys.stdout, data)
    elif options.grammar == "Tfinal":
        Tfinal(sys.stdout, data)
    elif options.grammar == "HTfinal":
        HTfinal(sys.stdout, data)
    else:
        sys.stderr.write("## Error -- unknown grammar argument: %s\n"%options.grammar)
        exit()


