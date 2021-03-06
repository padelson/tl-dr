from key_ex import *

def generate_summary(text, wordCounts, wikiCounts):
    candidates = extract_keys(text, wordCounts, wikiCounts)
    result = ''
    for ck in candidates.keys():
        # print sorted(candidates[ck])
        result += ck + ' ' +  str(max(candidates[ck])) + '  '
    return result
