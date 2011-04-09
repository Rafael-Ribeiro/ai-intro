#!/usr/bin/python

from pylab import *

import sys
sys.path.append("../../../src") 

from custom.functions import *

MATURITY 		= 50.0
PROCRIATION 	= 40.0
LIFESPAN 		= 300.0
VELOCITY 		= 3.0
NATURAL			= 2.0

HALF_DISTANCE = 3
HALF_LIGHT = 7.0
HALF_SOUND = 7.0

DISTANCE_BIAS = 2.0
LIGHT_BIAS = 4.0
SOUND_BIAS = 8.0

DISTANCE_CUT	= 0.2
LIGHT_CUT		= DISTANCE_CUT
SOUND_CUT		= DISTANCE_CUT
x = arange(0, 1, 0.01)

y_prox_l = map(lambda x: cut(x, 0, DISTANCE_CUT, (DISTANCE_CUT - x) * DISTANCE_BIAS, 0.5, -NATURAL + 1), x)
y_prox_r = map(lambda x: cut(x, 0, DISTANCE_CUT, (DISTANCE_CUT - x) * DISTANCE_BIAS, 0.5, -NATURAL - 1), x)

y_light_l = map(lambda x: cut(x, 0, LIGHT_CUT, (LIGHT_CUT - x) * LIGHT_BIAS), x)
y_light_r = map(lambda x: cut(x, 0, LIGHT_CUT, (LIGHT_CUT - x) * LIGHT_BIAS), x)

y_sound_l = map(lambda x: cut(x, 0, SOUND_CUT, (SOUND_CUT - x) * SOUND_BIAS), x)
y_sound_r = map(lambda x: cut(x, 0, SOUND_CUT, (SOUND_CUT - x) * SOUND_BIAS), x)

figure(0)
plot(x, y_prox_l, x, y_light_l, x, y_sound_l)

figure(1)
plot(x, y_prox_r, x, y_light_r, x, y_sound_r)

show()
