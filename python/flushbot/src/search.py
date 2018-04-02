import stacks, hands, game, copy
from card import card
from heapq import heappush, heappop, heapify

veryeasy = [card('King', 'Spades'),card('Queen', 'Spades'),card('Jack', 'Spades'),card('Ten', 'Spades'),card('Ace', 'Spades'),
            card('King', 'Clubs'),card('Queen', 'Clubs'),card('Jack', 'Clubs'),card('Ten', 'Clubs'),card('Nine', 'Clubs'),
            card('Eight', 'Hearts'),card('Eight', 'Spades'),card('Eight', 'Diamonds'),card('Eight', 'Clubs'),card('Two', 'Spades'),
            card('King', 'Diamonds'),card('King', 'Hearts'),card('Nine', 'Diamonds'),card('Nine', 'Spades'),card('Nine', 'Hearts'),
            card('Queen', 'Hearts'),card('Ten', 'Hearts'),card('Ace', 'Hearts'),card('Two', 'Hearts'),card('Jack', 'Hearts'),
            card('Seven', 'Diamonds'),card('Six', 'Diamonds'),card('Five', 'Diamonds'),card('Four', 'Clubs'),card('Three', 'Spades'),
            card('Seven', 'Spades'),card('Seven', 'Hearts'),card('Seven', 'Clubs'),card('Five', 'Clubs'),card('Ace', 'Clubs'),
            card('Six', 'Hearts'),card('Six', 'Clubs'),card('Five', 'Hearts'),card('Five', 'Spades'),card('Two', 'Diamonds'),
            card('Four', 'Spades'),card('Four', 'Hearts'),card('Three', 'Hearts'),card('Two', 'Clubs'),card('Ten', 'Diamonds'),
            card('Four', 'Diamonds'),card('Ace', 'Diamonds'),card('Six', 'Spades'), 
            card('Jack', 'Diamonds'),card('Three', 'Clubs'),card('Three', 'Diamonds'),  
            card('Queen', 'Diamonds')]

easy = [card('Queen', 'Hearts'),card('Ten', 'Hearts'),card('Ace', 'Hearts'),card('Two', 'Hearts'),card('Jack', 'Hearts'),
            card('King', 'Clubs'),card('Queen', 'Clubs'),card('Jack', 'Clubs'),card('Ten', 'Clubs'),card('Nine', 'Clubs'),
            card('Jack', 'Diamonds'),card('Three', 'Clubs'),card('Three', 'Diamonds'),  
            card('Eight', 'Hearts'),card('Eight', 'Spades'),card('Eight', 'Diamonds'),card('Eight', 'Clubs'),card('Two', 'Spades'),
            card('King', 'Diamonds'),card('King', 'Hearts'),card('Nine', 'Diamonds'),card('Nine', 'Spades'),card('Nine', 'Hearts'),
            card('Seven', 'Diamonds'),card('Six', 'Diamonds'),card('Five', 'Diamonds'),card('Four', 'Clubs'),card('Three', 'Spades'),
            card('Four', 'Spades'),card('Four', 'Hearts'),card('Three', 'Hearts'),card('Two', 'Clubs'),card('Ten', 'Diamonds'),
            card('King', 'Spades'),card('Queen', 'Spades'),card('Jack', 'Spades'),card('Ten', 'Spades'),card('Ace', 'Spades'),
            card('Seven', 'Spades'),card('Seven', 'Hearts'),card('Seven', 'Clubs'),card('Five', 'Clubs'),card('Ace', 'Clubs'),
            card('Six', 'Hearts'),card('Six', 'Clubs'),card('Five', 'Hearts'),card('Five', 'Spades'),card('Two', 'Diamonds'),
            card('Four', 'Diamonds'),card('Ace', 'Diamonds'),card('Six', 'Spades'), 
            card('Queen', 'Diamonds')]


random = [card('Eight', 'Clubs'), card('Queen', 'Hearts'), card('Ace', 'Clubs'), 
            card('Six', 'Hearts'), card('Eight', 'Spades'), card('Five', 'Spades'), 
            card('Nine', 'Clubs'), card('Four', 'Spades'), card('Eight', 'Diamonds'), 
            card('Two', 'Spades'), card('Five', 'Clubs'), card('Four', 'Hearts'), 
            card('King', 'Clubs'), card('Two', 'Diamonds'), card('Nine', 'Hearts'), 
            card('King', 'Diamonds'), card('Ten', 'Hearts'), card('Ten', 'Clubs'), 
            card('Eight', 'Hearts'), card('Six', 'Diamonds'), card('Three', 'Hearts'), 
            card('Queen', 'Spades'), card('Four', 'Diamonds'), card('Ace', 'Spades'), 
            card('Two', 'Clubs'), card('King', 'Spades'), card('Ace', 'Diamonds'), 
            card('Jack', 'Hearts'), card('Ten', 'Diamonds'), card('King', 'Hearts'), 
            card('Five', 'Diamonds'), card('Nine', 'Diamonds'), card('Seven', 'Spades'), 
            card('Seven', 'Clubs'), card('Queen', 'Clubs'), card('Six', 'Spades'), 
            card('Ace', 'Hearts'), card('Nine', 'Spades'), card('Ten', 'Spades'), 
            card('Two', 'Hearts'), card('Seven', 'Hearts'), card('Jack', 'Diamonds'), 
            card('Five', 'Hearts'), card('Jack', 'Spades'), card('Three', 'Spades'), 
            card('Three', 'Clubs'), card('Three', 'Diamonds'), card('Four', 'Clubs'), 
            card('Queen', 'Diamonds'), card('Jack', 'Clubs'), card('Seven', 'Diamonds'), 
            card('Six', 'Clubs')]

testdeck = easy

INFINITY = 32000
counter = 0
bestgame = 0
bestnode = None
bestcost = 0
bestpathcost = 0
completed = []

def solsearch():
    initstate = state(game.gamestate(), 0, testdeck)
    result,junk = rbfs(initstate,INFINITY)
    if result == None:
        print "No answer"
    else:
        print result.history


def rbfs(node, flimit):
    if node.problem.completecount == 9:
        return (node,0)
    if len(node.deck) == 0:
        return (None,INFINITY)
    #Don't even bother with nodes that have a penalty
    if node.problem.penalties > 0:
        return (None,INFINITY)
    
    global counter
    global bestgame
    global completed
    global bestnode
    global bestcost
    global bestpathcost
    counter += 1
    if node.problem.completecount > bestgame:
        bestnode = node
        bestgame = node.problem.completecount
        bestcost = node.cost
        bestpathcost = node.pathcost
        completed = node.problem.completelist()    
    print counter, "BDepth:", bestpathcost, "BCost:", bestcost, \
          "Best:", bestgame, completed, "CDepth:", node.pathcost, "CCost:", node.cost, \
          "Current:", node.problem.completelist()    
    if counter % 1 == 0:
        print node.history
    successors = rbfs_expand(node)
    if len(successors) == 0: return (None,INFINITY)
    for s in successors:
        s.cost = max(s.pathcost + s.heuristic, node.cost)
    while True:
        best = successors[0]
        alt = successors[0]
        for s in successors: # Find lowest value and second lowest value
            if s.cost < best.cost:
                best = s
                continue
            if s.cost < alt.cost:
                alt = s
        if best.cost > flimit: return (None,best.cost)
        result,best.cost = rbfs(best, min(flimit, alt.cost))
        if result != None: return result,best.cost
    
def rbfs_expand(node):
    nodes = []
    playedempty = False
    for i in range(1,5):
        if len(node.problem.bins[i]) > 0 or not playedempty:
            cpy = copy.deepcopy(node)
            cpy.pathcost = node.pathcost + 1
            cpy.cost = -1
            cpy.playnext(i)
            nodes.append(cpy)
            if len(node.problem.bins[i]) == 0:
                playedempty = True
        if len(node.problem.bins[i]) < 4 and len(node.problem.bins[i]) > 0:
            cpy2 = copy.deepcopy(node)
            cpy2.pathcost = node.pathcost+1
            cpy2.cost = -1
            cpy2.discard(i)
            nodes.append(cpy2)
    return nodes

class state:
    
    # Can improve performance by caching value between calls.  Will need to modify
    # deep copy so that cached value is reset when copied.
    def __init__(self, problem, pathcost, deck, history=[]):
        self.problem = problem
        self.pathcost = pathcost
        self.deck = deck
        self.history = history
        self.__cost = -1
    
    @property
    def cost(self):
        def fget(self):
            if self.__cost == -1:
                self.__cost = self.pathcost + self.heuristic
                return self.__cost 
            else:
                return self.__cost
        def fset(self, value):
            self.__cost = value
    
    @property
    def heuristic(self):
        return self.handvalue()
             
    def __cmp__(self, other):
        if isinstance(other, state):
            if self.cost == other.cost:
                return 0
            elif self.cost < other.cost:
                return -1
            else:
                return 1
        else: 
            return NotImplemented
        
    def playnext(self, bin):
        card = self.deck.pop(0)
        self.history.append((bin, card))
        self.problem.addcard(bin, card)
        
    def discard(self, bin):
        self.history.append(('Discard', bin))
        self.problem.foldbin(bin)

    def handvalue(self):
        best = 5
        score = 45
        if not self.problem.complete['R']:
            bestlen = 5
            lengths = [len(hands.toMakeRoyalFlush(self.problem.getbin(i))) for i in range(1,5)]
            for i in range(0,4):
                if lengths[i] > 0:
                    bestlen = min(bestlen, 5-len(self.problem.getbin(i+1)))
            if bestlen < best:
                best = bestlen
        else:
            score -= 5
        if not self.problem.complete['T']:
            bestlen = 5
            lengths = [len(hands.toMakeStraightFlush(self.problem.getbin(i))) for i in range(1,5)]
            for i in range(0,4):
                if lengths[i] > 0:
                    bestlen = min(bestlen, 5-len(self.problem.getbin(i+1)))
            if bestlen < best:
                best = bestlen
        else:
            score -= 5
        if not self.problem.complete['4']:
            bestlen = 5
            lengths = [len(hands.toMakeFourOAK(self.problem.getbin(i))) for i in range(1,5)]
            for i in range(0,4):
                if lengths[i] > 0:
                    bestlen = min(bestlen, 5-len(self.problem.getbin(i+1)))
            if bestlen < best:
                best = bestlen  
        else:
            score -= 5
        if not self.problem.complete['H']:
            bestlen = 5
            lengths = [len(hands.toMakeFullHouse(self.problem.getbin(i))) for i in range(1,5)]
            for i in range(0,4):
                if lengths[i] > 0:
                    bestlen = min(bestlen, 5-len(self.problem.getbin(i+1)))
            if bestlen < best:
                best = bestlen
        else:
            score -= 5
        if not self.problem.complete['F']:
            bestlen = 5
            lengths = [len(hands.toMakeFlush(self.problem.getbin(i))) for i in range(1,5)]
            for i in range(0,4):
                if lengths[i] > 0:
                    bestlen = min(bestlen, 5-len(self.problem.getbin(i+1)))
            if bestlen < best:
                best = bestlen
        else:
            score -= 5
        if not self.problem.complete['S']:
            bestlen = 5
            lengths = [len(hands.toMakeStraight(self.problem.getbin(i))) for i in range(1,5)]
            for i in range(0,4):
                if lengths[i] > 0:
                    bestlen = min(bestlen, 5-len(self.problem.getbin(i+1)))
            if bestlen < best:
                best = bestlen
        else:
            score -= 5
        if not self.problem.complete['3']:
            bestlen = 5
            lengths = [len(hands.toMakeThreeOAK(self.problem.getbin(i))) for i in range(1,5)]
            for i in range(0,4):
                if lengths[i] > 0:
                    bestlen = min(bestlen, 5-len(self.problem.getbin(i+1)))
            if bestlen < best:
                best = bestlen
        else:
            score -= 5
        if not self.problem.complete['X']:
            bestlen = 5
            lengths = [len(hands.toMakeTwoPair(self.problem.getbin(i))) for i in range(1,5)]
            for i in range(0,4):
                if lengths[i] > 0:
                    bestlen = min(bestlen, 5-len(self.problem.getbin(i+1)))
            if bestlen < best:
                best = bestlen
        else:
            score -= 5
        if not self.problem.complete['P']:
            bestlen = 5
            lengths = [len(hands.toMakePair(self.problem.getbin(i))) for i in range(1,5)]
            for i in range(0,4):
                if lengths[i] > 0:
                    bestlen = min(bestlen, 5-len(self.problem.getbin(i+1)))
            if bestlen < best:
                best = bestlen
        else:
            score -= 5
        return score-(5-best)
       
    def oldhandvalue(self):
        score = 0
        if not self.problem.complete['R']:
            bestlen = 5
            lengths = [len(hands.toMakeRoyalFlush(self.problem.getbin(i))) for i in range(1,5)]
            for i in range(0,4):
                if lengths[i] > 0:
                    bestlen = min(bestlen, 5-len(self.problem.getbin(i+1)))
            score += float(bestlen)/9
        else:
            score -= 4.0+4.0/4.0+4.0/5.0+4.0/8.0
        if not self.problem.complete['T']:
            bestlen = 5
            lengths = [len(hands.toMakeStraightFlush(self.problem.getbin(i))) for i in range(1,5)]
            for i in range(0,4):
                if lengths[i] > 0:
                    bestlen = min(bestlen, 5-len(self.problem.getbin(i+1)))
            score += float(bestlen)/8
        else:
            score -= 4.0+4.0/4.0+4.0/5.0
        if not self.problem.complete['4']:
            bestlen = 5
            lengths = [len(hands.toMakeFourOAK(self.problem.getbin(i))) for i in range(1,5)]
            for i in range(0,4):
                if lengths[i] > 0:
                    bestlen = min(bestlen, 5-len(self.problem.getbin(i+1)))
            score += float(bestlen)/7
            if bestlen >= 3:
                score -= 3.0/6.0+3.0/3.0
            
        else:
            score -= 4.0+4.0/3.0+4.0/6.0
        if not self.problem.complete['H']:
            bestlen = 5
            lengths = [len(hands.toMakeFullHouse(self.problem.getbin(i))) for i in range(1,5)]
            for i in range(0,4):
                if lengths[i] > 0:
                    bestlen = min(bestlen, 5-len(self.problem.getbin(i+1)))
            score += float(bestlen)/6
        else:
            score -= 4.0/2.0+4.0/3.0
        if not self.problem.complete['F']:
            bestlen = 5
            lengths = [len(hands.toMakeFlush(self.problem.getbin(i))) for i in range(1,5)]
            for i in range(0,4):
                if lengths[i] > 0:
                    bestlen = min(bestlen, 5-len(self.problem.getbin(i+1)))
            score += float(bestlen)/5
        else:
            score -= 4.0+4.0/4.0
        if not self.problem.complete['S']:
            bestlen = 5
            lengths = [len(hands.toMakeStraight(self.problem.getbin(i))) for i in range(1,5)]
            for i in range(0,4):
                if lengths[i] > 0:
                    bestlen = min(bestlen, 5-len(self.problem.getbin(i+1)))
            score += float(bestlen)/4
        else:
            score -= 4.0
        if not self.problem.complete['3']:
            bestlen = 5
            lengths = [len(hands.toMakeThreeOAK(self.problem.getbin(i))) for i in range(1,5)]
            for i in range(0,4):
                if lengths[i] > 0:
                    bestlen = min(bestlen, 5-len(self.problem.getbin(i+1)))
            score += float(bestlen)/3
        else:
            score -= 4.0+4.0/2.0
        if not self.problem.complete['X']:
            bestlen = 5
            lengths = [len(hands.toMakeTwoPair(self.problem.getbin(i))) for i in range(1,5)]
            for i in range(0,4):
                if lengths[i] > 0:
                    bestlen = min(bestlen, 5-len(self.problem.getbin(i+1)))
            score += float(bestlen)/2
        else:
            score -= 4.0
        if not self.problem.complete['P']:
            bestlen = 5
            lengths = [len(hands.toMakePair(self.problem.getbin(i))) for i in range(1,5)]
            for i in range(0,4):
                if lengths[i] > 0:
                    bestlen = min(bestlen, 5-len(self.problem.getbin(i+1)))
            score += float(bestlen)
        return score
    
if __name__ == '__main__': solsearch() 
