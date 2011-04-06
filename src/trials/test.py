#!/usr/bin/python

from pylab import *

import sys
sys.path.append("../") 

from custom.functions import cut

x = arange(0, 1, 0.01)
y = map (lambda x: cut(x, 1-x, 0.8, 2), x)   

fig = figure()
plot(x, y)
show()
