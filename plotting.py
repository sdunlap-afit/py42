#!/usr/bin/env python3

#%% Simple script to plot ECEF coordinates

import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial.transform import Rotation

%matplotlib widget
plt.rcParams["figure.figsize"] = (8, 8)


def plot_earth(ax):
    # https://medium.com/@Romain.p/plot-satellites-real-time-orbits-with-python-s-matplotlib-3c7ccd737638
    r = 6370000
    u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
    ax.plot_wireframe(r*np.cos(u)*np.sin(v),r*np.sin(u)*np.sin(v),r*np.cos(v),color="g",alpha=0.5,lw=0.5,zorder=0)


def plot_pos(ax, pos):
    '''Plot position'''

    # Plot
    ax.plot(pos[:,0], pos[:,1], pos[:,2])

    # Plot first and last point
    ax.scatter(pos[1,0], pos[1,1], pos[1,2], c='r')
    ax.scatter(pos[-1,0], pos[-1,1], pos[-1,2], c='orange')



def plot_vel(ax, vel, pos):
    '''Plot velocity vector at position'''
    
    # Plot velocity vector at position
    for i in range(0, len(vel), 10):
        ax.quiver(pos[i,0], pos[i,1], pos[i,2], vel[i,0], vel[i,1], vel[i,2], length=1e6, normalize=True, color='r')



def plot_quat(ax, qbn, posN):
    '''Plot attitude vector at position'''
    
    # Plot attitude vector at position
    for i in range(0, len(qbn), 5):
        # Rotate vector
        vs = [  Rotation.from_quat(qbn[i]).apply([1, 0, 0]),
                Rotation.from_quat(qbn[i]).apply([0, 1, 0]),
                Rotation.from_quat(qbn[i]).apply([0, 0, 1])]

        for v, c in zip(vs, ['r', 'g', 'b']):
            ax.quiver(posN[i,0], posN[i,1], posN[i,2], v[0], v[1], v[2], length=0.5e6, normalize=True, color=c)



DATA_DIR = 'testsc'

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_title('ECI Coordinates')
ax.set_xlabel('X (m)')
ax.set_ylabel('Y (m)')
ax.set_zlabel('Z (m)')

# Read coordinates from space delimited text file
posN = np.genfromtxt(os.path.join(DATA_DIR, 'PosN.42'), delimiter=' ')
velN = np.genfromtxt(os.path.join(DATA_DIR, 'VelN.42'), delimiter=' ')
qbn  = np.genfromtxt(os.path.join(DATA_DIR, 'qbn.42' ), delimiter=' ')

plot_earth(ax)
plot_pos(ax, posN)
# plot_vel(ax, velN, posN)
plot_quat(ax, qbn, posN)


# Adjust plot limits to be the same
max_range = np.array([posN.max(), posN.max(), posN.max()]).max()
ax.set_xlim(-max_range, max_range)
ax.set_ylim(-max_range, max_range)
ax.set_zlim(-max_range, max_range)


plt.show()


# %%
