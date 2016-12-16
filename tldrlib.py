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

def removePuncation (word):
    index1 = 0;
    for i in range(len(word)):
        if word[i].isalnum():
            index1 = i
            break
    index2 = 0
    for i in range(len(word)-1, 0-1, -1):
        if word[i].isalnum():
            index2 = i
            break
    return word[index1:index2+1]


def keywordFeatureExtractor(x, wordCounts, wikiCounts):
    phi = {}
    article = x[0]
    testWord = x[1]
    pos = x[2]

    # location, count
    count = 0
    wordCount = len(article.split())
    for i, wordPunc in enumerate(article.split()):
        word = removePuncation(wordPunc)
        if word == testWord:
            count += 1
            frac = roundToFraction(i, wordCount, 3)
            phi["location"+str(frac)] = 1
                #phi["term freq " + str(count)] = 1
    phi["term freq > 5 < 20"] = 1 if count < 20 and count > 5 else 0
    phi["term freq/5 "+ str(count/5)] = 1
    phi["all letter "] = 1 if testWord.isalpha() else 0
    phi['term freq'] = count / 10
    phi['1'] = 1
    phi["term length / 50 = " + str(wordCount / 50)] = 1
    phi["word is in first 50"] = 1 if testWord in article.split()[:50] else 0
    phi["word is in first & last 50"] = 1 if testWord in article.split()[-50:] and testWord in article.split()[:50] else 0
    phi["word freq in first 100"] = len([testWord for word in article.split()[:100] if word == testWord])

    # length
    length = len(testWord)
    # phi["length < 4"] = 1 if length < 4 else 0
    phi["word length / 5 = " + str(length / 5)] = 1
    # isCapital
    phi["isCapital"] = 1 if testWord[0].title() in article else 0
    phi["isCapital freq"] = count if phi["isCapital"] else 0
    phi["isCapital freq > 2"] = 1 if phi["isCapital"] and count > 2 else 0
    phi["isCapital freq > 3"] = 1 if phi["isCapital"] and count > 3 else 0
    phi["isCapital freq > 4"] = 1 if phi["isCapital"] and count > 4 else 0
    phi["isCapital and all letter"] = 1 if testWord[0].isupper() and testWord.isalpha() else 0
    phi["capitalized noun"] = 1 if pos == "NOUN" and testWord[0].isupper() else 0

    # phi["pos: " + pos] = 1

    # if wordCounts[testWord] > 0:
    #     phi['tf-idf'] = float(count) / wordCounts[testWord]

    if wikiCounts[testWord] > 0:
        phi["wiki count / 1000: " + str(wikiCounts[testWord] / 1000)] = 1
        phi["wiki count"] = wikiCounts[testWord] / 1000

    #TODO: occurs in first sentence
    #TODO: occurs in first sentence + what is your frequency?

    firstSentence = article.split('.')[0]
    phi["occurs in first sentence"] = 1 if testWord in firstSentence.lower() else 0
    occursFirstSentence = 0
    if testWord in firstSentence.lower():
        occursFirstSentence = article.split().count(testWord)
    phi["occurs in first sentence + count"] = occursFirstSentence
    phi["occurs in first sentence + count"] = occursFirstSentence

    phi["bias"] = 1

    return phi


### sanity check
#sanity = "This sentence needs to to to than ten words long"
#for w in sanity.split():
#    print keywordFeatureExtractor((sanity, w))
#print roundToTenth(1, 10) # -> expecting 2/10
#print roundToTenth(420, 2000) # -> expecting 2/10
