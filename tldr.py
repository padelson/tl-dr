#!/usr/bin/python
import tldrlib
import util
import process_data
import random
import collections
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

def getScore(word, featureExtractor, weights):
	return dotProduct(weights, featureExtractor(word))

def generateSummary(dataKeys, data, w):
	for dk in dataKeys:
		candidates = collections.defaultdict(list)
		for entry in data[dk]:
			score = getScore(entry[0], keywordFeatureExtractor, w)
			candidates[entry[0][2]].append((score, entry[0][1]))
		print 'title: ' + dk
		for ck in candidates.keys():
			print ck, max(candidates[ck])
		print ''

print "learning"

data = get_data()
keys = data.keys()
random.shuffle(keys)
testDataKeys = keys[:len(keys)/10]
trainingDataKeys = keys[len(testDataKeys)+1:]
trainingData = []
testData = []
for k in trainingDataKeys:
	trainingData += data[k]
for k in testDataKeys:
	testData += data[k]

# dumbassPredictor(onesTestData)
w = learnPredictor(trainingData, testData, keywordFeatureExtractor, 1, 0.01)
print w

generateSummary(trainingDataKeys, data, w)
