import random
import tldrlib
from process_data import *
from key_ex import *
from sum_gen import *

#TODO: read input args


data, wordCounts = get_data()

#split data into training and test data sets
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
# wordCounts = getWordCounts(data)
w = learn_key_extractor(trainingData, testData, tldrlib.keywordFeatureExtractor, 5, 0.01, wordCounts)
print w

for k in testDataKeys:
    text = data[k][0][0][0]
    print k
    print generate_summary(text, wordCounts)
    print
