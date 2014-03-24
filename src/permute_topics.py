import sys, random
usage = "usage: python src/permute_topics.py ylt_file_with_topic_prefixes"
if len(sys.argv) < 2:
    print usage
    sys.exit(-1)
folder = '/'.join(sys.argv[1].split('/')[:-1])
sourcename = sys.argv[1].split('/')[-1]
if not "_topic_" in sourcename:
    print usage
    sys.exit(-1)
#outputname = sourcename.replace('_topic_', '_random_topic_')
lines = []
with open(sys.argv[1]) as f:
    for line in f:
        lines.append(line)
new_topic_number = str(random.randint(0, 6)) # TODO number of topics
for i, line in enumerate(lines):
    current_topic_number = line.split()[0][2] # TODO currently only with single digits
    print "_t"+new_topic_number + " " + " ".join(line.split()[1:])
    if i+1 < len(lines) and lines[i+1].split()[0][2] != current_topic_number:
        new_topic_number = str(random.randint(0, 6))

