import sys, re

words_dict = {}
with open('phonology_dict/words.txt') as f:
    for line in f:
        words_dict[line.split('[')[0].rstrip('\t ')] = line.split(']')[1].split()


phns_dict = {}
with open('phonology_dict/phoneSet') as f:
    for line in f:
        tmp_l = line.split()
        phns_dict[tmp_l[0]] = tmp_l[1]


def wrd_to_phn(w):
    w = w.upper()
    if w in words_dict:
        tmp = []
        for phn in words_dict[w]:
            if not phn in phns_dict:
                return ''
            tmp.append(phns_dict[phn])
        return ''.join(tmp)
    return ''


with open(sys.argv[1]) as rf:
    with open(sys.argv[1].split('.')[0] + '.sin', 'w') as of:
        for line in rf:
            line = re.sub('\[[^\]]*\]', '', line, count=len(line))
            line = re.sub('\([^\)]*\)', '', line, count=len(line))
            line = re.sub('[.?!+/]*', '', line, count=len(line))
            line = line.split()
            doc = line[0]
            line = map(wrd_to_phn, line[1:])
            line = filter(lambda x: x!='', line)
            if line != []:
                joined = ' '.join(line)
                line = re.sub('  ', ' ', joined, count=len(line))
                of.write(doc + ' ' + line + '\n')

