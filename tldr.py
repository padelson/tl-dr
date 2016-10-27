#!/usr/bin/python
import tldrlib
import util
import process_data
import random
from tldrlib import *
from util import *
from process_data import *

print "learning"

data = get_data()
random.shuffle(data)
testData = data[:len(data)/10]
trainingData = data[len(testData)+1:]
testData = [d for d in data if d[1] == 1]
print [d[1] for d in testData]
# testData = random.sample(data, len(data)/10)
# trainingData = [d for d in data if d not in testData]
print 'datasets separated'
w = learnPredictor(trainingData, testData, keywordFeatureExtractor, 10, 0.01)

print w
