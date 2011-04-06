#!/usr/bin/python

from pylab import *
import mpl_toolkits.mplot3d.axes3d as p3

x = arange(-100, 100, 0.5)
y = arange(-100, 100, 0.5)

X,Y = meshgrid(x,y)

# BIAS = distance from source in the 0x axis where Intensity @ Sensor = 0.5*Intensity @ Source 
BIAS = 50
DIST = sqrt(X*X + Y*Y)
ANGLE = angle(X + Y*1j)
Z = 0.5*((1+cos(ANGLE))/(DIST/BIAS+1))

fig = figure()
pcolor(X,Y,Z)
colorbar()
show()
