import math
from lib.debug import print_line as p

class Earth(object):

    # 6371.00 in km, 3440.07 in NM
    # always make sure this is a float!!!
    R = 3440.07

class Point(object):

    """Represents a point on earth. Lat/lon in decimal degrees."""

    def __init__(self, lat, lon, name = 'Point'):
        self.lat = lat
        self.lon = lon
        if name == 'Point':
            self.name = '{%.2f, %.2f}' % (self.lat, self.lon)
        else:
            self.name = name

    def distance_to(self, point):
        R = Earth.R
        lat1 = math.radians(self.lat)
        lat2 = math.radians(point.lat)
        lon1 = math.radians(self.lon)
        lon2 = math.radians(point.lon)
        param = \
            math.sin(lat1)*math.sin(lat2)+\
            math.cos(lat1)*math.cos(lat2)*\
            math.cos(lon2-lon1)

        # Reduce precision to avoid 1.00000000000000034734 being out of domain
        param = float('%.6f' % param)

        d = math.acos(param)*R
        
        p('validate', 'Distance between %s and %s is %.2f NM' % (
            self, point, d
        ))
        
        return d

    def bearing_to(self, point):
        lat1 = math.radians(self.lat)
        lat2 = math.radians(point.lat)
        lon1 = math.radians(self.lon)
        lon2 = math.radians(point.lon)
        dLon = lon2 - lon1
        y = math.sin(dLon) * math.cos(lat2)
        x = math.cos(lat1)*math.sin(lat2) - math.sin(lat1)*\
                                            math.cos(lat2)*\
                                            math.cos(dLon)
        return math.degrees(math.atan2(y, x)) % 360
    
    def coincides(self, point):
        if point is self:
            return True
        if self.lat == point.lat and self.lon == point.lon:
            return True
        return False

    def get_position(self, bearing, distance):
        """
        Calculate destination given bearing and distance from start.
        """

        R = Earth.R
        d = distance/R

        theta = math.radians(bearing)

        lat1 = math.radians(self.lat)
        lon1 = math.radians(self.lon)

        part1 = math.cos(d) * math.sin(lat1)
        part2 = math.cos(theta) * math.cos(lat1) * math.sin(d)
        lat2  = math.asin(part1 + part2)

        part3 = math.sin(theta) * math.sin(d) * math.cos(lat1)
        part4 = math.cos(d) - math.sin(lat1) * math.sin(lat2)
        lon2  = lon1 + math.atan2(part3, part4)

        # Normalize between -pi and pi
        lon2  = lon2 - 2 * math.pi * math.floor((lon2 + math.pi) / (2 * math.pi))

        # Calculate the end bearing of the aircraft...
        y = math.sin(lon1 - lon2) * math.cos(lat1)
        x = math.cos(lat2) * math.sin(lat1) - math.sin(lat2) *\
                                              math.cos(lat1) *\
                                              math.cos(lon1 - lon2)
        new_bearing = (math.degrees(math.atan2(y, x)) + 180) % 360
        new_position = Point(math.degrees(lat2), math.degrees(lon2))
        #
        #p('validate',
        #    'Getting position. Start: %s, distance: %s, bearing: %s. '\
        #    'Result: %s' % (
        #        self, distance, bearing, new_position
        #    )
        #)

        return Position(new_position.lat, new_position.lon, new_bearing)

    def __repr__(self):
        #return "%s(%r)" % (self.__class__, self.__dict__)
        return '%s' % self.name

class Position(Point):
    """
    Represents a point with a bearing. Used to denote an aircraft's position.
    """

    def __init__(self, lat, lon, bearing):
        super(Position, self).__init__(lat, lon, 'Position')
        self.bearing = bearing
        self.name = '{%.2f, %.2f}' % (self.lat, self.lon)

    def __repr__(self):
        #return "%r" % (self.__dict__)
        #return '{%.2f, %.2f}' % (self.lat, self.lon)
        return self.name