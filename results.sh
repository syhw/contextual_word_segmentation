. /etc/profile.d/modules.sh
module load python-anaconda/2.7.5
python scripts/trees-words.py -c "^Word" -i "^_d" < ${1} > ${2}
python scripts/eval.py -g ${3} < ${2}
