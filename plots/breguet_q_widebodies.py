import math
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import spline

def get_range(V, C, L_D, W_1, W_2):
    return (V / C) * L_D * math.log(float(W_1) / W_2)

def get_weight_ratio(V, C, L_D, distance):
    return math.exp(distance * C / (V * L_D))

def project_segment(theta, c):
    theta = math.radians(theta)
    return c * math.cos(theta), c * math.sin(theta)

def get_hookoff(alpha, trunk, cross, W_1, model):
    
    Q_list     = np.arange(0, 1, .01)
    fuel_list  = []

    for Q in Q_list:
    
        # The distance from the hub to the hookoff point
        a = Q * trunk
        
        # The distance from the hookoff point to the destination
        b = math.sqrt((trunk-a)**2 + cross**2)
        
        formation_fuel = (1 - alpha) * get_fuel_burned_during_cruise(a, W_1, model)
        solo_fuel      = get_fuel_burned_during_cruise(b, W_1 - formation_fuel, model)
        fuel           = formation_fuel + solo_fuel
        
        fuel_list.append(fuel)
    
    fuel_opt = min(fuel_list)
    Q_opt = Q_list[fuel_list.index(fuel_opt)]
    
    return (Q_list, Q_opt, fuel_list, fuel_opt)

def get_fuel_burned_during_cruise(distance, W_1, model):
    
    V   = model['V']
    c_L = model['c_L']
    L_D = model['L_D']
    
    return W_1 * (1 - 1 / get_weight_ratio(V, c_L, L_D, distance))

def run():
    
    alpha              = .13 # Formation discount
    hub_to_destination = 1500 # distance in NM
    trunk_deviation    = 4 # degrees
    W_1                = 297550 - 14000 # B777 Maxweight at start of cruise
    
    font = {'family' : 'sans-serif',
            'weight' : 'normal',
            'size'   : 12}
    
    models = [{
        'name' : 'B772',
        'V'    : 500,
        'c_L'  : .6,
        'L_D'  : 19.26
    },{
        'name' : 'A333',
        'V'    : 500,
        'c_L'  : .4,
        'L_D'  : 10
    }]

    matplotlib.rc('font', **font)
    matplotlib.rc('mathtext', default='sf')
    
    # Split the segment hub-destination up into a trunk segment and a
    # cross segment
    (trunk, cross) = project_segment(trunk_deviation, hub_to_destination)
    
    for model in models:
    
        x = []
        y = []
        for alpha in np.arange(0, 1, .005):
            
            (Q_list, Q_opt, fuel_list, fuel_opt) =\
            get_hookoff(alpha, trunk, cross, W_1, model)
            
            x.append(alpha)
            y.append(Q_opt)
        
        plt.plot(x, y, label = model['name'])
        plt.legend(loc=(0.05, 0.05))
        plt.xlabel(r'$\alpha$')
        plt.ylabel(r'$Q$')
        plt.title(
            r'$Q_{opt}$ against $\alpha$ using Breguet Fuel Estimation'
        )
    plt.show()
    
    
    
    
    
    
    
    
    
    
    
    
    
    