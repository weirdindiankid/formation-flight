#!/usr/bin/env python
"""Simulation bootstrapper"""

from formation_flight.formation import handlers as formation_handlers
from formation_flight.aircraft import handlers as aircraft_handlers
from formation_flight.aircraft import generators
from formation_flight.hub import builders
from formation_flight.hub import allocators
from formation_flight import visualization
from lib.util import make_sure_path_exists

import matplotlib

from lib import sim, debug, sink
from lib.debug import print_line as p

from formation_flight import statistics

from lib.geo.segment import Segment
from lib.geo.route import Route

import config
import os
import numpy as np

from .. import run
from ..europe.run import create_segments

# Use this for the pre calib run
#config.count_hubs = 1
#config.min_P = 0
#config.dt = 0
#config.Z = 0.25
#config.phi_max = 45
#config.etah_slack = 30

# Use this for the post-calib run
config.count_hubs = 1
config.min_P = 0.95
config.dt = 30
config.Z = 0.25
config.phi_max = 5
config.etah_slack = 10

config.map_dimensions = {
    'lat' : [ 0., 70.],
    'lon' : [-130., 40.]
}

config.map = {
    'parallels' : np.arange(0, 90, 20),
    'meridians' : np.arange(-180, 180, 45)
}

config.sink_dir = '%s/sink' % os.path.dirname(__file__)

font = {'size' : 20}
matplotlib.rc('font', **font)

def execute():

    planes = run.single_run()
    
    segments = create_segments(planes)

    plt, ax = run.render(segments)

    name = str(config.min_P).replace('.','_')
    fig_path = '%s/plot_%s.pdf' % (config.sink_dir, name)
    fig_path = fig_path.replace('/runs/', '/plots/')
    fig_path = fig_path.replace('/sink/', '/')

    make_sure_path_exists(os.path.dirname(fig_path))
    
    plt.savefig(fig_path, bbox_inches='tight')
    #plt.show()
