#!/usr/bin/python
import nltk

# for now, here is what makes a word a keyword
# locations in the text
# count
# length
# capitalization
# part of speech*
def roundToFraction(num, denom, frac):
    sector = float(denom) / frac
    return int(num / sector)

def keywordFeatureExtractor(x):
    phi = {}
    article = x[0]
    testWord = x[1]

    # location, count
    count = 0
    wordCount = len(article.split())
    for i, word in enumerate(article.split()):
        if word == testWord:
            count += 1
            frac = roundToFraction(i, wordCount, 10)
            phi["location"+str(frac)] = 1
    # phi["count"] = count

    # length
    length = len(testWord)
    phi["length < 4"] = 1 if length < 4 else 0
    # isCapital
    phi["isCapital"] = 1 if testWord[0].isupper() else 0
    # TODO: pos

    return phi


### sanity check
#sanity = "This sentence needs to to to than ten words long"
#for w in sanity.split():
#    print keywordFeatureExtractor((sanity, w))
#print roundToTenth(1, 10) # -> expecting 2/10
#print roundToTenth(420, 2000) # -> expecting 2/10
