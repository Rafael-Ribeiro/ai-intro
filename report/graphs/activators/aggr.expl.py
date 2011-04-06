#!/usr/bin/python

from pylab import *

import sys
sys.path.append("../../../src") 

from custom.functions import *

x = arange(0, 1, 0.01)

OFF = gaussian(0,0.25,0.1)
y = map(lambda x: cut(x, (gaussian(x, 0.25, 0.1)-OFF)/2, 0.5, -(1-x*2)**2), x)

yleft = map(lambda x: cut(x, 1-x*2, 0.5, -1), x)
yright = map(lambda x: cut(x, 1-x*2, 0.5, 1), x)

figure(0)
plot(x, y, x, yleft)
axis([0.0, 1, -1.2, 1.2])

figure(1)
plot(x, y, x, yright)
axis([0.0, 1, -1.2, 1.2])

show()
