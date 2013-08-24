import sys, re, cPickle
from gensim import corpora, models, similarities, utils
from gensim.corpora.dictionary import Dictionary
from gensim.corpora.textcorpus import TextCorpus
from gensim.corpora.mmcorpus import MmCorpus

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

FILTER_WORDS = 'phonology_dict/filterWords.txt' # path to a list of words to remove
TFIDF_SUFFIX = '_tfidf' # set it to the empty string for no TF-IDF

if __name__ == '__main__':
    fname = sys.argv[1]
    bfname = fname.split('.')[0]

    LEMMATIZE = utils.HAS_PATTERN
    if LEMMATIZE:
        print "you have pattern: we will lemmatize ('you were'->'be/VB')"
        suffix = '_reseg_lemmatized'
    else:
        print "you don't have pattern: we will tokenize ('you were'->'you','were')"
        suffix = '_reseg_tokenized' + TFIDF_SUFFIX
    from src.prepare_corpus import tokenize
    outputname = bfname + suffix

    with open('provi' + suffix + '.ldamodel') as f:
        lda = cPickle.load(f)

    id2token = Dictionary.load_from_text('provi' + suffix + '_wordids.txt')

    doc_topics = {}

    out_topics = open(bfname + '_doc_topics' + suffix + '.txt', 'w')
    out_sentences = open(bfname + '_doc_prefixed' + suffix + '.txt', 'w')

    if FILTER_WORDS:
        filter_words = []
        with open(FILTER_WORDS) as f:
            for line in f:
                filter_words.append(line.rstrip('\n'))
        filter_words = set(filter_words)
        print "the following words will be filtered", filter_words

    with open(fname) as f:
        text = []
        doc = 0
        for line in f:
            if line[0] != '@':
                sentence = re.sub('\d+', '', line.rstrip('\n').replace('\n', '')).split(' ')
                if FILTER_WORDS:
                    for ind, word in enumerate(sentence):
                        if word.upper().rstrip(' ').strip(' ') in filter_words:
                            sentence[ind] = ''
                text.append(' '.join(sentence))
            else:
                if LEMMATIZE:
                    result = utils.lemmatize(' '.join(text))
                    topics = lda[id2token.doc2bow(result)]
                else:
                    result = tokenize(' '.join(text)) # text into tokens here
                    topics = lda[id2token.doc2bow(result)]
                doc += 1
                doc_topics['_d'+str(doc)] = topics
                out_topics.write('_d'+str(doc)+' '+str(topics)+'\n')
                out_sentences.write('\n'.join(
                    map(lambda x: '_d'+str(doc)+' '+x, text)))
                text = []
        if LEMMATIZE:
            result = utils.lemmatize(' '.join(text))
            topics = lda[id2token.doc2bow(result)]
        else:
            result = tokenize(' '.join(text)) # text into tokens here
            topics = lda[id2token.doc2bow(result)]
        doc += 1
        doc_topics['_d'+str(doc)] = topics
        out_topics.write('_d'+str(doc)+' '+str(topics)+'\n')
        out_sentences.write('\n'.join(
            map(lambda x: '_d'+str(doc)+' '+x, text)))

    out_topics.close()
    out_sentences.close()
    with open(bfname + '_doc_topics' + suffix + '.pickle', 'w') as f:
        cPickle.dump(doc_topics, f)

