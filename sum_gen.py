from key_ex import *

def generate_summary(text, wordCounts):
    candidates = extract_keys(text, wordCounts)
    result = ''
    for ck in candidates.keys():
        result += ck + ' ' +  max(candidates[ck])[1] + '  '
    return result
