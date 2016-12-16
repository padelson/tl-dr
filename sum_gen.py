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
    top_keywords = nouns[-10:] + verbs[-10:] + adjs[-10:]
    #mdp = SummaryMDP(top_keywords)
    #result = ''
    return top_keywords
