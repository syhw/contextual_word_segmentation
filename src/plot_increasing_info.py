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
pl.plot(results[:,0])
pl.plot(results[:,3])
pl.legend(['token f-score', 'boundary f-score'], loc=6)
pl.show()

