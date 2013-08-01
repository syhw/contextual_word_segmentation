import sys, re, cPickle
from gensim import corpora, models, similarities, utils
from gensim.corpora.dictionary import Dictionary
from gensim.corpora.textcorpus import TextCorpus
from gensim.corpora.mmcorpus import MmCorpus

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

if __name__ == '__main__':
    fname = sys.argv[1]
    bfname = fname.split('.')[0]

    LEMMATIZE = utils.HAS_PATTERN
    if LEMMATIZE:
        print "you have pattern: we will lemmatize ('you were'->'be/VB')"
        suffix = '_lemmatized'
    else:
        print "you don't have pattern: we will tokenize ('you were'->'you','were')"
        suffix = '_tokenized'
    from src.prepare_corpus import tokenize
    outputname = bfname + suffix

    with open('provi' + suffix + '.ldamodel') as f:
        lda = cPickle.load(f)

    id2token = Dictionary.load_from_text('provi' + suffix + '_wordids.txt')

    out_topics = open(bfname + '_doc_topics' + suffix + '.txt', 'w')
    out_sentences = open(bfname + '_docs' + suffix + '.sin', 'w')

    with open(fname) as f:
        text = ""
        doc = 0
        line_number = 0
        for line in f:
            if line[0] != '@':
                sentence = re.sub('\d+', '', line.rstrip('\n').replace('\n', '')) + ' '
                text += sentence
                line_number += 1
            else:
                if LEMMATIZE:
                    result = utils.lemmatize(text)
                    topics = lda[id2token.doc2bow(result)]
                else:
                    result = tokenize(text) # text into tokens here
                    topics = lda[id2token.doc2bow(result)]
                doc += 1
                out_topics.write('_d'+str(doc)+' '+str(topics)+'\n')
                out_sentences.write('_d'+str(doc)+' '+text+'\n')
                text = ""
        if LEMMATIZE:
            result = utils.lemmatize(text)
            topics = lda[id2token.doc2bow(result)]
        else:
            result = tokenize(text) # text into tokens here
            topics = lda[id2token.doc2bow(result)]
        doc += 1
        out_topics.write('_d'+str(doc)+' '+str(topics)+'\n')
        out_sentences.write('_d'+str(doc)+' '+text+'\n')

    out_topics.close()
    out_sentences.close()

