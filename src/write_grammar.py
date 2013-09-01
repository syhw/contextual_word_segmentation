import sys, cPickle

# S -> _dN Words_dN
# Words_dN -> Word_dN ( Topics_dN )
# Word_dN -> Word_tK
# (adapted) Word_tK -> Phons
# Phons -> Phon ( Phons )

ADAPT_WORD = True # say if we adapt Word_tK -> Word -> Phons 
                  # (instead of directly Word_tK -> Phons)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "usage: python src/write_grammar.py naima_docs_11to22m.ylt all_1min_doc_topics_reseg_lemmatized.pickle"
        sys.exit(-1)

    doc_to_topics = {}
    with open(sys.argv[2]) as f:
        doc_to_topics = cPickle.load(f)
    docs = []
    phones_set = set()
    with open(sys.argv[1]) as f:
        for line in f:
            sl = line.split()
            docs.append(sl[0])
            phones_set.update(sl[1:])
    docs = set(docs)
    topics_set = set()
    with open('grammar.lt', 'w') as of:
        for doc in docs:
            # TODO simple documents clustering
            #of.write('1 1 Root --> ' + doc[1:] + ' Topics' + doc + '\n')
            #of.write('1 1 ' + doc[1:] + ' --> ' + doc + '\n')
            of.write('1 1 Root --> ' + doc + ' Topics' + doc + '\n')

            of.write('1 1 Topics' + doc + ' --> Word' + doc + '\n')
            of.write('1 1 Topics' + doc + ' --> Word' + doc + ' Topics' + doc + '\n')
        for doc, topics in doc_to_topics.iteritems():
            for topic in topics:
                topics_set.add(topic[0])
                prob = str(topic[1] * 1000000000)
                of.write(prob + ' 1 Word' + doc + ' --> Word_t' + str(topic[0]) + '\n')
        # TODO adapt Word_tI --> Word
        for topic_id in topics_set:
            if ADAPT_WORD:
                of.write('Word_t' + str(topic_id) + ' --> Word' + '\n')
            else:
                of.write('Word_t' + str(topic_id) + ' --> Phons' + '\n')
        if ADAPT_WORD:
            of.write('Word --> Phons' + '\n')
        of.write('1 1 Phons --> Phon' + '\n')
        of.write('1 1 Phons --> Phon Phons' + '\n')
        for phn in phones_set:
            of.write('1 1 Phon --> ' + phn + '\n')
        print "written grammar.lt"


