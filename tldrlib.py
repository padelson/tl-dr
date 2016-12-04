#!/usr/bin/python
import nltk
import util

def getScore(entry, featureExtractor, weights, wordCounts, wikiCounts):
	return util.dotProduct(weights, featureExtractor(entry, wordCounts, wikiCounts))

# for now, here is what makes a word a keyword
# locations in the text
# count
# length
# capitalization
# part of speech*
def roundToFraction(num, denom, frac):
    sector = float(denom) / frac
    return int(num / sector)

def keywordFeatureExtractor(x, wordCounts, wikiCounts):
    phi = {}
    article = x[0]
    testWord = x[1]
    pos = x[2]

    # location, count
    count = 0
    wordCount = len(article.split())
    for i, word in enumerate(article.split()):
        if word == testWord:
            count += 1
            frac = roundToFraction(i, wordCount, 3)
            phi["location"+str(frac)] = 1
    phi["term freq / 10 = " + str(count / 10)] = 1

    phi["term length / 100 = " + str(wordCount / 100)] = 1

    phi["word is in first 100"] = 1 if testWord in article.split()[:100] else 0

    # length
    length = len(testWord)
    # phi["length < 4"] = 1 if length < 4 else 0
    phi["word length / 5 = " + str(length / 5)] = 1
    # isCapital
    phi["isCapital"] = 1 if testWord[0].isupper() else 0

    phi["pos: " + pos] = 1

    if wordCounts[testWord] > 0:
        phi['tf-idf'] = float(count) / wordCounts[testWord]

    if wikiCounts[testWord] > 0:
        phi["wiki count / 1000: " + str(wikiCounts[testWord] / 1000)] = 1

    return phi


### sanity check
#sanity = "This sentence needs to to to than ten words long"
#for w in sanity.split():
#    print keywordFeatureExtractor((sanity, w))
#print roundToTenth(1, 10) # -> expecting 2/10
#print roundToTenth(420, 2000) # -> expecting 2/10
