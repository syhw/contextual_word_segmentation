import sys, cPickle

# S --> _dN Topics_dN
# Topics_dN --> Word_dN ( Topics_dN )
# [lda prob] Word_dN --> Word_tK
# [adapted] Word_tK --> Struct
# Struct --> Phons
# Phons --> Phon ( Phons )

prefix = 'grammar'
suffix = ''
PROB_MULTIPLIER = 1000000
ADAPT_WORD = False # say if we adapt Word_tK --> Word --> Struct 
                  # (instead of directly Word_tK --> Struct)
DOC_COLLOC = False # S --> _dN Collocs1_dN
                  # Collocs1_dN --> Colloc1_dN Collocs1_dN
                  # Collocs1_dN --> Colloc1_dN
                  # [adapted] Colloc1_dN --> Words_dN
                  # Words_dN --> Word_dN Words_dN
                  # Words_dN --> Word_dN
                  # [lda prob] Word_dN --> Word_tK
                  # [adapted] Word_tK --> Struct
TOPICS_COLLOC = False # S --> _dN Topics_dN
                     # [lda prob] Topics_dN --> Collocs1_tK
                     # Collocs1_tK --> Colloc1_tK Collocs1_tK
                     # Collocs1_tK --> Colloc1_tK
                     # [adapted] Colloc_tK --> Words_tK
                     # Words_tK --> Word_tK Words_tK
                     # Words_tK --> Word_tK
                     # [adapted] Word_tK --> Struct
SYLLABIC_STRUCTURE = False # as in Johnson & Goldwater 2009
                          # Struct --> SyllIF
                          # Struct --> SyllI Sylls
                          # Sylls --> SyllF
                          # Sylls --> Syll Sylls
                          # 2 Syll --> Onset Rhyme
                          # 1 Syll --> Rhyme
                          # 2 SyllI --> OnsetI Rhyme
                          # 1 SyllI --> Rhyme
                          # 2 SyllF --> Onset RhymeF
                          # 1 SyllF --> RhymeF
                          # 2 SyllIF --> OnsetI RhymeF
                          # 1 SyllIF --> RhymeF
                          # 2 Rhyme --> Nucleus
                          # 1 Rhyme --> Nucleus Coda
                          # 2 RhymeF --> Nucleus CodaF
                          # 1 RhymeF --> Nucleus
                          # [adapted] Onset --> Consonants
                          # [adapted] OnsetI --> Consonants
                          # [adapted] Nucleus --> Vowels
                          # [adapted] Coda --> Consonants
                          # [adapted] CodaF --> Consonants
                          # Consonants --> Consonant
                          # Consonants --> Consonant Consonants
                          # Vowels --> Vowel
                          # Vowels --> Vowel Vowel


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "usage: python src/write_grammar.py naima_docs_11to22m.ylt all_1min_doc_topics_reseg_lemmatized.pickle [-a -d/-t -s] [output_prefix]"
        sys.exit(-1)
    if '-a' in sys.argv:
        ADAPT_WORD = True
    if '-d' in sys.argv:
        DOC_COLLOC = True
    if '-t' in sys.argv:
        TOPICS_COLLOC = True
    if '-s' in sys.argv:
        SYLLABIC_STRUCTURE = True
    # mutual exclusivity of True for both colloc types
    assert((not DOC_COLLOC and not TOPICS_COLLOC) or DOC_COLLOC != TOPICS_COLLOC) 
    if ADAPT_WORD:
        suffix += '_readapt'
    if DOC_COLLOC:
        suffix += '_doc_colloc'
    if TOPICS_COLLOC:
        suffix += '_topics_colloc'
    if SYLLABIC_STRUCTURE:
        suffix += '_syll'
    if len(sys.argv) > 3 and sys.argv[-1][0] != '-':
        prefix = sys.argv[-1]

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
    with open(prefix + suffix + '.lt', 'w') as of:
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

        if SYLLABIC_STRUCTURE:
            of.write('1 1 Struct --> SyllIF\n')
            of.write('1 1 Struct --> SyllI Sylls\n')
            of.write('1 1 Sylls --> SyllF\n')
            of.write('1 1 Sylls --> Syll Sylls\n')
            of.write('2 1 Syll --> Onset Rhyme\n')
            of.write('1 1 Syll --> Rhyme\n')
            of.write('2 1 SyllI --> OnsetI Rhyme\n')
            of.write('1 1 SyllI --> Rhyme\n')
            of.write('2 1 SyllF --> Onset RhymeF\n')
            of.write('1 1 SyllF --> RhymeF\n')
            of.write('2 1 SyllIF --> OnsetI RhymeF\n')
            of.write('1 1 SyllIF --> RhymeF\n')
            of.write('2 1 Rhyme --> Nucleus\n')
            of.write('1 1 Rhyme --> Nucleus Coda\n')
            of.write('2 1 RhymeF --> Nucleus CodaF\n')
            of.write('1 1 RhymeF --> Nucleus\n')
            of.write('Onset --> Consonants\n')
            of.write('OnsetI --> Consonants\n')
            of.write('Nucleus --> Vowels\n')
            of.write('Coda --> Consonants\n')
            of.write('CodaF --> Consonants\n')
            of.write('1 1 Consonants --> Consonant\n')
            of.write('1 1 Consonants --> Consonant Consonants\n')
            of.write('1 1 Vowels --> Vowel\n')
            of.write('1 1 Vowels --> Vowel Vowel\n') # and not Vowel Vowel_s_!
            vowels = set(['A', '&', 'a', 'o', '1', '6', '2', 'e', '3', 'i', '4', 'I', 'O', '5', 'R', 'u', 'U', 'y'])
            consonants = phones_set - vowels
            for phn in vowels:
                of.write('1 1 Vowel --> ' + phn + '\n')
            for phn in consonants:
                of.write('1 1 Consonant --> ' + phn + '\n')
        else:
            of.write('1 1 Struct --> Phons\n')
            of.write('1 1 Phons --> Phon\n')
            of.write('1 1 Phons --> Phon Phons\n')
            for phn in phones_set:
                of.write('1 1 Phon --> ' + phn + '\n')

        for topic_id in topics_set:
            tid = str(topic_id)
            if ADAPT_WORD:
                of.write('Word_t' + tid + ' --> Word\n')
            else:
                of.write('Word_t' + tid + ' --> Struct\n')
        if ADAPT_WORD:
            of.write('Word --> Struct\n')
        print "written:"
        print prefix + suffix + ".lt"


