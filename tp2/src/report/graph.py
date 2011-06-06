#!/usr/bin/python

from math import *
from matplotlib.pyplot import figure
START = 0
MAX_ITER = 100
iterations = range(START+1, MAX_ITER+1)

f = open('graphlines.py', 'r')
data = eval(f.read())
f.close()

figureHist = figure(figsize=(6.0, 4.0), dpi=72)
graphHist = figureHist.add_subplot(111)
graphHist.plot(iterations, data[0][2][START:MAX_ITER], data[0][1], iterations, data[1][2][START:MAX_ITER], data[1][1], iterations, data[2][2][START:MAX_ITER], data[2][1],  iterations, data[3][2][START:MAX_ITER], data[3][1])
graphHist.legend( (data[0][0], data[1][0], data[2][0], data[3][0]), loc='upper right')
figureHist.savefig('burst.png' , format="png", transparent=True)
figureHist.clf()
