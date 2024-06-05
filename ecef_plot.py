#!/usr/bin/env python3

#%% 


# Simple script to plot ECEF coordinates

import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 3.429742e+06 -5.846064e+06 6.042774e+04

%matplotlib widget

def plot_pos(pos_file, title=None, plot_earth=False):
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_title(title)
    
    if plot_earth:
        # Plot earth
        # https://medium.com/@Romain.p/plot-satellites-real-time-orbits-with-python-s-matplotlib-3c7ccd737638
        r = 6370000
        u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
        ax.plot_wireframe(r*np.cos(u)*np.sin(v),r*np.sin(u)*np.sin(v),r*np.cos(v),color="g",alpha=0.5,lw=0.5,zorder=0)

    # Read coordinates from space delimited text file
    data = np.genfromtxt(pos_file, delimiter=' ')

    # Plot
    ax.plot(data[:,0], data[:,1], data[:,2])

    # Plot first and last point
    # ax.scatter(data[1,0], data[1,1], data[1,2], c='r')
    # ax.scatter(data[-1,0], data[-1,1], data[-1,2], c='orange')


    plt.show()

plot_pos('testsc/PosW.42', title='ECEF Coordinates', plot_earth=True)
plot_pos('testsc/PosN.42', title='ECI Coordinates' , plot_earth=True)




# %%
