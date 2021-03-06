#!/usr/bin/env python
"""Simulation bootstrapper"""

from formation_flight.formation import handlers as formation_handlers
from formation_flight.aircraft import handlers as aircraft_handlers
from formation_flight.aircraft import generators
from formation_flight.hub import builders
from formation_flight.hub import allocators

from lib import sim, debug, sink
from lib.debug import print_line as p

from formation_flight import statistics
from formation_flight import calibrate

import config, os, copy

# Deze werkte goed (P=0.3 gaf hogere abs savings dan P=0)
#config.alpha      = .25
#config.etah_slack = 5
#config.lock_time  = 20
#config.phi_max    = 5
#config.count_hubs = 1
#config.Z          = .25
#config.dt         = 30

config.etah_slack = 7
config.phi_max    = 10
config.dt         = 15

config.alpha      = .25
config.lock_time  = 20
config.count_hubs = 1
config.Z          = .25

config.sink_dir = '%s/sink' % os.path.dirname(__file__)

def execute():
    
    sink.init(config.sink_dir)

    # Construct flight list (for aircraft lookup)
    planes = generators.get_via_stdin()
    
    runs = 10
    
    for i in xrange(1, runs + 1):
        # Construct flight list once more for the sim runs
        # Very little performance drawback due to caching
        single_run(generators.get_via_stdin())
        print 'Completed run %d of %d...' % (i, runs)
        #print calibrate.vars

    rows = []
    for label, value in calibrate.vars.items():
        # Lookup of aircraft belonging to key
        plane = next((a for a in planes if a.label == label), None)
        rows.append([
            plane.departure_time_scheduled,
            label,
            '%s-%s' % (plane.origin, plane.destination),
            plane.aircraft_type,
            '%.2f' % value
        ])
    sink.dump_rows(rows)
    #for row in rows:
    #    print row

def single_run(planes):
    
    sim.init()
    aircraft_handlers.init()
    formation_handlers.init()
    statistics.init()
    calibrate.init()
    
    # Find hubs
    config.hubs = builders.build_hubs(planes, config.count_hubs, config.Z)
    
    # Allocate hubs to flights
    allocators.allocate(planes, config.hubs)
    
    for flight in planes:
        sim.events.append(sim.Event('aircraft-init', flight, 0))
    
    sim.run()

def plot():
    
    import plot
    plot.run()
    















