import sys, re, cPickle
from gensim import corpora, models, similarities, utils
from gensim.corpora.dictionary import Dictionary
from gensim.corpora.textcorpus import TextCorpus
from gensim.corpora.mmcorpus import MmCorpus

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

FILTER_WORDS = 'phonology_dict/filterWords.txt' # path to a list of words to remove
TFIDF_SUFFIX = '_tfidf' # set it to the empty string for no TF-IDF

def parse_kid(line, kid):
    """ parses a "@   ale01.cha   1;4.28" line into name/month ("ale", 16) """
    tmp = line.split('\t')
    if len(tmp) < 3 or not "cha" in tmp[1]:
        return kid
    else:
        date = tmp[2].split(';')
        return (tmp[1][:3], int(date[0]) * 12 + int(date[1].split('.')[0]))


def find_argmax(topics_list):
    """ returns the maximum probability topic id in a 
    [(topic_id, topic_prob)...] topics distribution """
    m = -1.
    r_tid = -1
    for tid, tprob in topics_list:
        if tprob > m:
            m = tprob
            r_tid = tid
    return r_tid


if __name__ == '__main__':
    fname = sys.argv[1]
    bfname = fname.split('.')[0]
    basefolder = '/'.join(fname.split('/')[:-1]) + '/'

    LEMMATIZE = utils.HAS_PATTERN
    if LEMMATIZE:
        print "you have pattern: we will lemmatize ('you were'->'be/VB')"
        suffix = '_reseg_lemmatized' + TFIDF_SUFFIX
    else:
        print "you don't have pattern: we will tokenize ('you were'->'you','were')"
        suffix = '_reseg_tokenized' + TFIDF_SUFFIX
    from prepare_corpus import tokenize
    outputname = bfname + suffix

    with open('provi' + suffix + '.ldamodel') as f:
        lda = cPickle.load(f)

    id2token = Dictionary.load_from_text('provi' + suffix + '_wordids.txt')

    doc_topics = {}

    out_topics = open(bfname + '_doc_topics' + suffix + '.txt', 'w')
    out_sentences = open(bfname + '_doc_prefixed' + suffix + '.txt', 'w')
    print "writing:", bfname + '_doc_topics', "and", bfname + '_doc_prefixed'

    if FILTER_WORDS:
        filter_words = []
        with open(FILTER_WORDS) as f:
            for line in f:
                filter_words.append(line.rstrip('\n'))
        filter_words = set(filter_words)
        print "the following words will be filtered", filter_words

    with open(fname) as f:
        text = []
        current_kid = None
        out_kid_sentences_d = None
        out_kid_sentences_t = None
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
                if doc != 0: # doc == 0 is the first header
                    if LEMMATIZE:
                        result = utils.lemmatize(' '.join(text))
                        topics = lda[id2token.doc2bow(result)]
                    else:
                        result = tokenize(' '.join(text)) # text into tokens here
                        topics = lda[id2token.doc2bow(result)]
                    doc_topics['_d'+str(doc)] = topics
                    out_topics.write('_d'+str(doc)+' '+str(topics)+'\n')
                    tmp_sentences_d = '\n'.join(
                            map(lambda x: '_d'+str(doc)+' '+x, text)) + '\n'
                    out_sentences.write(tmp_sentences_d)
                    out_kid_sentences_d.write(tmp_sentences_d)
                    cur_t = find_argmax(topics)
                    tmp_sentences_t = '\n'.join(
                            map(lambda x: '_t'+str(cur_t)+' '+x, text)) + '\n'
                    out_kid_sentences_t.write(tmp_sentences_t)
                    text = []
                new_kid = parse_kid(line, current_kid)
                if current_kid == None or new_kid[0] != current_kid[0] or new_kid[1] != current_kid[1]:
                    if doc != 0:
                        out_kid_sentences_d.close()
                        out_kid_sentences_t.close()
                    out_kid_sentences_d = open(basefolder + new_kid[0] + '_docs_' + str(new_kid[1]) + '.txt', 'w')
                    out_kid_sentences_t = open(basefolder + new_kid[0] + '_topic_' + str(new_kid[1]) + '.txt', 'w')
                    current_kid = new_kid
                doc += 1

        if LEMMATIZE:
            result = utils.lemmatize(' '.join(text))
            topics = lda[id2token.doc2bow(result)]
        else:
            result = tokenize(' '.join(text)) # text into tokens here
            topics = lda[id2token.doc2bow(result)]
        doc_topics['_d'+str(doc)] = topics
        out_topics.write('_d'+str(doc)+' '+str(topics)+'\n')
        tmp_sentences_d = '\n'.join(
            map(lambda x: '_d'+str(doc)+' '+x, text))
        out_sentences.write(tmp_sentences_d)
        out_kid_sentences_d.write(tmp_sentences_d)
        cur_t = find_argmax(topics)
        tmp_sentences_t = '\n'.join(
                map(lambda x: '_t'+str(cur_t)+' '+x, text))
        out_kid_sentences_t.write(tmp_sentences_t)
        doc += 1

    out_topics.close()
    out_sentences.close()
    out_kid_sentences_d.close()
    out_kid_sentences_t.close()
    with open(bfname + '_doc_topics' + suffix + '.pickle', 'w') as f:
        cPickle.dump(doc_topics, f)

