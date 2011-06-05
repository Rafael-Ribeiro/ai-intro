#!/usr/bin/python

from math import *
from matplotlib.pyplot import figure

data1 = ['Even - 15 points', 'red', []]
data2 = ['Even - 30 points', 'green', []]
data3 = ['Dynamic - 15 points', 'blue', []]
data4 = ['Dynamic - 30 points', 'black', []]
MAX_ITER = 2000
iterations = range(1, MAX_ITER+1)

figureHist = figure(figsize=(12.0, 6.0), dpi=72)
graphHist = figureHist.add_subplot(111)
graphHist.plot(iterations, data1[2][:MAX_ITER+1], data1[1], iterations, data2[2][:MAX_ITER+1], data2[1], iterations, data3[2][:MAX_ITER+1], data3[1], iterations, data4[2][:MAX_ITER+1], data4[1])
graphHist.legend( (data1[0], data2[0], data3[0], data4[0]), loc='upper right')
figureHist.savefig('evolution.png' , format="png", transparent=True)
figureHist.clf()
