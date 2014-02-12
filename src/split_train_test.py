import sys, random
if len(sys.argv) < 3:
    print "usage: python src/split_train_test.py YLT_FILE GOLD_FILE [TEST_FRACTION]"
test_fraction = 0.2
if len(sys.argv) == 4:
    test_fraction = float(sys.argv[3])
gold = []
with open(sys.argv[2]) as g:
    for line in g:
        gold.append(line)
with open(sys.argv[1]) as f:
    with open(sys.argv[1].split('.')[0] + '_test.ylt', 'w') as teylt:
        with open(sys.argv[1].split('.')[0] + '_train.ylt', 'w') as trylt:
            with open(sys.argv[1].split('.')[0] + '_test.gold', 'w') as tegld:
                with open(sys.argv[1].split('.')[0] + '_train.gold', 'w') as trgld:
                    for i, line in enumerate(f):
                        if random.random() < test_fraction:
                            teylt.write(line)
                            tegld.write(gold[i])
                        else:
                            trylt.write(line)
                            trgld.write(gold[i])


