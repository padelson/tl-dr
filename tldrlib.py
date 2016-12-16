#!/usr/bin/python
import nltk
import util
import re
import string

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

#########################################
# preprocess(str) -> string w/o punct   #
#########################################
def replaceApostrophe(body):
    body = body.replace("\xe2\x80\x98", "'") # \u2018
    body = body.replace("\xe2\x80\x99", "'") # \u2019
    return body

def replaceQuotation(body):
    body = body.replace("\xe2\x80\x9c",'"') # \u201c
    body = body.replace("\xe2\x80\x9d",'"') # \u201d
    return body

def removeDash(body):
    body = body.replace("\xe2\x80\x93","") # \u2013
    body = body.replace("\xe2\x80\x94","") # \u2014
    body = body.replace("\xe2\x80\x95","") # \u2015
    body = body.replace("\xe2\x80\xa6","") # \u2026 ellipses
    return body

def replaceWhiteSpace(body):
    body = body.replace("\xe2\x80\x89"," ") # \u2009
    body = body.replace("\xc2\xa0"," ") # \u00a0
    #body = body.replace("\\n", " ")
    return body

def convertToASCII(body):
	ascii_chars = [c for c in body if c in string.printable]
	return ''.join(ascii_chars)

def preprocess(body):
    body = replaceApostrophe(body)
    body = replaceQuotation(body)
    body = removeDash(body)
    body = replaceWhiteSpace(body)
    # maybe comment out?
    body = convertToASCII(body)
    return body
##########################################
"""
def removePunctuation(word):
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
"""
def removePunctuation(word):
    while not word[0].isalnum():
        word = word[1:]
    while not word[-1].isalnum():
        word = word[:-1]
    return word

def keywordFeatureExtractor(x, wordCounts, wikiCounts):
    phi = {}
    article = x[0]
    testWord = x[1]
    pos = x[2]

    # location, count
    count = 0
    wordCount = len(article.split())

    for i,word in enumerate(article.split()):
        word = removePunctuation(word)
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
    phi["isCapital"] = 1 if testWord[0].isupper() else 0
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
    return phi


### sanity check
#sanity = "This sentence needs to to to than ten words long"
#for w in sanity.split():
#    print keywordFeatureExtractor((sanity, w))
#print roundToTenth(1, 10) # -> expecting 2/10
#print roundToTenth(420, 2000) # -> expecting 2/10
