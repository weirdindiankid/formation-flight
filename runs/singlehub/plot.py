import os
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate
import math
from lib.util import make_sure_path_exists
from lib.util import tsv_get_column_index
from mpl_toolkits.basemap import Basemap
import config

config.sink_dir = '%s/sink' % os.path.dirname(__file__)

config.plots = [
    {
        'column' : 'formation_count',
        'title'  : r'Formation Count $M$',
        'levels' : np.arange(0, 30, 2),
    },{
        'column' : 'formation_success_rate',
        'title'  : r'Formation Success Rate $S_f$',
        'levels' : np.arange(0, 1.05, .05),
    },{
        'column' : 'avg_formation_size',
        'title'  : r'Average Formation Size $N_{avg}$',
        'levels' : 20,
    },{
        'column' : 'distance_success_rate',
        'title'  : r'Distance Success Rate $S_d$',
        'levels' : np.arange(0, 1.05, .05),
    },{
        'column' : 'fuel_saved',
        'title'  : r'Fuel Saved',
        'levels' : 20,
    },{
        'column' : 'distance_penalty',
        'title'  : r'Distance Penalty $P_d$',
        'levels' : 20,
    }
]

#config.output_var = 'distance_total'
#config.output_var = 'distance_formation'
#config.output_var = 'distance_solo'
#config.output_var = 'formation_count'
#config.output_var = 'formation_success_rate'
#config.output_var = 'alpha_eff'
#config.output_var = 'distance_success_rate'

#config.contour_levels = np.arange(.8, 1, .05)

#print data_file

def run():
    
    data_file = '%s/latest.tsv' % config.sink_dir
    
    data = np.loadtxt(
        open(data_file, 'rb'),
        delimiter = "\t",
        skiprows = 1
    )
    
    for plotconf in config.plots:
        do_plot(plotconf, data)
    
def do_plot(plotconf, data):
    
    plt.figure()
    
    column = plotconf['column']
    print 'Drawing plot for %s' % column
    
    data_file = '%s/latest.tsv' % config.sink_dir
    
    x = data[:, tsv_get_column_index(data_file, 'hub_lon')]
    y = data[:, tsv_get_column_index(data_file, 'hub_lat')]
    z = data[:, tsv_get_column_index(data_file, column)]
    
    minlat = np.min(y)
    maxlat = np.max(y)
    minlon = np.min(x)
    maxlon = np.max(x)
    
    m = Basemap(
        projection = 'merc', resolution = 'c',
        llcrnrlat = minlat, urcrnrlat = maxlat,
        llcrnrlon = minlon, urcrnrlon = maxlon
    )
    
    # Reverse Y-axis (high lat = low y)
    #y = y[::-1]
    
    #x, y = np.meshgrid(x, y)
    
    N = len(z)
    #print N
    nx = math.sqrt(N)
    ny = nx
    
    x = x.reshape(nx, ny)
    y = y.reshape(nx, ny)
    z = z.reshape(nx, ny)

    #print x
    #print y
    #print z
    
    m.drawcoastlines()
    m.drawstates()
    m.drawcountries()
    
    x, y = m(x, y)
    m.contourf(x, y, z, plotconf['levels'])
    
    plt.colorbar()
    plt.title(plotconf['title'])
    
    #plt.show()
    
    fig_path = '%s/plot_%s.pdf' % (config.sink_dir, column)
    fig_path = fig_path.replace('/runs/', '/plots/')
    fig_path = fig_path.replace('/sink/', '/')
    make_sure_path_exists(os.path.dirname(fig_path))
    plt.savefig(fig_path)
    