#!/usr/bin/python
import tldrlib
import util
import process_data
from tldrlib import *
from util import *
from process_data import *

print "learning"

trainingData = get_data(10000)
w = learnPredictor(trainingData, trainingData, keywordFeatureExtractor, 100, 0.001)

print w
