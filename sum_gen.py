from key_ex import *
import util

class SummaryMDP(util.MDP):
    def __init__(self, keywords):
        self.keywords = keywords

    # Return the start state
    # (empty string, remaining keywords)
    def startState(self):
        return ("", self.keywords)

    # Return the set of actions possible from state
    def actions(self, state):
        pass

# extract_keys returns map of pos to words
def generate_summary(text, wordCounts, wikiCounts):
    keywords = extract_keys(text, wordCounts, wikiCounts)
    nouns = sorted(keywords['NOUN'])
    verbs = sorted(keywords['VERB'])
    adjs = sorted(keywords['ADJ'])
    print nouns[-10:]
    print verbs[-10:]
    print adjs[-10:]
    result = ''

    return result
