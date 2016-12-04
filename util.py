#!/usr/bin/python

import os, random, operator, sys
from collections import Counter

##################################################################################################
# Algorithm
##################################################################################################
### stochastic gradient descent
### classify if a word is relevant or not
def learnPredictor(trainExamples, testExamples, featureExtractor, numIters, eta, wordCounts, wikiCounts):
    '''
    Given |trainExamples| and |testExamples| (each one is a list of (x,y)
    pairs), a |featureExtractor| to apply to x, and the number of iterations to
    train |numIters|, the step size |eta|, return the weight vector (sparse
    feature vector) learned.
    '''
    weights = {}  # feature => weight
    def Loss(x, y, w):
        # return (dotProduct(w, featureExtractor(x, wordCounts, wikiCounts)) - y) ** 2
        return max(0, 1 - dotProduct(w, featureExtractor(x, wordCounts, wikiCounts)) * y)

    def Predictor(x):
        return 1 if dotProduct(weights, featureExtractor(x, wordCounts, wikiCounts)) > 0 else -1

    for i in range(numIters):
        for x, y in trainExamples:
            if Loss(x, y, weights) != 0:
                increment(weights, eta * y, featureExtractor(x, wordCounts, wikiCounts))
            # print weights
            # print Predictor(x), y
        print 'Iteration ' + str(i)
        print 'Training Error: ' + str(evaluatePredictor(trainExamples, Predictor))
        print 'Test Error: ' + str(evaluatePredictor(testExamples, Predictor))
        print ''

    # END_YOUR_CODE
    return weights

###################################################################################################
# API (from sentiment/util.py)
###################################################################################################
def dotProduct(d1, d2):
    """
    @param dict d1: a feature vector represented by a mapping from a feature (string) to a weight (float).
    @param dict d2: same as d1
    @return float: the dot product between d1 and d2
    """
    if len(d1) < len(d2):
        return dotProduct(d2, d1)
    else:
        return sum(d1.get(f, 0) * v for f, v in d2.items())

def increment(d1, scale, d2):
    """
    Implements d1 += scale * d2 for sparse vectors.
    @param dict d1: the feature vector which is mutated.
    @param float scale
    @param dict d2: a feature vector.
    """
    for f, v in d2.items():
        d1[f] = d1.get(f, 0) + v * scale

def readExamples(path):
    '''
    Reads a set of training examples.
    '''
    examples = []
    for line in open(path):
        # Format of each line: <output label (+1 or -1)> <input sentence>
        y, x = line.split(' ', 1)
        examples.append((x.strip(), int(y)))
    print 'Read %d examples from %s' % (len(examples), path)
    return examples

def evaluatePredictor(examples, predictor):
    '''
    predictor: a function that takes an x and returns a predicted y.
    Given a list of examples (x, y), makes predictions based on |predict| and returns the fraction
    of misclassiied examples.
    '''
    error = 0
    for x, y in examples:
        if predictor(x) != y:
            error += 1
    return 1.0 * error / len(examples)

def outputWeights(weights, path):
    print "%d weights" % len(weights)
    out = open(path, 'w')
    for f, v in sorted(weights.items(), key=lambda (f, v) : -v):
        print >>out, '\t'.join([f, str(v)])
    out.close()

def verbosePredict(phi, y, weights, out):
    yy = 1 if dotProduct(phi, weights) > 0 else -1
    if y:
        print >>out, 'Truth: %s, Prediction: %s [%s]' % (y, yy, 'CORRECT' if y == yy else 'WRONG')
    else:
        print >>out, 'Prediction:', yy
    for f, v in sorted(phi.items(), key=lambda (f, v) : -v * weights.get(f, 0)):
        w = weights.get(f, 0)
        print >>out, "%-30s%s * %s = %s" % (f, v, w, v * w)
    return yy

def outputErrorAnalysis(examples, featureExtractor, weights, path):
    out = open('error-analysis', 'w')
    for x, y in examples:
        print >>out, '===', x
        verbosePredict(featureExtractor(x), y, weights, out)
    out.close()

def interactivePrompt(featureExtractor, weights):
    while True:
        print '> ',
        x = sys.stdin.readline()
        if not x: break
        phi = featureExtractor(x)
        verbosePredict(phi, None, weights, sys.stdout)

############################################################
