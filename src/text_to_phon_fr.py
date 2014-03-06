import sys, re

words_dict = {}
with open('phonology_dict/words_fr.txt') as f:
    for line in f:
        tmp = line.split('\t')
        words_dict[tmp[0].rstrip('\t ')] = tmp[1].rstrip('\n')


def wrd_to_phn(w):
    w = w.lower()
    if w in words_dict:
        return words_dict[w]
    return ''


with open(sys.argv[1]) as rf:
    with open(sys.argv[1].split('.')[0] + '.sin', 'w') as of:
        for line in rf:
            line = re.sub('\[[^\]]*\]', '', line, count=len(line))
            line = re.sub('\([^\)]*\)', '', line, count=len(line))
            line = re.sub('&=\w*', '', line, count=len(line))
            line = line.replace('+', ' ')
            line = re.sub('[.,?!/]*', '', line, count=len(line))
            line = line.split()
            if len(line) == 0:
                continue
            doc = line[0]
            line = map(wrd_to_phn, line[1:])
            line = filter(lambda x: x!='', line)
            if line != []:
                joined = ' '.join(line)
                line = re.sub('  ', ' ', joined, count=len(line))
                of.write(doc + ' ' + line + '\n')

