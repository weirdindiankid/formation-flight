from ..benchmark import run
from lib import sink
import config
import os
import numpy as np
import math

from lib.geo.point import Point

config.sink_dir = '%s/sink' % os.path.dirname(__file__)
config.count_hubs = 3

def get_matrix_dimensions():
    
    nx = 5
    ny = 5
    
    return (nx, ny,)

def execute():
    
    nx, ny = get_matrix_dimensions()
    x_range = np.linspace(1, 30, nx)
    y_range = np.linspace(0.01, 25, ny)
    run.init()

    for x in x_range:

        config.etah_slack = x
    
        for y in y_range:

            config.phi_max = y
            run.single_run()