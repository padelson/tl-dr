import mdputil, math, random
from collections import defaultdict
from mdputil import ValueIteration


class headlineMDP(mdputil.MDP):
    def __init__(self, nouns, verbs, adjs):
        self.nouns = nouns
        self.verbs = verbs
        self.adjs = adjs


    def startState(self):
        return ("", "", 0)

    def actions(self, state):
        list = []
        if state[2] == 0:
            for adjT in self.adjs:
                adj = adjT[0]
                for nounT in self.nouns:
                    noun = nounT[0]
                    if noun != "" and noun != adj:
                        list.append((adj, noun))
        elif state[2] ==1:
            for verbT in self.verbs:
                verb = verbT[0]
                if verb not in state[1]:
                    list.append( (verb, "") )
    
        elif state[2] ==2:
            for adjT in self.adjs:
                adj = adjT[0]
                if adj == "" or adj not in state[1]:
                    for nounT in self.nouns:
                        noun = nounT[0]
                        if (noun == "" or noun not in state[1]) and noun != adj:
                            list.append((adj, noun))
        else:
            list.append( ("",""))
                                    
        return list


    def succAndProbReward(self, state, action):
        def evalFunction(string):
            headline = string.split(" ")
            return self.adjs[headline[0]] +2*self.nouns[headline[1]]  + self.verbs[headline[2]]  + self.adjs[headline[3]] + self.nouns[headline[4]]

        list = []
        if state[2] == 0:
            headline = action[0]+ " "+ action[1]
            newState = (headline, action[0], action[1], 1)
            
            list.append( (newState, 1, 0))
        elif state[2] ==1:
            headline = state[0] + " "+action[0]
            newState = (headline, state[1]+action[0], 2)
            list.append( (newState, 1, 0))
        elif state[2] == 2:
            headline = state[0]+ " "+ action[0]+ " "+action[1]
            newState = (headline, state[1], 3)
            list.append((newState, 1, evalFunction(headline)))

        return list

    def discount(self):
        return 1



