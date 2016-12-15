import util, math, random
from collections import defaultdict
from util import ValueIteration

############################################################
# Problem 2a

# If you decide 2a is true, prove it in blackjack.pdf and put "return None" for
# the code blocks below.  If you decide that 2a is false, construct a counterexample.
class CounterexampleMDP(util.MDP):
    def startState(self):
        # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
        raise Exception("Not implemented yet")
        # END_YOUR_CODE

    # Return set of actions possible from |state|.
    def actions(self, state):
        # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
        raise Exception("Not implemented yet")
        # END_YOUR_CODE

    # Return a list of (newState, prob, reward) tuples corresponding to edges
    # coming out of |state|.
    def succAndProbReward(self, state, action):
        # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
        raise Exception("Not implemented yet")
        # END_YOUR_CODE

    def discount(self):
        # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
        raise Exception("Not implemented yet")
        # END_YOUR_CODE

############################################################
# Problem 3a

class headlineMDP(util.MDP):
    def __init__(self, nouns, verbs, adjs):
        self.nouns = nouns
        self.verbs = verbs
        self.adjs = adjs


    def startState(self):
        return ("", "", "", 0)

    def actions(self, state):
        list = []
        if state[3] == 0:
            for adj in self.adjs:
                for noun in self.nouns:
                    if noun != "":
                        list.append((adj, noun))
        elif state[3] ==1:
            for verb in self.verbs:
                list.append( (verb, "") )
    
        elif state[3] ==2:
            for adj in self.adjs:
                if adj == "" or adj != state[1]:
                    for noun in self.nouns:
                        if noun != state[2]:
                            list.append((adj, noun))
        elif state[3] == 3:
            list.append( ("",""))
                                    
        return list


    def succAndProbReward(self, state, action):
        def evalFunction(string):
            headline = string.split(" ")
            return self.adjs[headline[0]] +2*self.nouns[headline[1]]  + self.verbs[headline[2]]  + self.adjs[headline[3]] + self.nouns[headline[4]]

        list = []
        if state[3] == 0:
            headline = action[0]+ " "+action[1]
            newState = (headline, action[0], action[1], 1)
            list.append( (newState, 1, 0))
        elif state[3] ==1:
            headline = state[0] + " "+action[0]
            newState = (headline, state[1], state[2], 2)
            list.append( (newState, 1, 0))
        elif state[3] == 2:
            headline = state[0]+ " "+ action[0]+ " "+action[1]
            newState = (headline, state[1], state[2], 3)
            list.append((newState, 1, evalFunction(headline)))

        return list

    def discount(self):
        return 1

class BlackjackMDP(util.MDP):
    def __init__(self, cardValues, multiplicity, threshold, peekCost):
        """
        cardValues: array of card values for each card type
        multiplicity: number of each card type
        threshold: maximum total before going bust
        peekCost: how much it costs to peek at the next card
        """
        self.cardValues = cardValues
        self.multiplicity = multiplicity
        self.threshold = threshold
        self.peekCost = peekCost

    # Return the start state.
    # Look at this function to learn about the state representation.
    # The first element of the tuple is the sum of the cards in the player's
    # hand.
    # The second element is the index (not the value) of the next card, if the player peeked in the
    # last action.  If they didn't peek, this will be None.
    # The final element is the current deck.
    def startState(self):
        return (0, None, (self.multiplicity,) * len(self.cardValues))  # total, next card (if any), multiplicity for each card

    # Return set of actions possible from |state|.
    # You do not need to modify this function.
    # All logic for dealing with end states should be done in succAndProbReward
    def actions(self, state):
        return ['Take', 'Peek', 'Quit']

    # Return a list of (newState, prob, reward) tuples corresponding to edges
    # coming out of |state|.  Indicate a terminal state (after quitting or
    # busting) by setting the deck to None. 
    # When the probability is 0 for a particular transition, don't include that 
    # in the list returned by succAndProbReward.
    def succAndProbReward(self, state, action):
        # BEGIN_YOUR_CODE (our solution is 53 lines of code, but don't worry if you deviate from this)
        list = []
        count, next, deck = state
        if action == 'Quit':
            list.append(count, None, None)
        else:
            numCards = 0;
            for i in range(0, len(deck)):
                numCards += deck[i]
            if next == None:
                if action == 'Take':
                    for i in range(0, len(deck)):
                        if deck[i] != 0:
                            if count + self.cardValues[i] > self.threshold:
                                list.append( ( (count + self.cardValues[i], None, None), (0.0 + deck[i]) /numCards, 0))
                            else:
                                newDeck = deck #shallow copy though
                                newDeck[i] = newDeck[i] - 1
                                if numCards == 1:
                                    newDeck == None
                                list.append( ( (count + self.cardValues[i], None, newDeck), (0.0 + deck[i])/numCards, 0))
                else: #action is peek and valid
                    for i in range(0, len(deck)):
                        if deck[i] != 0:
                            list.append( ( (count + self.cardValues[i], i, deck), (0.0 + deck[i])/numCards, self.peekCost))
                                    
            else:
                if action == 'Take':
                    if count + self.cardValues[next] > self.threshold:
                        list.append( ( (count + self.cardValues[next], None, None), 1, 0))
                    else:
                        newDeck = deck #shallow copy though
                        newDeck[next] = newDeck[next] - 1
                        if numCards == 0:
                            newDeck = None
                        list.append( ( (count + self.cardValues[next], None, newDeck), 1, 0))
        return list
        # END_YOUR_CODE

    def discount(self):
        return 1

############################################################
# Problem 3b

def peekingMDP():
    """
    Return an instance of BlackjackMDP where peeking is the optimal action at
    least 10% of the time.
    """
    # BEGIN_YOUR_CODE (our solution is 2 lines of code, but don't worry if you deviate from this)
    raise Exception("Not implemented yet")
    # END_YOUR_CODE

############################################################
# Problem 4a: Q learning

# Performs Q-learning.  Read util.RLAlgorithm for more information.
# actions: a function that takes a state and returns a list of actions.
# discount: a number between 0 and 1, which determines the discount factor
# featureExtractor: a function that takes a state and action and returns a list of (feature name, feature value) pairs.
# explorationProb: the epsilon value indicating how frequently the policy
# returns a random action
class QLearningAlgorithm(util.RLAlgorithm):
    def __init__(self, actions, discount, featureExtractor, explorationProb=0.2):
        self.actions = actions
        self.discount = discount
        self.featureExtractor = featureExtractor
        self.explorationProb = explorationProb
        self.weights = defaultdict(float)
        self.numIters = 0

    # Return the Q function associated with the weights and features
    def getQ(self, state, action):
        score = 0
        for f, v in self.featureExtractor(state, action):
            score += self.weights[f] * v
        return score

    # This algorithm will produce an action given a state.
    # Here we use the epsilon-greedy algorithm: with probability
    # |explorationProb|, take a random action.
    def getAction(self, state):
        self.numIters += 1
        if random.random() < self.explorationProb:
            return random.choice(self.actions(state))
        else:
            return max((self.getQ(state, action), action) for action in self.actions(state))[1]

    # Call this function to get the step size to update the weights.
    def getStepSize(self):
        return 1.0 / math.sqrt(self.numIters)

    # We will call this function with (s, a, r, s'), which you should use to update |weights|.
    # Note that if s is a terminal state, then s' will be None.  Remember to check for this.
    # You should update the weights using self.getStepSize(); use
    # self.getQ() to compute the current estimate of the parameters.
    def incorporateFeedback(self, state, action, reward, newState):
        # BEGIN_YOUR_CODE (our solution is 12 lines of code, but don't worry if you deviate from this)
        raise Exception("Not implemented yet")
        # END_YOUR_CODE

# Return a singleton list containing indicator feature for the (state, action)
# pair.  Provides no generalization.
def identityFeatureExtractor(state, action):
    featureKey = (state, action)
    featureValue = 1
    return [(featureKey, featureValue)]

############################################################
# Problem 4b: convergence of Q-learning
# Small test case
smallMDP = BlackjackMDP(cardValues=[1, 5], multiplicity=2, threshold=10, peekCost=1)

# Large test case
largeMDP = BlackjackMDP(cardValues=[1, 3, 5, 8, 10], multiplicity=3, threshold=40, peekCost=1)
#largeMDP.computeStates()



############################################################
# Problem 4c: features for Q-learning.

# You should return a list of (feature key, feature value) pairs (see
# identityFeatureExtractor()).
# Implement the following features:
# - indicator on the total and the action (1 feature).
# - indicator on the presence/absence of each card and the action (1 feature).
#       Example: if the deck is (3, 4, 0 , 2), then your indicator on the presence of each card is (1,1,0,1)
#       Only add this feature if the deck != None
# - indicator on the number of cards for each card type and the action (len(counts) features).  Only add these features if the deck != None
def blackjackFeatureExtractor(state, action):
    total, nextCard, counts = state
    # BEGIN_YOUR_CODE (our solution is 9 lines of code, but don't worry if you deviate from this)
    raise Exception("Not implemented yet")
    # END_YOUR_CODE

############################################################
# Problem 4d: What happens when the MDP changes underneath you?!

# Original mdp


