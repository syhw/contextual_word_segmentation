import sys
for line in sys.stdin:
    sl = line.split()
    tmp = sl[0]
    for word in sl[1:]:
        tmp += ' ' + ' '.join([c for c in word])
    print tmp


