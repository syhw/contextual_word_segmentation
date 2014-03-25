import sys

usage = """usage: python src/topics_learning_grammars.py $CHILDFOLDER $YLTINPUT $NTOPICS $NLEVELS"""

syll = """1 1 Struct --> SyllIF
1 1 Struct --> SyllI Sylls
1 1 Sylls --> SyllF
1 1 Sylls --> Syll Sylls
2 1 Syll --> Onset Rhyme
1 1 Syll --> Rhyme
2 1 SyllI --> OnsetI Rhyme
1 1 SyllI --> Rhyme
2 1 SyllF --> Onset RhymeF
1 1 SyllF --> RhymeF
2 1 SyllIF --> OnsetI RhymeF
1 1 SyllIF --> RhymeF
2 1 Rhyme --> Nucleus
1 1 Rhyme --> Nucleus Coda
2 1 RhymeF --> Nucleus CodaF
1 1 RhymeF --> Nucleus
Onset --> Consonants
OnsetI --> Consonants
Nucleus --> Vowels
Coda --> Consonants
CodaF --> Consonants
1 1 Consonants --> Consonant
1 1 Consonants --> Consonant Consonants
1 1 Vowels --> Vowel
1 1 Vowels --> Vowel Vowel
1 1 Vowel --> A
1 1 Vowel --> a
1 1 Vowel --> e
1 1 Vowel --> &
1 1 Vowel --> i
1 1 Vowel --> o
1 1 Vowel --> 1
1 1 Vowel --> I
1 1 Vowel --> 3
1 1 Vowel --> 2
1 1 Vowel --> 5
1 1 Vowel --> 4
1 1 Vowel --> O
1 1 Vowel --> 6
1 1 Vowel --> y
1 1 Vowel --> u
1 1 Vowel --> R
1 1 Vowel --> U
1 1 Consonant --> 9
1 1 Consonant --> C
1 1 Consonant --> D
1 1 Consonant --> J
1 1 Consonant --> N
1 1 Consonant --> S
1 1 Consonant --> T
1 1 Consonant --> Z
1 1 Consonant --> b
1 1 Consonant --> d
1 1 Consonant --> g
1 1 Consonant --> f
1 1 Consonant --> h
1 1 Consonant --> k
1 1 Consonant --> m
1 1 Consonant --> l
1 1 Consonant --> n
1 1 Consonant --> p
1 1 Consonant --> s
1 1 Consonant --> r
1 1 Consonant --> t
1 1 Consonant --> w
1 1 Consonant --> v
1 1 Consonant --> z
"""

phons = """1 1 Phons --> Phon
1 1 Phons --> Phon Phons
1 1 Phon --> &
1 1 Phon --> 1
1 1 Phon --> 3
1 1 Phon --> 2
1 1 Phon --> 5
1 1 Phon --> 4
1 1 Phon --> 6
1 1 Phon --> 9
1 1 Phon --> A
1 1 Phon --> C
1 1 Phon --> D
1 1 Phon --> I
1 1 Phon --> J
1 1 Phon --> O
1 1 Phon --> N
1 1 Phon --> S
1 1 Phon --> R
1 1 Phon --> U
1 1 Phon --> T
1 1 Phon --> Z
1 1 Phon --> a
1 1 Phon --> b
1 1 Phon --> e
1 1 Phon --> d
1 1 Phon --> g
1 1 Phon --> f
1 1 Phon --> i
1 1 Phon --> h
1 1 Phon --> k
1 1 Phon --> m
1 1 Phon --> l
1 1 Phon --> o
1 1 Phon --> n
1 1 Phon --> p
1 1 Phon --> s
1 1 Phon --> r
1 1 Phon --> u
1 1 Phon --> t
1 1 Phon --> w
1 1 Phon --> v
1 1 Phon --> y
1 1 Phon --> z
"""


def find_docs_boundaries(ylt_input):
    min_, max_ = -1, -1
    with open(ylt_input) as f:
        for line in f:
            if not len(line):
                continue
            tmp = int(line.split()[0][2:])
            if min_ == -1:
                min_ = tmp
            max_ = tmp
    return min_, max_


def generate_grammars(min_, max_, ntopics, nlevels):
    header = ""
    header_collocs = ""
    colloc = ""
    levels = ""
    colloc_common = ""
    for dN in xrange(min_, max_+1):
        dNstr = str(dN)
        header += "1 1 Root --> _d" + dNstr + " d" + dNstr + '\n'
        for tN in xrange(ntopics):
            tNstr = str(tN)
            header_collocs += "1 1 d" + dNstr + " --> Collocs_t" + tNstr + '\n'
            levels += "1 1 d" + dNstr + " --> Levels" + str(nlevels) + '_t' + tNstr + '\n'
    colloc_common += "1 1 Collocs_ --> Colloc_ Collocs_\n"
    colloc_common += "1 1 Collocs_ --> Colloc_\n"
    colloc_common += "Colloc_ --> Words_\n"
    colloc_common += "1 1 Words_ --> Word_\n"
    colloc_common += "1 1 Words_ --> Word_ Words_\n"
    colloc_common += "Word_ --> Struct\n"
    for tN in xrange(ntopics):
        tNstr = str(tN)
        header_collocs += "Colloc_t" + tNstr + " --> Words_t" + tNstr + '\n'
        header_collocs += "1 1 Words_t" + tNstr + " --> Word_t" + tNstr + '\n'
        header_collocs += "1 1 Words_t" + tNstr + " --> Word_t" + tNstr + " Words_t" + tNstr + '\n'
        header_collocs += "Word_t" + tNstr + " --> Struct\n"
        colloc += "1 1 Collocs_t" + tNstr + " --> Colloc_t" + tNstr + " Collocs_t" + tNstr + '\n'
        colloc += "1 1 Collocs_t" + tNstr + " --> Colloc_t" + tNstr + '\n'
        colloc_common += "1 1 Collocs_t" + tNstr + " --> Collocs_\n"
        colloc_common += "1 1 Collocs_t" + tNstr + " --> Collocs_ Collocs_t" + tNstr + '\n'
        colloc_common += "1 1 Collocs_t" + tNstr + " --> Colloc_t" + tNstr + " Collocs_t" + tNstr + '\n'
        colloc_common += "1 1 Collocs_t" + tNstr + " --> Colloc_t" + tNstr + " Collocs_\n"
        colloc_common += "1 1 Collocs_t" + tNstr + " --> Colloc_t" + tNstr + '\n'
        for lN in xrange(nlevels+1):
            lNstr = str(lN)
            levels += "1 1 Levels" + lNstr + '_t' + tNstr + " --> Level" + lNstr + '_t' + tNstr + " Levels" + lNstr + '_t' + tNstr + '\n'
            levels += "1 1 Levels" + lNstr + '_t' + tNstr + " --> Level" + lNstr + '_t' + tNstr + '\n'
            if lN == 0:
                levels += "Level" + lNstr + '_t' + tNstr + " --> Phons\n"
            else:
                levels += "Level" + lNstr + '_t' + tNstr + " --> Levels" + str(lN-1) + '_t' + tNstr + '\n'
    colloc_syll_g = header + header_collocs + colloc + syll
    colloc_common_syll_g = header + header_collocs + colloc_common + syll
    levels_g = header + levels + phons
    return {"colloc_syll_learn_topics": colloc_syll_g, 
            "colloc_common_syll_learn_topics": colloc_common_syll_g, 
            "levels_" + str(nlevels) + "_learn_topics": levels_g}


def write_grammars(folder, grammars):
    for gname, g in grammars.iteritems():
        with open(folder + '/' + gname + '.lt', 'w') as f:
            f.write(g)


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print usage
        sys.exit(-1)
    ntopics, nlevels = map(int, sys.argv[3:5])
    min_, max_ = find_docs_boundaries(sys.argv[2])
    write_grammars(sys.argv[1].rstrip('/'), 
        generate_grammars(min_, max_, ntopics, nlevels))
    

