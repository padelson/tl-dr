import mdputil, math, random
from collections import defaultdict
from mdputil import ValueIteration


class headlineMDP(mdputil.MDP):
    def __init__(self, nouns, verbs, adjs):
        self.nouns = nouns
        self.verbs = verbs
        self.adjs = adjs

    def startState(self):
        return ("", "" , 0)

    def actions(self, state):
        actions = []
        if state[2] == 0:
            for adjT in self.adjs:
                adj = adjT[0]
                for nounT in self.nouns:
                    noun = nounT[0]
                    if noun != "" and noun != adj:
                        actions.append((adj, noun))
        elif state[2] == 1:
            for verbT in self.verbs:
                verb = verbT[0]
                if verb != "" and verb not in state[1]:
                    actions.append( (verb, "") )
    
        elif state[2] ==2:
            for adjT in self.adjs:
                adj = adjT[0]
                if adj == "" or adj not in state[1]:
                    for nounT in self.nouns:
                        noun = nounT[0]
                        if (noun == "" or noun not in state[1]) and noun != adj:
                            actions.append((adj, noun))
        if len(actions) == 0:
            actions.append( ("", ""))                  
        return actions


    def succAndProbReward(self, state, action):
        
        
        def evalFunction(string):
            
            def find(string, n):
                if n == 1:
                    for i in range(0, len(self.adjs)):
                        if self.adjs[i][0] == string:
                            return self.adjs[i][1]
                elif n ==2:
                    for i in range(0, len(self.nouns)):
                        if self.nouns[i][0] == string:
                            return self.nouns[i][1]
                else:
                    for i in range(0, len(self.verbs)):
                        if self.verbs[i][0] == string:
                            return self.verbs[i][1]
            
            
            headline = string.split(" ")
            length =  0
            for i in range(0, len(headline)):
                if headline[i] != "":
                    length +=1
            return  (2*find(headline[0],1) + 4*find(headline[1],2) + find(headline[2],3) + find(headline[3],1) + 2*find(headline[4],2))/length
        

        list = []
        
        if state[2] == 0:
            if action[1] == "":
                return list
            headline = action[0]+ " "+ action[1]
            newState = (headline, action[0]+ action[1], 1)
            
            list.append( (newState, 1, 0))
        elif state[2] == 1:
            if action[0] =="":
                return list
            headline = state[0] + " "+action[0]
            newState = (headline, state[1]+action[0], 2)
            list.append( (newState, 1, 0))
        elif state[2] == 2:
            headline = state[0]+ " "+ action[0]+ " "+action[1]
            newState = (headline, state[1], 3)
            list.append((newState, 1, 0))
        elif state[2] == 3:
            headline = state[0]
            newState = (headline, state[1], 4)
            list.append((newState, 1, evalFunction(headline)))

        return list

    def discount(self):
        return 1



