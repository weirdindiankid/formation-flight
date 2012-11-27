import math
from point import Point

from lib.debug import print_line as p

def cross_track_distance(d_13, theta_13, theta_12):
    """Calculate distance from great circle path (1 -> 2) to point (3).

    Adapted from http://www.movable-type.co.uk/scripts/latlong.html

    This implementation does not produce a great-circle distance but a mere
    straight-line (through the earth) distance. We don't need anything more
    complicated for our purposes of comparison.

    d_13:     Distance from origin to third point (any distance measure)
    theta_13: Initial bearing from origin to third point (degrees)
    theta_12: Initial bearing from origin to destination (degrees)
    """
    R = 3440
    return math.asin( math.sin (d_13 / R) *\
                      math.sin (math.radians (theta_13 - theta_12))) * R

def midpoint(points):
    """Calculate an average destination based on a planar average (=bad)

    @todo Replace with vectorized version (most accurate solution)
    """

    sum_lat = sum((point.weight if hasattr(point, 'weight') else 1) * point.lat for point in points)
    sum_lon = sum((point.weight if hasattr(point, 'weight') else 1) * point.lon for point in points)
    count = sum((point.weight if hasattr(point, 'weight') else 1) for point in points)
    
    return Point(sum_lat / count, sum_lon / count)

def reduce_points(points):
    """Reduces the input list of points to unique points.
    
    Points are given "weights" for each time they appear in the input list."""
    
    # Reset the points from any previous calls
    for point in points:
        try:
            del point.weight
        except AttributeError:
            pass
    
    ret = []
    for point in points:
        for point_other in ret:
            # If the point is already in our return list
            if point_other.coincides(point):
                point.weight = point_other.weight + 1
                
        # Only add our point if no weight was set
        if not hasattr(point, 'weight'):
            point.weight = 1
            ret.append(point)
    return ret

def point_in_points(point, points):
    """Returns True if the point exists/coincides with any point in the list."""
    for p in points:
        if p.coincides(point):
            return True
    return False

def project_segment(theta, c):
    """Given the angle between lines AB and AC, and given a distance c of AC,
    return the distance a of AB and b of BC.
    
      A
      |\
    a | \ c
      |  \
      B---C
        b

    This implementation does not produce a great-circle distance but a mere
    straight-line (through the earth) distance. We don't need anything more
    complicated for our purposes of comparison.

    float theta: Angle between AB and AC (in degrees)
    float c:     Distance AC.
    """
    theta = math.radians(theta)
    return c * math.cos(theta), c * math.sin(theta)

def get_costs(a, b, alpha, beta):
    """Given a triangle ABC (with B being rectangular), return the cost to
       fly in formation from A to B', and solo from B' to C, where B' is a
       point on AB and is uniquely defined by the angle between BC and B'C.
       
       A
       |\
       | \
       |  \
       B'  \
       |    \
       B-----C
       
       float a:     distance from A to B
       float b:     distance from B to C
       float alpha: angle between BC and B'C (in degrees)
       float beta:  discount factor when flying in formation (0 < beta < 1)
    """
    alpha = math.radians(alpha)
    
    # Alpha cannot be larger than the angle between BC and AC.
    alpha_max = math.acos(b / math.sqrt(math.pow(a, 2) + math.pow(b, 2)));
    
    if alpha > alpha_max:
        raise Exception('alpha = %.2f exceeds the allowed value of %.2f' %\
                        (math.degrees(alpha), math.degrees(alpha_max)))
    
    return a - (1-beta)*b*math.tan(alpha) + b/math.cos(alpha)

def get_hookoff_quotient(a, b, beta):
    """Given a triangle AB'C (with B being rectangular), where AB' is a
       formation trajectory, and B'C is a solo trajectory. Find the hookoff
       point that minimizes fuel burn (using the discount factor beta), and
       return the quotient Q = AB' / AB.
       
       For performance, alpha (angle between BC and B'C) has 5 deg increments.
       
       A
       |\
       | \
       |  \
       B'  \
       |    \
       B-----C
       
       float a:     distance from A to B
       float b:     distance from B to C
       float beta:  discount factor when flying in formation (0 < beta < 1)
    """
    alpha_list = range(0, 90, 5)
    
    costs_list = []
    min_cost = None
    min_alpha = 0
    for alpha in alpha_list:
        try:
            costs = get_costs(a, b, float(alpha), beta)
            if min_cost is None:
                min_cost = costs
            elif min_cost > costs:
                min_cost = costs
            else:
                min_alpha = alpha
                break
            #print 'beta =% 5.2f\talpha =% 5.2f\t%.2f' % (beta, alpha, costs)
        # we have reached the maximum allowable angle between BC and B'C
        except Exception:
            break
    return (a - b*math.tan(math.radians(min_alpha))) / a

if __name__ == "__main__":

    print cross_track_distance (34, 237, 187)