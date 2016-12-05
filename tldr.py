import random
import tldrlib
from process_data import *
from key_ex import *
from sum_gen import *

#TODO: read input args


data, wordCounts, wikiCounts = get_data()

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


w = learn_key_extractor(trainingData, testData, tldrlib.keywordFeatureExtractor, 15, 0.0001, wordCounts, wikiCounts)
print w

articles = getArticlesDict()


for k in testDataKeys:
    text = articles[k]
    print k
    print generate_summary(text, wordCounts, wikiCounts)
    print
