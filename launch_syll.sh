./py-cfg_grammarsamples/py-cfg-mp -n 100 -A output_syll.prs -F output_syll.trace -G output_syll.wlt -x 1 -E -d 101 -a 0.0001 -b 10000 -e 1 -f 1 -g 100 -h 0.001 -R -1 -Y "cat > output_syll.samples" -P syll.lt < ${1}.ylt
python scripts/trees-words.py -c "^Word" -i "^_d" < output_syll.prs > output_syll.seg
python scripts/eval.py -g ${1}.gold < output_syll.seg

