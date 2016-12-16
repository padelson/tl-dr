import random
import tldrlib
import process_data
import key_ex
import sum_gen
import argparse
import sys
import os.path

#TODO: caching of weight vector
#TODO: create small dataset from rss.py?

def setup_argparse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', type=int, default=-1, help='number of articles to learn on')
    parser.add_argument('-a', type=str, default='all', choices=['key', 'sum', 'base', 'oracle'])
    parser.add_argument('-f', type=str, help='filepath to desired text')
    return parser

def learn(n):
    data, wordCounts, wikiCounts = process_data.get_data()

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

    w = key_ex.learn_key_extractor(trainingData, testData, tldrlib.keywordFeatureExtractor, 15, 0.0001, wordCounts, wikiCounts)
    print w

    articles = process_data.getArticlesDict()


    for k in testDataKeys:
        text = articles[k]
        print k
        print sum_gen.generate_summary(text, wordCounts, wikiCounts)
        print

parser = setup_argparse()
args = parser.parse_args()

# if not os.path.isfile('processed_data.txt') or args.n != -1:
process_data.process_data(args.n)

if args.a == 'all':
    learn(args.n)

elif args.a == 'key':
    if not args.f:
        data, wordCounts, wikiCounts = process_data.get_data()
        articles = process_data.getArticlesDict()
        for key in articles:
            print key_ex.extract_keys(articles[key], wordCounts, wikiCounts)
    else:
        wikiCounts = process_data.getWikiCounts()
        f = open(args.f, 'r')
        text = f.read()
        f.close()
        print key_ex.extract_keys(text, {}, wikiCounts)

elif args.a == 'sum':
    if not args.f:
        data, wordCounts, wikiCounts = process_data.get_data()
        articles = process_data.getArticlesDict()
        for key in articles:
            print sum_gen.generate_summary(articles[key], wordCounts, wikiCounts)
    else:
        wikiCounts = process_data.getWikiCounts()
        f = open(args.f, 'r')
        text = f.read()
        f.close()
        print sum_gen.generate_summary(text, {}, wikiCounts)

elif args.a == 'base':
    data, wordCounts, wikiCounts = process_data.get_data()
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
    key_ex.dumbass_predictor(trainingData)

elif args.a == 'oracle':
    print 'not implemented yet'
    sys.exit()

else:
    sys.exit()
