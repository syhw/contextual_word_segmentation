import sys, random
usage = "usage: python src/randomize_topics.py ylt_file_with_topic_prefixes"
if len(sys.argv) < 2:
    print usage
    sys.exit(-1)
folder = '/'.join(sys.argv[1].split('/')[:-1])
sourcename = sys.argv[1].split('/')[-1]
if not "_topic_" in sourcename:
    print usage
    sys.exit(-1)
#outputname = sourcename.replace('_topic_', '_random_topic_')
with open(sys.argv[1]) as f:
    for line in f:
        new_topic_number = str(random.randint(0, 6)) # TODO number of topics
        print "_t"+new_topic_number + " " + " ".join(line.split()[1:])

