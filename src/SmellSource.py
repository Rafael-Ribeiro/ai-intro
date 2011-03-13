#!/usr/bin/env python
# -*- coding: utf-8 -*-

class SmellSource(breve.Mobile):

	def __init__(self):
		breve.Mobile.__init__(self)
		SmellSource.init(self)

	def init(self):
		self.setShape(breve.createInstances(breve.Sphere,1).initWith(0.300000))
		self.setColor(breve.vector(1,0,0))

breve.SmellSource = SmellSource
