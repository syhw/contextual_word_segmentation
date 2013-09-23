import sys, cPickle

# S --> _dN Topics_dN
# Topics_dN --> Word_dN ( Topics_dN )
# [lda prob] Word_dN --> Word_tK
# [adapted] Word_tK --> Phons
# Phons --> Phon ( Phons )

PROB_MULTIPLIER = 1000000
ADAPT_WORD = True # say if we adapt Word_tK --> Word --> Phons 
                  # (instead of directly Word_tK --> Phons)
DOC_COLLOC = False # S --> _dN Collocs1_dN
                  # Collocs1_dN --> Colloc1_dN Collocs1_dN
                  # Collocs1_dN --> Colloc1_dN
                  # [adapted] Colloc1_dN --> Words_dN
                  # Words_dN --> Word_dN Words_dN
                  # Words_dN --> Word_dN
                  # [lda prob] Word_dN --> Word_tK
                  # [adapted] Word_tK --> Phons
TOPICS_COLLOC = False # S --> _dN Topics_dN
                     # [lda prob] Topics_dN --> Collocs1_tK
                     # Collocs1_tK --> Colloc1_tK Collocs1_tK
                     # Collocs1_tK --> Colloc1_tK
                     # [adapted] Colloc_tK --> Words_tK
                     # Words_tK --> Word_tK Words_tK
                     # Words_tK --> Word_tK
                     # [adapted] Word_tK --> Phons
# mutual exclusivity
assert((not DOC_COLLOC and not TOPICS_COLLOC) or DOC_COLLOC != TOPICS_COLLOC) 


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "usage: python src/write_grammar.py Naima_docs_11to22m.ylt all_1min_doc_topics_reseg_lemmatized.pickle"
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

            if DOC_COLLOC:
                of.write('1 1 Root --> ' + doc + ' Collocs1' + doc + '\n')
                of.write('1 1 Collocs1' + doc + ' --> Colloc1' + doc + '\n')
                of.write('1 1 Collocs1' + doc + ' --> Colloc1' + doc + ' Collocs1' + doc + '\n')
                of.write('Colloc1' + doc + ' --> Words' + doc + '\n')
                of.write('1 1 Words' + doc + ' --> Word' + doc + '\n')
                of.write('1 1 Words' + doc + ' --> Word' + doc + ' Words' + doc + '\n')
            elif TOPICS_COLLOC:
                of.write('1 1 Root --> ' + doc + ' Topics' + doc + '\n')
            else:
                of.write('1 1 Root --> ' + doc + ' Topics' + doc + '\n')
                of.write('1 1 Topics' + doc + ' --> Word' + doc + '\n')
                of.write('1 1 Topics' + doc + ' --> Word' + doc + ' Topics' + doc + '\n')

        for doc, topics in doc_to_topics.iteritems():
            for topic in topics:
                topics_set.add(topic[0])
                prob = str(topic[1] * PROB_MULTIPLIER)
                tK = '_t' + str(topic[0])

                if TOPICS_COLLOC:
                    of.write(prob + ' 1 Topics' + doc + ' --> Collocs1' + tK + '\n')
                    of.write('1 1 Collocs1' + tK + ' --> Colloc1' + tK + '\n')
                    of.write('1 1 Collocs1' + tK + ' --> Colloc1' + tK + ' Collocs1' + tK + '\n')
                    of.write('Colloc1' + tK + ' --> Words' + tK + '\n')
                    of.write('1 1 Words' + tK + ' --> Word' + tK + '\n')
                    of.write('1 1 Words' + tK + ' --> Word' + tK + ' Words' + tK + '\n')
                else:
                    of.write(prob + ' 1 Word' + doc + ' --> Word' + tK + '\n')

        for topic_id in topics_set:
            tid = str(topic_id)
            if ADAPT_WORD:
                of.write('Word_t' + tid + ' --> Word' + '\n')
            else:
                of.write('Word_t' + tid + ' --> Phons' + '\n')
        if ADAPT_WORD:
            of.write('Word --> Phons' + '\n')
        of.write('1 1 Phons --> Phon' + '\n')
        of.write('1 1 Phons --> Phon Phons' + '\n')
        for phn in phones_set:
            of.write('1 1 Phon --> ' + phn + '\n')
        print "written grammar.lt"


