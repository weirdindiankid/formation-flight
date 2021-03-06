import math

import matplotlib.pyplot as plt
import numpy as np

def breguet(discount = 0):
    
    V   = 500
    c_T = .56
    d   = 3000
    L_D = 17
    
    return 1-math.exp(-(1 - discount)*d*c_T/(V*L_D))

for drag_discount in np.arange(0,1,.01):
    fuel_discount = 1 - breguet(drag_discount)/breguet()
    print '%.2f leads to %.4f' % (drag_discount, fuel_discount)