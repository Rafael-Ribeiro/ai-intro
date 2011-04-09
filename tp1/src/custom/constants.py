#!/usr/bin/python
# -*- coding: utf-8 -*-

import breve

class direction:
	FRONT = breve.vector(1,0,0)
	LEFT = breve.vector(0,0,-1)
	RIGHT = breve.vector(0,0,1)
	BACK = breve.vector(-1,0,0)
	UP = breve.vector(0,1,0)

class color:
	RED = breve.vector(1,0,0)
	GREEN = breve.vector(0,1,0)
	BLACK = breve.vector(0,0,0)
	PINK = breve.vector(1, 0.6, 1)
	EGG = breve.vector(1,1,0.6)
	WHITE = breve.vector(1,1,1)

