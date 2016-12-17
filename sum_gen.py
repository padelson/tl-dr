from key_ex import *
import mdp, nltk
from tldrlib import removePunctuation
from nltk.stem import WordNetLemmatizer as lemma

# headline is of form "ADJ NOUN VERB ADJ NOUN"
def polish(text, headline):
    polished = headline.split()[0].capitalize()
    capital = {word:0 for word in headline.split()[1:]}
    for word in text.split():
        word = removePunctuation(word)
        for string in headline.split()[1:]:
            if string.lower == word.lower():
                capital[string] += 1 if word[0].isupper() else -1
    for string in headline.split()[1:]:
        word = string.capitalize() if capital[string] > 0 else string.lower()
        polished += " " + word

    #polished = ' '.join([capital(word,i,text) for i,word in enumerate(headline.split())])
    return "\"" + polished + "\""

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
def getSentences(text):
    global tokenizer
    tokens = tokenizer.tokenize(text)
    sentences = []
    for sentence in tokens:
        words = [removePunctuation(word) for word in sentence.split()]
        sentences.append(' '.join(words))
    return sentences

def generate_summary(text, wordCounts, wikiCounts):
    candidates = extract_keys(text, wordCounts, wikiCounts)
    result = ''
    verbs = []
    adjs = []
    nouns = []
    for ck in candidates.keys():
        ckSorted =  sorted(candidates[ck])
        ckSorted.reverse()
        #result += ck + ' ' + str(ckSorted)
        vals = [val[0] for val in ckSorted]
        avg = sum(vals)/float(len(vals))
        if (ck == "VERB"):
        	for i in range(0, 3):
        		if i < len(ckSorted):
        			verbs.append( (ckSorted[i][1], ckSorted[i][0]- avg) )
        	verbs.append( ("", 0) )
        if (ck == "NOUN"):
        	for i in range(0, 7):
        		if i < len(ckSorted):
        			nouns.append( (ckSorted[i][1], ckSorted[i][0] -avg) )
        	nouns.append( ("", 0) )
       	if (ck == "ADJ"):
        	for i in range(0, 5):
        		if i < len(ckSorted):
        			adjs.append( (ckSorted[i][1], ckSorted[i][0]- avg) )
        	adjs.append( ("", 0) )
        #result += ck + ' ' +  str(max(candidates[ck])) + '  '

    content = getSentences(text)
    mdpH = mdp.headlineMDP(nouns = nouns, adjs = adjs, verbs = verbs, content = content)
    vi = mdp.ValueIteration()
    vi.solve(mdpH)
    curr = mdpH.startState()
    best = 0
    headline = ""

    print "Finding best headine..."
    while True:
    	action = vi.pi[curr]
    	nextProbRew = mdpH.succAndProbReward(curr, action )
    	if nextProbRew[0][2] >0:
    		headline = curr[0]
    		best = nextProbRew[0][2]
    		break
    	curr = nextProbRew[0][0]
    return polish(text, headline)

def generate_summary2(text, wordCounts, wikiCounts):
    candidates = extract_keys(text, wordCounts, wikiCounts)
    result = ''
    for ck in candidates.keys():
        keys = sorted(candidates[ck])
        keys.reverse()
        print keys[:10]
        result += ck + ' ' +  str(max(candidates[ck])) + '  '
    return result
