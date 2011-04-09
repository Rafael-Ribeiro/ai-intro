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

figure(0)
plot(x, yLL, x, yLR)

figure(1)
plot(x, yRL, x, yRR)
show()
