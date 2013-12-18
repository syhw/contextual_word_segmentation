./py-cfg_grammarsamples/py-cfg-mp -n 100 -A output_uni.prs -F output_uni.trace -G output_unig.wlt -x 1 -E -d 101 -a 0.0001 -b 10000 -e 1 -f 1 -g 100 -h 0.001 -R -1 -Y "cat > output_uni.samples" -P unigram.lt < ${1}.ylt
python scripts/trees-words.py -c "^Word" -i "^_d" < output_uni.prs > output_uni.seg
python scripts/eval.py -g ${1}.gold < output_uni.seg

