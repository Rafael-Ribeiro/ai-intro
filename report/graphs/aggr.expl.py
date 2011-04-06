#!/usr/bin/python

from pylab import *

import sys
sys.path.append("../../src") 

from custom.functions import *

x = arange(0, 1, 0.01)
#y = map (lambda x: cut(x, 1-x, 0.8, 2), x)   
y = map(lambda x: cut(x, x*2, 0.4, 0.8-(x-0.4)*8, 0.5, 1-x*2), x)

fig = figure()
plot(x, y)
axis([0.0, 1, -1.2, 1.2])
show()
