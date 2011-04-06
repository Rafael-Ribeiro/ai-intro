#!/usr/bin/python

from pylab import *

import sys
sys.path.append("../../../src") 

from custom.functions import *

ANGULAR = 0.5
AXIS_DIST = 4.0
RADIUS = 10.0

x = arange(0, RADIUS, 0.1)

yLL = map(lambda x: RADIUS*ANGULAR*x, x)
yLR = map(lambda x: (RADIUS+AXIS_DIST)*ANGULAR*x, x)

yRL = map(lambda x: (RADIUS+AXIS_DIST)*ANGULAR*x, x)
yRR = map(lambda x: RADIUS*ANGULAR*x, x)

X,Y = meshgrid(x,x)
ZL = X*RADIUS*ANGULAR+Y*(RADIUS+AXIS_DIST)*ANGULAR
ZR = Y*RADIUS*ANGULAR+X*(RADIUS+AXIS_DIST)*ANGULAR


figure(0)
subplots_adjust(right=0.75)

subplot(2,1,1)
plot(x, yLL, x, yLR)

subplot(2,1,2)
pcolor(X,Y,ZL)
colorbar()

figure(1)
subplot(2,1,1)
plot(x, yRL, x, yRR)

subplot(2,1,2)
pcolor(X,Y,ZR)
colorbar()
show()
