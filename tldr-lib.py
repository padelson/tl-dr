#!/usr/bin/python

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
    """
    Extract word features for a string x. Words are delimited by whitespace characters only.
    """
    # BEGIN_YOUR_CODE (our solution is 4 lines of code, but don't worry if you deviate from this)
    d = {}
    wordcount = len(x.split())
    for i, word in enumerate(x.split()):
        # location in text
        d[(word, "location" + str(roundToFraction(i, wordcount, 10)))] = 1
        # count
        d[(word, "count")] = 1 if word not in d else d[word] + 1
        # length
        d[(word, "length", len(word))] = 1
        # isCapital
        d[(word, "isCapital")] = 1 if word[0].isupper() else 0
        # part of speech
    return d
    # END_YOUR_CODE


### sanity check
#sanity = "This sentence needs to be greater than ten words long"
#print keywordFeatureExtractor(sanity)
#print roundToTenth(1, 10) # -> expecting 2/10
#print roundToTenth(420, 2000) # -> expecting 2/10
