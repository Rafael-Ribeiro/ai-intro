#!/usr/bin/python

from pylab import *

import sys
sys.path.append("../../../src") 

from custom.functions import *

#Simulation constants
VELOCITY = 5.0 			# Natural velocity

# Senses factors
LIGHT_BIAS = 2.0
SMELL_BIAS = 4.0
SOUND_BIAS = 5.0
PROXIMITY_BIAS = 2.0

NATURAL = 2.0
C = 0.2
CSOUND = 0.3

x = arange(0, 1, 0.01)
y_prox_l = map(lambda x: cut(x, 0, C, (C-x)*PROXIMITY_BIAS, 0.5, -NATURAL-1), x)
y_prox_r = map(lambda x: cut(x, 0, C, (C-x)*PROXIMITY_BIAS, 0.5, -NATURAL+1), x)

y_light_l = map(lambda x: cut(x, 0, C, (C-x)*LIGHT_BIAS, 0.5, -NATURAL-1), x)
y_light_r = map(lambda x: cut(x, 0, C, (C-x)*LIGHT_BIAS, 0.5, -NATURAL+1), x)

y_smell_l = map(lambda x: cut(x, 0, C, (x-C)*SMELL_BIAS), x)
y_smell_r = map(lambda x: cut(x, 0, C, (x-C)*SMELL_BIAS), x)

y_sound_l = map(lambda x: cut(x, 0, CSOUND, (x-CSOUND)*SOUND_BIAS), x)
y_sound_r = map(lambda x: cut(x, 0, CSOUND, (x-CSOUND)*SOUND_BIAS), x)


figure(0)
plot(x, y_prox_l, x, y_light_l, x, y_smell_l, x, y_sound_l)
axis([0,1,-4,4])

figure(1)
plot(x, y_prox_r, x, y_light_r, x, y_smell_r, x, y_sound_r)
axis([0,1,-4,4])

show()
