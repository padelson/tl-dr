from key_ex import *

def generate_summary(text):
    candidates = extract_keys(text)
    result = ''
    for ck in candidates.keys():
        result += ck + ' ' +  max(candidates[ck])[1] + '  '
    return result
