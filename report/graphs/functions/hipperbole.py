#!/usr/bin/python

from pylab import *

import sys
sys.path.append("../../../src") 

from custom.functions import *

MED = 0.5
DEV = 0.1

x = arange(0, 4, 0.01)
y = map(lambda x: hiperbole(x), x)

fig = figure()
plot(x, y)
axis([0.0, 4, 0, 6])
show()
