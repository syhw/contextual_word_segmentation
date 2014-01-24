import glob, sys, shutil

if len(sys.argv) != 2:
    print "usage: python src/cut_too_long.py PATH_TO/CHILDREN (*.txt files)"

DEBUG = False
N_WORDS_MAX = 42
conjs = ", but and because or nor yet so".split()
point = "(.)"


def split_with_conjs(p):
    """ splits the phrase p according to the conjunctions conjs, in order """
    r_split = [p]
    all_small_enough = lambda w: reduce(lambda x, y: x and y, map(lambda z: len(z.split()) < N_WORDS_MAX, w))
    ind_conjs = 0
    while not all_small_enough(r_split) and ind_conjs < len(conjs):
        tmp = [sub2 for sub1 in r_split for sub2 in sub1.split(conjs[ind_conjs])]
        ind_conjs += 1
        r_split = tmp
    return r_split
        

searching_for = sys.argv[1] + '*.txt'
cuts = 0
print "searching for theses files", searching_for
print "maximum number of words:", N_WORDS_MAX
for fname in glob.iglob(searching_for):
    fname_r = fname+'_before_split'
    shutil.move(fname, fname_r)
    with open(fname_r) as f:
        with open(fname, 'w') as wf:
            for line in f:
                if '\t' in line:
                    tmp = line.replace('\x15', '').replace('\n', '').split('\t') 
                    h, l = tmp[0], tmp[-1]
                    if h[0] != '_':
                        continue
                    phrase = l.split()
                    if len(phrase) > N_WORDS_MAX:
                        fullsplit = []
                        sp = l.split(point)
                        for piece in sp:
                            if len(piece.split()) > N_WORDS_MAX:
                                fullsplit.extend(split_with_conjs(piece))
                            else:
                                fullsplit.append(piece)
                        if DEBUG:
                            print "================================="
                            print l
                            print fullsplit
                        cuts += 1
                        for piece in fullsplit:
                            wf.write(''.join(tmp[:-1]) + piece + '\n')
                    else:
                        wf.write(line.replace('\x15', ''))
print "we did %d cuts" % cuts
