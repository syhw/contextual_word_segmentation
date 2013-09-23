""" done on Naima with 7 increasingly larger pieces of the corpus """

import numpy as np

# token_f-score   token_precision token_recall    boundary_f-score        boundary_precision     boundary_recall
results = np.array([[0.5773,0.5156,0.6557,0.7863,0.6836,0.925],
                    [0.5992,0.5391,0.6743,0.7963,0.6991,0.9249],
                    [0.6195,0.5648,0.686,0.81,0.724,0.919],
                    [0.6024,0.5414,0.6789,0.8044,0.7075,0.932],
                    [0.593,0.5332,0.668,0.8007,0.7049,0.9268],
                    [0.6404,0.5892,0.7014,0.8234,0.7446,0.9208],
                    #[0.6002,0.5361,0.6817,0.805,0.7036,0.9404]])
                    [0.6732,0.6256,0.7285,0.8405,0.7694,0.9261]])
import pylab as pl
#pl.plot(results[:,0])
#pl.plot(results[:,3])
#pl.legend(['token f-score', 'boundary f-score'], loc=6)
#pl.show()

# Unigram 6t tfidf, 8 progressing bits
#token_f-score   token_precision token_recall    boundary_f-score        boundary_precision      boundary_recall
#0.6308  0.5897  0.6781  0.8051  0.7386  0.8848
#token_f-score   token_precision token_recall    boundary_f-score        boundary_precision      boundary_recall
#0.632   0.5808  0.6931  0.8119  0.7307  0.9134
#token_f-score   token_precision token_recall    boundary_f-score        boundary_precision      boundary_recall
#0.5976  0.5441  0.6628  0.7933  0.7068  0.904
#token_f-score   token_precision token_recall    boundary_f-score        boundary_precision      boundary_recall
#0.5929  0.547   0.6471  0.7988  0.724   0.8907
#token_f-score   token_precision token_recall    boundary_f-score        boundary_precision      boundary_recall
#0.615   0.561   0.6805  0.81    0.7246  0.9183
#token_f-score   token_precision token_recall    boundary_f-score        boundary_precision      boundary_recall
#0.646   0.6019  0.6971  0.8262  0.758   0.9078
#token_f-score   token_precision token_recall    boundary_f-score        boundary_precision      boundary_recall
#0.6215  0.5632  0.6933  0.8121  0.7215  0.9288
#token_f-score   token_precision token_recall    boundary_f-score        boundary_precision      boundary_recall
#0.6211  0.5672  0.6863  0.8162  0.732   0.9223

# Unigram 6t tfidf, 8 progressing bits, adapted twice
# 10 iter
#token_f-score   token_precision token_recall    boundary_f-score        boundary_precision      boundary_recall
#0.5997  0.5482  0.6619  0.7856  0.7011  0.8932
#token_f-score   token_precision token_recall    boundary_f-score        boundary_precision      boundary_recall
#0.5441  0.4837  0.6219  0.7681  0.6645  0.91
#token_f-score   token_precision token_recall    boundary_f-score        boundary_precision      boundary_recall
#0.5494  0.486   0.6317  0.7655  0.6594  0.9123
#token_f-score   token_precision token_recall    boundary_f-score        boundary_precision      boundary_recall
#0.5927  0.5421  0.6538  0.794   0.7122  0.8969
#token_f-score   token_precision token_recall    boundary_f-score        boundary_precision      boundary_recall
#0.5338  0.476   0.6074  0.767   0.6683  0.8998
#token_f-score   token_precision token_recall    boundary_f-score        boundary_precision      boundary_recall
#0.5123  0.4462  0.6014  0.752   0.6382  0.9151
#token_f-score   token_precision token_recall    boundary_f-score        boundary_precision      boundary_recall
#0.5422  0.4806  0.622   0.7666  0.6639  0.9069
#token_f-score   token_precision token_recall    boundary_f-score        boundary_precision      boundary_recall
#0.5939  0.5421  0.6568  0.7993  0.7163  0.904
#################
# 50 iter
#token_f-score   token_precision token_recall    boundary_f-score        boundary_precision      boundary_recall
#0.6158  0.5752  0.6626  0.7932  0.727   0.8727
#token_f-score   token_precision token_recall    boundary_f-score        boundary_precision      boundary_recall
#0.5932  0.541   0.6565  0.7913  0.7057  0.9004
#token_f-score   token_precision token_recall    boundary_f-score        boundary_precision      boundary_recall
#0.5947  0.538   0.6648  0.7963  0.7041  0.9164
#token_f-score   token_precision token_recall    boundary_f-score        boundary_precision      boundary_recall
#0.5902  0.5247  0.6743  0.798   0.6926  0.9412
#token_f-score   token_precision token_recall    boundary_f-score        boundary_precision      boundary_recall
#0.615   0.561   0.6805  0.81    0.7246  0.9183
#token_f-score   token_precision token_recall    boundary_f-score        boundary_precision      boundary_recall
#0.646   0.6019  0.6971  0.8262  0.758   0.9078
#token_f-score   token_precision token_recall    boundary_f-score        boundary_precision      boundary_recall
#0.6215  0.5632  0.6933  0.8121  0.7215  0.9288
#token_f-score   token_precision token_recall    boundary_f-score        boundary_precision      boundary_recall



results = np.array([[0.63,0.63,0.62,0.61,0.60,0.59,0.58,0.57], # unigrams
                    #[0.65,0.65,0.64,0.62,0.61,0.60,0.59,0.58], # unigrams
                    #[0.77,0.75,0.72,0.68,0.65,0.63,0.62,0.61] # colloc syll
                    [0.6308,0.632,0.5976,0.5929,0.615,0.646,0.6215,0.6211], # uni 6t
                    [0.6158,0.5932,0.5947,0.5902,0.615,0.646,0.6215,0.6213], # uni 6t + adapted twice
                    ])

import matplotlib.pyplot as plt

fig = plt.figure(figsize=(12, 9), dpi=300)
#plt.xticks([11, 12, 13, 14.5, 16, 17.5, 19, 20.5, 22])
plt.xticks(xrange(8))
#plt.yticks([])
ax = plt.gca()
ax.set_ylim([0.54,0.71])
ax.set_xlim([-0.1,7.1])
ax.set_xticklabels(map(str, [11, 13, 14.5, 16, 17.5, 19, 20.5, 22]))
plt.plot(results[0], 'o--', linewidth=3.5)#, alpha=0.8)
plt.plot(results[1], 'o--', linewidth=3.5)#, alpha=0.8)
plt.plot(results[2], 'o--', linewidth=3.5)#, alpha=0.8)
plt.xlabel('~ months')
plt.ylabel('token f-score')
plt.legend(["Unigram", "Uni 6t", "Uni 6t +readapt"])
    
plt.savefig('progress.png')
