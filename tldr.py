#!/usr/bin/python
import tldrlib
import util
import process_data
import random
from tldrlib import *
from util import *
from process_data import *


def dumbassPredictor(data):
	error = 0
	for d in data:
		firstSentence = d[0][0].split('.')[0]
		prediction = None
		if d[0][1] in firstSentence:
			prediction = 1
		else:
			prediction = -1
		if prediction != d[1]:
			error +=1
	print '\n\nnumWrong, numDataPoints, error'
	print error, len(data), error/float(len(data))


print "learning"

data = get_data()
random.shuffle(data)
testData = data[:len(data)/10]
trainingData = data[len(testData)+1:]
testData = [d for d in data if d[1] == 1]
print 'currently using test data of all keywords'
# testData = random.sample(data, len(data)/10)
# trainingData = [d for d in data if d not in testData]
print 'datasets separated'
dumbassPredictor(data)
# w = learnPredictor(trainingData, testData, keywordFeatureExtractor, 10, 0.01)

# print w

