#!/usr/bin/python

from pylab import *
import mpl_toolkits.mplot3d.axes3d as p3

x = arange(-100, 100, 0.5)
y = arange(-100, 100, 0.5)

X,Y = meshgrid(x,y)

APPERTURE = 2.0
Z = (X >= 0.0) * (abs(Y) <= APPERTURE) * X

fig = figure()
pcolor(X,Y,Z)
colorbar()
show()
