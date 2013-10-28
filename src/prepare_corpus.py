from gensim import corpora, models, similarities, utils

from gensim.corpora.dictionary import Dictionary
from gensim.corpora.textcorpus import TextCorpus
from gensim.corpora.mmcorpus import MmCorpus

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

import glob, sys, cPickle, re

NO_BELOW = 5 # no word used less than 5 times
NO_ABOVE = 0.1 # no word which is in above 10% of the corpus
VOCAB_SIZE = 5000 # 5k, more?
LEMMATIZE = utils.HAS_PATTERN
#LEMMATIZE = False
N_TOPICS = 6 # number of topics
FILTER_WORDS = 'phonology_dict/filterWords.txt' # path to a list of words to remove
FILTER_WORDS_ADD = 'to_filter.txt'
ONLY_NOUN_VERBS = True
if not LEMMATIZE:
    ONLY_NOUN_VERBS = False
HDP = True

def tokenize(text):
    return [token.encode('utf8') for token in utils.tokenize(text, lower=True, errors='ignore') if 2 <= len(token) <= 20 and not token.startswith('_')]

class ProvidenceCorpus(TextCorpus):
    def __init__(self, folder, dictionary=None):
        """
        Takes the list of txt files in a folder from Isabelle 
        as input and builds the dictionary and corpus
        """
        self.folder = folder
        if dictionary is None:
            self.dictionary = Dictionary(self.get_texts())
            self.dictionary.filter_extremes(no_below=NO_BELOW, 
                    no_above=NO_ABOVE, keep_n=VOCAB_SIZE)
        else:
            self.dictionary = dictionary


    def get_texts(self):
        """
        Iterate over the "documents" (sessions/places) returning text
        """
        if FILTER_WORDS:
            filter_words = []
            with open(FILTER_WORDS) as f:
                for line in f:
                    filter_words.append(line.rstrip('\n'))
            filter_words = set(filter_words)
            print "the following words will be filtered", filter_words
        if FILTER_WORDS_ADD:
            filter_words_add = []
            with open(FILTER_WORDS_ADD) as f:
                for line in f:
                    filter_words_add.append(line.rstrip('\n'))
            filter_words_add = set(filter_words_add)
            print "and the other the following words will be filtered", filter_words_add

        positions, hn_articles = 0, 0
        fnamelist = []
        docs = 0
        for g in glob.iglob(self.folder + '/*.txt'):
            fnamelist.append(g)
        for fileno, fname in enumerate(fnamelist):
            with open(fname) as f:
                text = ""
                for line in f:
                    if line[0] != '@':
                        #sentence = re.sub('\d+', '', line.rstrip('\n').strip('\t').replace('\n', '')).split(' ')
                        sentence = tokenize(re.sub('\d+', '', line.rstrip('\n').strip('\t').replace('\n', '')))
                        for ind, word in enumerate(sentence):
                            w = word.lower().rstrip(' ').strip(' ').strip('\t')
                            sentence[ind] = w
                        if FILTER_WORDS:
                            for ind, word in enumerate(sentence):
                                if word.upper() in filter_words:
                                    sentence[ind] = ''
                        if FILTER_WORDS_ADD:
                            for ind, word in enumerate(sentence):
                                if word in filter_words_add:
                                    sentence[ind] = ''
                        text += ' '.join(sentence) + ' '
                    else:
                        docs += 1
                        if LEMMATIZE:
                            result = utils.lemmatize(text)
                            if ONLY_NOUN_VERBS:
                                result = filter(lambda x: x.split('/')[-1] == 'VB' or x.split('/')[-1] == 'NN', result)
                            positions += len(result)
                            yield result
                        else:
                            result = tokenize(text) # text into tokens here
                            positions += len(result)
                            yield result
                        text = ""
                docs += 1
                if LEMMATIZE:
                    result = utils.lemmatize(text)
                    if ONLY_NOUN_VERBS:
                        result = filter(lambda x: x.split('/')[-1] == 'VB' or x.split('/')[-1] == 'NN', result)
                    positions += len(result)
                    yield result
                else:
                    result = tokenize(text) # text into tokens here
                    positions += len(result)
                    yield result

        print (">>> finished iterating over the corpus of %i documents with %i positions" % (docs, positions))

        self.length = docs # cache corpus length


if __name__ == '__main__':
    if len(sys.argv) > 1:
        print "Usage, see __name__ == '__main__' ==> TODO"
        sys.exit(-1)

    if LEMMATIZE:
        print "you have pattern: we will lemmatize ('you were'->'be/VB')"
        outputname = 'provi_reseg_lemmatized'
    else:
        print "you don't have pattern: we will tokenize ('you were'->'you','were')"
        outputname = 'provi_reseg_tokenized'

    try:
        id2token = Dictionary.load_from_text(outputname + '_wordids.txt')
        mm = MmCorpus(outputname + '_bow.mm')
        print ">>> Loaded corpus from serialized files"
    except:
        print ">>> Extracting articles..."
        corpus = ProvidenceCorpus('ProviOverSeg')
        corpus.dictionary.save_as_text(outputname + '_wordids.txt')
        print ">>> Saved dictionary as " + outputname + "_wordids.txt"
        MmCorpus.serialize(outputname + '_bow.mm', corpus, progress_cnt=1000)
        print ">>> Saved MM corpus as " + outputname + "_bow.mm"
        id2token = Dictionary.load_from_text(outputname + '_wordids.txt')
        mm = MmCorpus(outputname + '_bow.mm')
        del corpus

    if HDP:
        lda = models.hdpmodel.HdpModel(corpus=mm, id2word=id2token, 
                gamma=0.01, alpha=0.01,
                kappa=0.001, tau=128.0, T=100, K=10, scale=0.1, 
                var_converge=0.000001)
        f = open(outputname + '.hdpmodel', 'w')
    else:
        lda = models.ldamodel.LdaModel(corpus=mm, id2word=id2token, 
                #num_topics=N_TOPICS, update_every=0, passes=42)
                num_topics=N_TOPICS, update_every=1, chunksize=420, passes=42)
        f = open(outputname + '.ldamodel', 'w')

    cPickle.dump(lda, f)
    f.close()

    if not HDP:
        alpha = [float(i)**2 for i in range(1, N_TOPICS+1)] # enforcing sparsity on topics
        # with the first topic 40 less probable than the 40th
        div = sum(alpha)
        alpha = [x/div for x in alpha]
        lda_sparse = models.ldamodel.LdaModel(corpus=mm, id2word=id2token, 
                #num_topics=N_TOPICS, update_every=0, passes=42,
                num_topics=N_TOPICS, update_every=1, chunksize=420, passes=51,
                alpha=alpha)

        f = open(outputname + '.ldasparsemodel', 'w')
        cPickle.dump(lda_sparse, f)

    print "================================================"
    if HDP:
        print ">>> hdp normal"
        lda.print_topics(topics=50, topn=50)
        print "------------------------------------------------"
        lda.optimal_ordering()
        lda.print_topics(topics=50, topn=50)
    else:
        print ">>> lda normal"
        lda.print_topics(N_TOPICS, topn=20)
        print "------------------------------------------------"
        print ">>> lda sparse prior"
        lda_sparse.print_topics(N_TOPICS, topn=20)


