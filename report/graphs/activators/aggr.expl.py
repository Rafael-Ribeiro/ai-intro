#!/usr/bin/python

from pylab import *

import sys
sys.path.append("../../../src") 

from custom.functions import *

def gauss(x, med, dev):
	return exp(-(x-med)**2/(2*dev**2))

OFF = gaussian(0,0.25,0.1)

x = arange(0, 1, 0.01)
X,Y = meshgrid(x,x)

y = map(lambda x: cut(x, (gaussian(x, 0.25, 0.1)-OFF)/2, 0.5, -(1-x*2)**2), x)

yleft = map(lambda x: cut(x, 1-x*2, 0.5, -1), x)
yright = map(lambda x: cut(x, 1-x*2, 0.5, 1), x)

A = (gauss(X, 0.25, 0.1)-OFF)*(X < 0.5)+(-(1-X*2)**2)*(X >= 0.5)

ZL = A + (1-Y*2)*(X<0.5)+(X>=0.5)*(-1)
ZR = A + (1-Y*2)*(X<0.5)+(X>=0.5)

figure(0)
subplot(2,1,1)
plot(x, y, x, yleft)
axis([0.0, 1, -1.2, 1.2])


subplot(2,1,2)
pcolor(X,Y,ZL)
colorbar()

figure(1)
subplot(2,1,1)
plot(x, y, x, yright)
axis([0.0, 1, -1.2, 1.2])

subplot(2,1,2)
pcolor(X,Y,ZR)
colorbar()

show()
