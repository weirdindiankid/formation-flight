#!/usr/bin/env python

import random

from formation_flight.formation.handlers import FormationHandler
from formation_flight.formation.allocators import *
from formation_flight.formation.synchronizers import *
from formation_flight.aircraft.handlers import AircraftHandler
from formation_flight.aircraft.models import Aircraft
from formation_flight.formation.models import Formation
from lib.geo.route import Route
from lib.geo.waypoint import Waypoint
from lib import sim, debug

aircraft_handler   = AircraftHandler()
formation_handler  = FormationHandler(
    allocator    = FormationAllocatorEtah,
    synchronizer = FormationSynchronizer
)

# Generate a list of random flights
origins      = ['AMS', 'CDG', 'LHR', 'FRA', 'DUS', 'BRU']
destinations = ['EWR', 'JFK', 'ORD', 'LAX', 'SFO']
hubs         = ['MAN']#, 'LHR']
planes       = []

for i in range(0, 500):
    planes.append(Aircraft(
        label = 'FLT%03d' % i,
        route = Route([
            Waypoint(random.choice(origins)), 
            Waypoint(random.choice(hubs)), 
            Waypoint(random.choice(destinations))
        ]),
        departure_time = random.choice(range(0, 440))))

# Override auto-planes, useful when reproducing a bug...
#planes = [
#    Aircraft('FLT001', Route([Waypoint('DUS'), Waypoint('MAN'),
#        Waypoint('JFK')]), 0),
#    Aircraft('FLT002', Route([Waypoint('FRA'), Waypoint('MAN'),
#        Waypoint('JFK')]), 0),
#    Aircraft('FLT003', Route([Waypoint('BRU'), Waypoint('MAN'),
#        Waypoint('LAX')]), 1),
#    Aircraft('FLT004', Route([Waypoint('BRU'), Waypoint('MAN'),
#        Waypoint('ORD')]), 2),
#    Aircraft('FLT005', Route([Waypoint('DUS'), Waypoint('MAN'),
#        Waypoint('JFK')]), 3),
#]
  
def run():
    for aircraft in planes:
        sim.events.append(sim.Event(
            'aircraft-depart', 
            aircraft, 
            aircraft.departure_time
        ))

    sim.run()

# docs: http://docs.python.org/library/profile.html
import cProfile, pstats
profile_file = 'data/profile.txt'
cProfile.run('run()', profile_file)
p = pstats.Stats(profile_file)
p.strip_dirs()
#p.sort_stats('cumulative')
p.sort_stats('time')
p.print_stats(30)
