#!/usr/bin/python

from pylab import *

import sys
sys.path.append("../../src") 

from custom.functions import *

MED = 0.5
DEV = 0.1

x = arange(0, 1, 0.01)
#y = map (lambda x: cut(x, 1-x, 0.8, 2), x)   
y = map(lambda x: gaussian(x, MED, DEV), x)

fig = figure()
plot(x, y)
axis([0.0, 1, -0.2, 1.2])
show()
