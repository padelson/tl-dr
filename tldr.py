#!/usr/bin/python
import tldrlib
import util
import process_data
from tldrlib import *
from util import *
from process_data import *

print "learning"
print getData(100)

trainingData = getData(1)
w = learnPredictor(trainingData, keywordFeatureExtractor, 1, 0.0001)
print w
