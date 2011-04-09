#!/usr/bin/python

from pylab import *

import sys
sys.path.append("../../../src") 

from custom.functions import *

DISTANCE = 20.0
RADIUS = 13.0
VELOCITY = 5.0
ANGULAR_FREQUENCY = VELOCITY / RADIUS

AXIS_DIST = 4.0
OFFSET = 0.6
DIFFERENTIAL = ANGULAR_FREQUENCY * AXIS_DIST

x = arange(-1, 1, 0.1)
x2 = arange(0, RADIUS+DISTANCE, 1)

yleft = map(lambda x: VELOCITY, x2)

y1 = map(lambda x: cut(x, OFFSET, 0, 0), x)
y2 = map(lambda x: cut(x, DIFFERENTIAL, RADIUS*2, 0)+VELOCITY, x2)

figure(0)
plot(x2, yleft)
axis([0.0, RADIUS+DISTANCE, 0, 6])

figure(1)
subplot(2,1,1)
plot(x2, y2)
axis([0.0, RADIUS+DISTANCE, 0, 7])

subplot(2,1,2)
plot(x, y1)
axis([-1, 1, -0.1, 0.7])


show()
