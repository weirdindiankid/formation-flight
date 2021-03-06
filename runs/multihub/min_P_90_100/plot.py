import config
from lib.util import tsv_get_column_index
import os

import numpy as np
import matplotlib.pyplot as plt

config.sink_dir = '%s/sink' % os.path.dirname(__file__)

def run():
    
    data_file = '%s/latest.tsv' % config.sink_dir
    
    data = np.loadtxt(
        open(data_file, 'rb'),
        delimiter = "\t",
        skiprows = 1
    )
    
    x = data[:, tsv_get_column_index(data_file, 'config_min_P')]
    y = data[:, tsv_get_column_index(data_file, 'fuel_saved')]
    
    plt.xlabel(r'Formation Suitability Criterium $C_{min}$')
    plt.ylabel(r'Fuel Saved $S_f$')
    
    plt.plot(x, y)
    plt.show()