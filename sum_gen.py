from key_ex import *

def generate_summary(text, wordCounts, wikiCounts):
    candidates = extract_keys(text, wordCounts, wikiCounts)
    result = ''
    for ck in candidates.keys():
        keys = sorted(candidates[ck])
        keys.reverse()
        print keys[:10]
        result += ck + ' ' +  str(max(candidates[ck])) + '  '
    return result
