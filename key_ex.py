import collections
import json
import tldrlib
import util
from process_data import *

def learn_key_extractor(trainingData, testData, keywordFeatureExtractor, numIters, eta, wordCounts, wikiCounts):
    w = util.learnPredictor(trainingData, testData, keywordFeatureExtractor, numIters, eta, wordCounts, wikiCounts)
    f = open('key_extractor_weights.txt', 'w')
    f.write(str(json.dumps(w)))
    f.close()
    return w

def extract_keys(text, wordCounts, wikiCounts):
    f = open('key_extractor_weights.txt', 'r')
    w = json.loads(f.readline())
    f.close()
    data = get_data_entries(text)
    candidates = collections.defaultdict(list)
    for entry in data:
        features, word, pos = entry
        score = tldrlib.getScore(entry, tldrlib.keywordFeatureExtractor, w, wordCounts, wikiCounts)
        candidates[pos].append((score,word))
    return candidates

def extract_keys1(path):
    f = open(path, 'r')
    text = f.read()
    f.close()
    return extrat_keys(text)

def dumbass_predictor(data):
    error = 0
    for d in data:
        firstSentence = d[0][0]["word is in first 200"]
        prediction = None
        if firstSentence == 1:
            prediction = 1
        else:
            prediction = -1
        if prediction != d[1]:
            error +=1
    print '\n\nnumWrong, numDataPoints, error'
    print error, len(data), error/float(len(data))
