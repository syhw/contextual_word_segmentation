./py-cfg_grammarsamples/py-cfg -n 100 -G ${1}.wlt -A ${1}.prs -F ${1}.trace -x 1 -E -d 101 -a 0.0001 -b 10000 -e 1 -f 1 -g 100 -h 0.001 -R -1 -Y "cat > ${1}.samples" -P ${1}.lt < ${2}.ylt
python scripts/trees-words.py -c "^Word" -i "^_d" < ${1}.prs > ${1}.seg
python scripts/eval.py -g ${3}.gold < ${1}.seg
