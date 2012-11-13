"""Models contain information and do not initiate actions or commands."""
from lib.debug import print_line as p
from lib.geo.route import Route

class Aircraft(object):
    """An individual flight."""

    def __init__(self, label = None, route = None,
                 departure_time = 0, aircraft_type = None):

        self.label = label if label is not None else str(route)
        self.route = route
        self.waypoints_passed = []
        self.description = str(route)
        self.departure_time = departure_time
        self.aircraft_type = aircraft_type
        self.origin = self.route.waypoints[0]
        self.destination = self.route.waypoints[-1]
        # Distance units per time unit (500 kts)
        self.speed = 500/60

    def depart(self):
        """Sets the current position and increments to the first waypoint."""
        self.position = self.route.waypoints[0]
        self.waypoints_passed.append(self.position)
        del self.route.waypoints[0]
        del self.route.segments[0]

    def at_waypoint(self):
        """Sets the current position and increments to the next segment."""
        self.position = self.route.waypoints[0]
        self.waypoints_passed.append(self.position)
        del self.route.waypoints[0]
        del self.route.segments[0]
        
    def arrive(self):
        """Placeholder for the aircraft's arrival."""
        self.position = self.route.waypoints[0]
        self.waypoints_passed.append(self.position)
        del self.route.waypoints[0]

    def time_to_waypoint(self):
        """Calculates the time left to fly to the current waypoint."""
        waypoint = self.route.waypoints[0]
        distance = self.position.distance_to(waypoint)
        return distance / self.speed

    def __repr__(self):
        return '%s (%s, t=%d)' % (self.label, self.aircraft_type, self.departure_time)
    
