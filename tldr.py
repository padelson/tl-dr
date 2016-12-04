#!/usr/bin/python
import tldrlib
import util
import process_data
from tldrlib import *
from util import *
from process_data import *

print "learning"

process_data(1000)
data = get_data(10000)
w = learnPredictor(trainingData, trainingData, keywordFeatureExtractor, 100, 0.001)

print w
