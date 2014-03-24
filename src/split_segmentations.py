import sys, glob
import itertools

usage = """python src/split_segmentations.py folder_with_segs topic_prefixed.ylt goldfile
produces *_tK.seg and *_tK.gold files split by topic prefixes"""


if len(sys.argv) < 4:
    print usage
    sys.exit(-1)

folder = sys.argv[1].rstrip('/') + '/'
yltfile = sys.argv[2]
goldfile = sys.argv[3]
# split gold and segmentations
for fname in itertools.chain(glob.iglob(folder + "*5??.seg"), [goldfile]):
    print fname
    with open(fname) as f:
        with open(yltfile) as t:
            fds = {}
            for line in t:
                topic = line.split()[0]
                if topic not in fds:
                    tmp = fname.split('.')
                    fds[topic] = open(tmp[0] + topic + '.' + tmp[-1], 'w')
                fds[topic].write(f.readline())
            for fd in fds.itervalues():
                fd.close()
