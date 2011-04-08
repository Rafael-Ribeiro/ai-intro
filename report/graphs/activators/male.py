#!/usr/bin/python

from pylab import *

import sys
sys.path.append("../../../src") 

from custom.functions import *

MATURITY 		= 60.0
PROCRIATION 	= 30.0
LIFESPAN 		= 250.0
VELOCITY 		= 4.0
NATURAL			= 2.0
CURVING_FACTOR	= 25

HALF_DISTANCE = 3
HALF_LIGHT = 14.0
HALF_SMELL = 30.0
HALF_SOUND = 7.0

DISTANCE_BIAS = 1.0
LIGHT_BIAS = 5.0
SMELL_BIAS = 2.0
SOUND_BIAS = 9.0

DISTANCE_CUT	= 0.2
LIGHT_CUT		= DISTANCE_CUT
SMELL_CUT		= DISTANCE_CUT
SOUND_CUT		= DISTANCE_CUT

x = arange(0, 1, 0.01)

y_prox_l = map(lambda x: cut(x, 0, DISTANCE_CUT, (DISTANCE_CUT - x) * DISTANCE_BIAS, 0.5, -NATURAL + 1), x)
y_prox_r = map(lambda x: cut(x, 0, DISTANCE_CUT, (DISTANCE_CUT - x) * DISTANCE_BIAS, 0.5, -NATURAL - 1), x)

y_light_l = map(lambda x: cut(x, 0, LIGHT_CUT, (LIGHT_CUT - x) * LIGHT_BIAS), x)
y_light_r = map(lambda x: cut(x, 0, LIGHT_CUT, (LIGHT_CUT - x) * LIGHT_BIAS), x)

y_sound_l = map(lambda x: cut(x, 0, SOUND_CUT, (x - SOUND_CUT) * SOUND_BIAS), x)
y_sound_r = map(lambda x: cut(x, 0, SOUND_CUT, (x - SOUND_CUT) * SOUND_BIAS - 0.1), x)


s_diff = arange(-0.1, 0.1, 0.001)
s_sum = arange(0, 2.0, 0.001)

SOUND = -2
D, S = meshgrid(s_diff, s_sum)
smell = (D*CURVING_FACTOR) + (S>0.2)*(abs(D)/((S+0.000000001)/2.0) < 0.05)*(-SOUND+1)


figure(0)
plot(x, y_prox_l, x, y_light_l, x, y_sound_l)
#axis([0,1,-4,4])

figure(1)
plot(x, y_prox_r, x, y_light_r, x, y_sound_r)
#axis([0,1,-4,4])

figure(2)
pcolor(D,S,smell)
colorbar()

show()
