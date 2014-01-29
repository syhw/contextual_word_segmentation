import gensim, cPickle, sys, re
import numpy as np
from gensim.corpora.dictionary import Dictionary
from gensim import utils
from prepare_corpus import tokenize, parse_args

usage = """python src/split_corpus.py $corpus_to_split.txt [$suffix]"""
prefix = ''
suffix = '_lemmatized_tfidf'
LEMMATIZE = True
MIN_LINES = 10 # minimum number of lines to be considered for topic-based seg.
MAX_KL_DIST = 1.0 # we add a next final doc segment when both prev and next 
                  # KL divergences are above this threshold
DEBUG = False # debug output


def find_start_end(doc):
    start = 0
    end = 0
    if len(doc) == 1:
        return start, end
    for line in doc: 
        l = re.findall('(\d+)\t\d+\t\w*', line)
        if len(l):
            start = int(l[0])
            break
    for line in doc[::-1]:
        l = re.findall('\d+\t(\d+)\t\w*', line)
        if len(l):
            end = int(l[0])
            break
    if start == 0 and end == 0:
        print 'start and end == 0 for', doc # this only happens for "headers"
        end = 5*len(' '.join(doc)) # lower bounding how fast you can pronounce
    return start, end


def extract_sentence(line):
    return re.sub('\d+', '', line.rstrip('\n').replace('\n', ''))


def compute_KL_div(t1, t2):
    # sum_i [ln(p_{t1}(i) / p_{t2}(i)) p_{t1}(i)]
    p_t1 = dict(t1)
    p_t2 = dict(t2)
    #inds = set(p_t1.keys())
    #inds = inds.intersection(set(p_t2.keys()))
    return np.sum([np.log(p_t1[i] / p_t2.get(i, 1.E-30)) * p_t1[i] for i in p_t1.keys()])


def merge_too_small(docs):
    docs = docs
    for i, doc in enumerate(docs): # first pass, small docs
        if len(doc) and '@?' in doc[0]:
            #' and len(doc[0]) > 1 and doc[0][1] == '?': we're at a disputed doc segment
            if i - 1 < 0 or i + 1 >= len(docs):
                continue
            if len(doc) <= 1:
                docs[i] = []
                continue
            if len(doc) < MIN_LINES: # too few lines => GROUP WITH CLOSEST TIME
                doc_start, doc_end = find_start_end(doc)
                p_i = i-1 # previous non empty
                for j, d in enumerate(docs[p_i::-1]):
                    if len(d):
                        break
                    p_i -= 1
                n_i = i+1 # next non empty
                for j, d in enumerate(docs[n_i:]):
                    if len(d):
                        break
                    n_i += 1
                prev_start, prev_end = find_start_end(docs[p_i])
                next_start, next_end = find_start_end(docs[n_i])
                dp = doc_start - prev_end
                nd = next_start - doc_end
                if dp < 0: # accross .cha for prev to current
                    print doc
                    print "ERROR accross prev to current"
                    sys.exit(-1)
                if nd < 0 or nd > dp: # group with prev non empty
                    #docs[p_i][0] = docs[p_i][0].replace('?', '')
                    docs[p_i].extend(doc[1:])
                    docs[i] = []
                else: # group with next
                    docs[i].extend(docs[n_i][1:])
                    docs[n_i] = []
    return filter(lambda x: len(x), docs)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print usage
        sys.exit(-1)

    fname = sys.argv[1]
    prefix = fname.split('/')[0]
    if len(sys.argv) > 2:
        suffix = sys.argv[2]

    lemmatizer = parse_args(sys.argv)
    if lemmatizer == None:
        LEMMATIZE = False
        suffix = '_tokenized_tfidf'

    lda = None
    with open(prefix + suffix + '.ldamodel') as f:
        lda = cPickle.load(f)
    id2token = Dictionary.load_from_text(prefix + suffix + '_wordids.txt')

    docs = []
    with open(fname) as f:
        print("splitting %s" % fname)
        tmp = []
        for line in f: # bufferize into docs list
            if line[0] == '@':
                docs.append(tmp)
                tmp = [line]
            else:
                tmp.append(line)
        print("with %d possible docs" % len(docs))

        docs = filter(lambda x: len(x), docs)
        n_docs_before = -1
        print "merging too small docs..."
        while n_docs_before != len(docs):
            n_docs_before = len(docs)
            docs = merge_too_small(docs)
        print "using KL-divergence..."
        for i, doc in enumerate(docs): # second pass, topics + KL-div
            if len(doc) and '@?' in doc[0]:
                # we're at a disputed doc segment
                if i - 1 < 0 or i + 1 >= len(docs):
                    continue
                if len(doc) <= 1:
                    docs[i] = []
                    continue
                p_i = i-1 # previous non empty
                for j, d in enumerate(docs[p_i::-1]):
                    if len(d):
                        break
                    p_i -= 1
                n_i = i+1 # previous non empty
                for j, d in enumerate(docs[n_i:]):
                    if len(d):
                        break
                    n_i += 1
                current_doc = ' '.join(map(extract_sentence, doc[1:]))
                prev_doc = ' '.join(map(extract_sentence, docs[p_i][1:]))
                next_doc = ' '.join(map(extract_sentence, docs[n_i][1:]))
                if LEMMATIZE:
                    current_doc = lemmatizer(current_doc)
                    prev_doc = lemmatizer(prev_doc)
                    next_doc = lemmatizer(next_doc)
                else:
                    current_doc = tokenize(current_doc)
                    prev_doc = tokenize(prev_doc)
                    next_doc = tokenize(next_doc)
                current_topics = lda[id2token.doc2bow(current_doc)]
                prev_topics = lda[id2token.doc2bow(prev_doc)]
                next_topics = lda[id2token.doc2bow(next_doc)]
                kl_div_prev = compute_KL_div(current_topics, prev_topics)
                kl_div_next = compute_KL_div(current_topics, next_topics)
                if DEBUG:
                    print current_topics
                    print prev_topics
                    print kl_div_prev
                    print next_topics
                    print kl_div_next
                if kl_div_prev > MAX_KL_DIST and kl_div_next > MAX_KL_DIST:
                    # keep this candidate doc segment in the final
                    doc[0] = '@\n'
                else:
                    # regroup with closest KL div
                    if kl_div_prev < kl_div_next: # group with previous
                        docs[p_i][0] = docs[p_i][0].replace('?', '')
                        docs[p_i].extend(doc[1:])
                        docs[i] = []
                    else: # group with next
                        docs[i].extend(docs[n_i][1:])
                        docs[i][0] = docs[i][0].replace('?', '')
                        docs[n_i] = []

        docs = filter(lambda x: len(x), docs)

    with open(sys.argv[1].split('.')[0] + '_final_split.txt', 'w') as wf:
        for doc in docs:
            for line in doc:
                wf.write(line)

