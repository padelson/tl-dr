from key_ex import *
import mdp
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
        if (ck == "NOUN"):
        	for i in range(0, 7):
        		if i < len(ckSorted):
        			nouns.append( (ckSorted[i][1], ckSorted[i][0] -avg) )
       	if (ck == "ADJ"):
        	for i in range(0, 5):
        		if i < len(ckSorted):
        			adjs.append( (ckSorted[i][1], ckSorted[i][0]- avg) )
        #result += ck + ' ' +  str(max(candidates[ck])) + '  '
    mdpH = mdp.headlineMDP(nouns = nouns, adjs = adjs, verbs = verbs)
    vi = mdp.ValueIteration()
    vi.solve(mdpH)
    headline = max(vi.V)
    return headline[0]

def generate_summary2(text, wordCounts, wikiCounts):
    candidates = extract_keys(text, wordCounts, wikiCounts)
    result = ''
    for ck in candidates.keys():
        keys = sorted(candidates[ck])
        keys.reverse()
        print keys[:10]
        result += ck + ' ' +  str(max(candidates[ck])) + '  '
    return result
