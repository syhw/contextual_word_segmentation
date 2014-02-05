from gensim import corpora, models, similarities, utils

from gensim.corpora.dictionary import Dictionary
from gensim.corpora.textcorpus import TextCorpus
from gensim.corpora.mmcorpus import MmCorpus

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

import glob, sys, cPickle, re
from subprocess import Popen, PIPE 
from unidecode import unidecode

FOLDER = "ProvidenceFinal/Final"
NO_BELOW = 20 # no word used less than 20 times
NO_ABOVE = 0.5 # no word which is in above 50% of the corpus
VOCAB_SIZE = 10000 # 10k, more?
N_TOPICS = 7 # number of topics
FILTER_WORDS = 'phonology_dict/filterWords.txt' # path to a list of words to remove
LANG = 'en'
FILTER_WORDS_ADD = 'to_filter.txt'
LEMMATIZE = True # by default
ONLY_NOUN_VERBS = False # only works with the lemmatizer
ONLY_NOUNS = True # only works with the lemmatizer
DO_SPARSE_LDA = False # train the sparse LDA
DEBUG = True # debug output
lemmatizer = None # scope to find the object

def tokenize(text, min_size=2):
    return [token.encode('utf8') for token in utils.tokenize(text, lower=True, errors='ignore') if min_size <= len(token) <= 20 and not token.startswith('_')]


def english_lemmatizer(text):
    """ calls the "pattern" module lemmatizer through utils """
    result = utils.lemmatize(text)
    if ONLY_NOUN_VERBS:
        result = filter(lambda x: x.split('/')[-1] == 'VB' or x.split('/')[-1] == 'NN', result)
    if ONLY_NOUNS:
        result = filter(lambda x: x.split('/')[-1] == 'NN', result)
    if DEBUG:
        print text
        print result
    return result


def french_lemmatizer(text):
    """ calls MElt lemmatizer (-L option), slow b/c MElt has no server mode """
    # TODO hack MElt into a server (not reloading the model everytime)
    # /!\ MElt mistakes a lot of tu pronouns into tu/VPP/taire
    MElt = Popen(['MElt', '-L'], stdout=PIPE, stdin=PIPE, stderr=PIPE)
    tmp = unidecode(text.decode('utf-8'))
    out = MElt.communicate(input=tmp)[0]
    result = map(lambda x: '/'.join(x.split('/')[1:]), out.split())
    if ONLY_NOUN_VERBS:
        result = filter(lambda x: x.split('/')[0] == 'V' or x.split('/')[0] == 'VINF' or x.split('/')[0] == 'NC', result)
    if ONLY_NOUNS:
        result = filter(lambda x: x.split('/')[0] == 'NC', result)
    result = filter(lambda x: not '*' in x, result) # unrecognized words
    if DEBUG:
        print tmp
        print result
    return result


class Lemmatizer:
    def __init__(self, lang):
        if lang == 'en':
            self.__call__ = english_lemmatizer
        elif lang == 'fr':
            self.__call__ = french_lemmatizer
        else:
            print >> sys.err, "this language (--(fr|en)) is not recognized"
            sys.exit(-1)


class CDS_Corpus(TextCorpus):
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
        filter_words = set()
        if FILTER_WORDS:
            filter_words = []
            with open(FILTER_WORDS) as f:
                for line in f:
                    filter_words.append(line.rstrip('\n'))
            filter_words = set(filter_words)
            #print "the following words will be filtered", filter_words
        filter_words_add = set()
        if FILTER_WORDS_ADD:
            filter_words_add = []
            with open(FILTER_WORDS_ADD) as f:
                for line in f:
                    filter_words_add.append(line.rstrip('\n'))
            filter_words_add = set(filter_words_add)

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
                        text += ' '.join(sentence) + '\n'
                    else:
                        docs += 1
                        if LEMMATIZE:
                            result = lemmatizer(text)
                            positions += len(result)
                            yield result
                        else:
                            result = tokenize(text) # text into tokens here
                            positions += len(result)
                            yield result
                        text = ""
                docs += 1
                if LEMMATIZE:
                    result = lemmatizer(text)
                    positions += len(result)
                    yield result
                else:
                    result = tokenize(text) # text into tokens here
                    positions += len(result)
                    yield result

        print (">>> finished iterating over the corpus of %i documents with %i positions" % (docs, positions))

        self.length = docs # cache corpus length


def parse_args(argv):
    """ parses args and build the correct lemmatizer if possible """
    argv_sorted = sorted(argv)
    lang = 'en'
    lemmatizer = None
    if argv_sorted[0][0] == '-':
        lang = argv_sorted[0].replace('--','')
        if lang != 'fr' and lang != 'en':
            print >> sys.err, "this language (--(fr|en)) is not recognized"
            sys.exit(-1)
    try:
        lemmatizer = Lemmatizer(lang)
    except:
        print >> sys.err, "we couldn't build the lemmatizer, tokenizing instead"
        lemmatizer = None
    if lang == 'fr':
        return lemmatizer, 'to_filter_fr.txt'
    else:
        return lemmatizer, FILTER_WORDS_ADD


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print """Usage: python src/prepare_corpus_tfidf.py $FOLDER [--(en|fr)]
        look at the start of the src/prepare_corpus_tfidf.py file for params"""
        sys.exit(-1)

    FOLDER = sys.argv[1]
    prefix = FOLDER.split('/')[0]

    if LEMMATIZE:
        lemmatizer, FILTER_WORDS_ADD = parse_args(sys.argv)
        if lemmatizer != None:
            LEMMATIZE = True
        else:
            LEMMATIZE = False

    if not LEMMATIZE:
        ONLY_NOUN_VERBS = False
        ONLY_NOUNS = False

    if LEMMATIZE:
        print "we will lemmatize ('you were'->'be/VB')"
        outputname = prefix + '_lemmatized_tfidf'
        inputname = prefix + '_lemmatized'
    else:
        print "you don't have pattern: we will tokenize ('you were'->'you','were')"
        outputname = prefix + '_tokenized_tfidf'
        inputname = prefix + '_tokenized'

    try:

        id2token = Dictionary.load_from_text(inputname + '_wordids.txt')
        mm = MmCorpus(inputname + '_bow.mm')
        print ">>> Loaded corpus from serialized files"
    except:
        print ">>> Extracting articles..."
        corpus = CDS_Corpus(FOLDER)
        corpus.dictionary.save_as_text(outputname + '_wordids.txt')
        print ">>> Saved dictionary as " + outputname + "_wordids.txt"
        MmCorpus.serialize(outputname + '_bow.mm', corpus, progress_cnt=1000)
        print ">>> Saved MM corpus as " + outputname + "_bow.mm"
        id2token = Dictionary.load_from_text(outputname + '_wordids.txt')
        mm = MmCorpus(outputname + '_bow.mm')
        del corpus

    print ">>> Using TF-IDF"
    tfidf = models.TfidfModel(mm, id2word=id2token, normalize=True)
    corpus_tfidf = tfidf[mm]

    lda = models.ldamodel.LdaModel(corpus=corpus_tfidf, id2word=id2token, 
            num_topics=N_TOPICS, update_every=0, passes=69)
            #num_topics=N_TOPICS, update_every=1, chunksize=800, passes=42)

    f = open(outputname + '.ldamodel', 'w')
    cPickle.dump(lda, f)
    f.close()

    if DO_SPARSE_LDA:
        alpha = [float(i)**2 for i in range(1, N_TOPICS+1)] # enforcing sparsity on topics
        # with the first topic 40 less probable than the 40th
        div = sum(alpha)
        alpha = [x/div for x in alpha]
        lda_sparse = models.ldamodel.LdaModel(corpus=corpus_tfidf, id2word=id2token, 
                num_topics=N_TOPICS, update_every=0, passes=51,
                #num_topics=N_TOPICS, update_every=1, chunksize=420, passes=42,
                alpha=alpha)

        f = open(outputname + '.ldasparsemodel', 'w')
        cPickle.dump(lda_sparse, f)

    print "================================================"
    print ">>> lda normal"
    lda.print_topics(N_TOPICS, topn=20)
    if DO_SPARSE_LDA:
        print "------------------------------------------------"
        print ">>> lda sparse prior"
        lda_sparse.print_topics(N_TOPICS, topn=20)


