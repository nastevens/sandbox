import stacks, hands, copy
from card import card
from util import prop
from game import gamestate
from bisect import insort

INFINITY = 32000
counter = 0
bestgame = 0
bestnode = None
bestcost = 0
bestpathcost = 0
completed = []
memlimit = 200

def smas(initial):
    queue = []
    insort(queue,initial)
    while True:
        if len(queue) == 0:
            return None
        n = queue[0]
        if n.problem.completecount == 9:
            return n
        s = node.getsuccessor()
        if not s.problem.completecount == 9 and s.problem.depth == 52:
            s.cost = INFINITY
        else:
            s.cost = min(n.cost,s.depth+s.heuristic)
        if n.allexpanded():
            pass
            #Update n's f-cost and those of its ancestors to min of children's f-costs
        if n.allinmemory():
            n = queue.pop(0) #Remove n from queue
            del n
        if len(queue) > memlimit:
            worst = queue.pop(-1)
            del worst
        heappush(queue,s)
        
class state:
    
    # TODO: Can improve performance by caching value between calls.  Will need to modify
    # deep copy so that cached value is reset when copied.
    def __init__(self, game, depth, deck, parent=None, history=[], cost=-1):
        self.game = game
        self.depth = depth
        self.deck = deck
        self.history = []
        self._cost = cost
        # (pointer (none if not in memory), f-cost, index 0-7)
        self.successors = [(None,-1,r) for r in range(0,8)]
        self.sindex = 0
        self.parent = parent
    
    def __del__(self):
        pass #Make sure to remove this state from its parent
    
    @prop
    def cost():
        def fget(self):
            if self._cost == -1:
                self._cost = self.depth + self.heuristic
                return self._cost 
            else:
                return self._cost
        def fset(self, value):
            self._cost = value
        def fdel(self):
            del self._cost
        return locals()
    
    @prop
    def heuristic():
        def fget(self):
            return self._heuristic()
        return locals()
    
    def allexpanded(self):
        return sindex == 8
    
    def allinmemory(self):
        pass
             
    def __cmp__(self, other):
        if isinstance(other, state):
            if self.cost == other.cost:
                if self.depth == other.depth:
                    return 0
                elif self.depth < other.depth:
                    return 1
                else:
                    return -1
            elif self.cost < other.cost:
                return -1
            else:
                return 1
        else: 
            return NotImplemented
        
    def getsuccessor(self):
        if sindex > 7:
            return None
        sstate = self.successors[self.sindex]
        successor = search.smasstate(self.game, self.depth+1, self.deck, self, self.history)
        if sstate[2] < 4:
            successor.play(sstate[2]+1)
        else:
            binlen = len(successor.game.bins[sstate[2]-3])
            if 0 < binlen < 4:
                successor.discard(sstate[2]-3)
        self.sindex += 1
        return successor
        
    def play(self, bin):    
        card = self.deck.pop(0)
        self.history.append((bin, card))
        self.game.addcard(bin, card)
        
    def discard(self, bin):
        self.history.append(('Discard', bin))
        self.game.foldbin(bin)

    def _heuristic(self):
        best = 5
        score = 45
        if not self.game.complete['R']:
            bestlen = 5
            lengths = [len(hands.toMakeRoyalFlush(self.game.getbin(i))) for i in range(1,5)]
            for i in range(0,4):
                if lengths[i] > 0:
                    bestlen = min(bestlen, 5-len(self.game.getbin(i+1)))
            if bestlen < best:
                best = bestlen
        else:
            score -= 5
        if not self.game.complete['T']:
            bestlen = 5
            lengths = [len(hands.toMakeStraightFlush(self.game.getbin(i))) for i in range(1,5)]
            for i in range(0,4):
                if lengths[i] > 0:
                    bestlen = min(bestlen, 5-len(self.game.getbin(i+1)))
            if bestlen < best:
                best = bestlen
        else:
            score -= 5
        if not self.game.complete['4']:
            bestlen = 5
            lengths = [len(hands.toMakeFourOAK(self.game.getbin(i))) for i in range(1,5)]
            for i in range(0,4):
                if lengths[i] > 0:
                    bestlen = min(bestlen, 5-len(self.game.getbin(i+1)))
            if bestlen < best:
                best = bestlen  
        else:
            score -= 5
        if not self.game.complete['H']:
            bestlen = 5
            lengths = [len(hands.toMakeFullHouse(self.game.getbin(i))) for i in range(1,5)]
            for i in range(0,4):
                if lengths[i] > 0:
                    bestlen = min(bestlen, 5-len(self.game.getbin(i+1)))
            if bestlen < best:
                best = bestlen
        else:
            score -= 5
        if not self.game.complete['F']:
            bestlen = 5
            lengths = [len(hands.toMakeFlush(self.game.getbin(i))) for i in range(1,5)]
            for i in range(0,4):
                if lengths[i] > 0:
                    bestlen = min(bestlen, 5-len(self.game.getbin(i+1)))
            if bestlen < best:
                best = bestlen
        else:
            score -= 5
        if not self.game.complete['S']:
            bestlen = 5
            lengths = [len(hands.toMakeStraight(self.game.getbin(i))) for i in range(1,5)]
            for i in range(0,4):
                if lengths[i] > 0:
                    bestlen = min(bestlen, 5-len(self.game.getbin(i+1)))
            if bestlen < best:
                best = bestlen
        else:
            score -= 5
        if not self.game.complete['3']:
            bestlen = 5
            lengths = [len(hands.toMakeThreeOAK(self.game.getbin(i))) for i in range(1,5)]
            for i in range(0,4):
                if lengths[i] > 0:
                    bestlen = min(bestlen, 5-len(self.game.getbin(i+1)))
            if bestlen < best:
                best = bestlen
        else:
            score -= 5
        if not self.game.complete['X']:
            bestlen = 5
            lengths = [len(hands.toMakeTwoPair(self.game.getbin(i))) for i in range(1,5)]
            for i in range(0,4):
                if lengths[i] > 0:
                    bestlen = min(bestlen, 5-len(self.game.getbin(i+1)))
            if bestlen < best:
                best = bestlen
        else:
            score -= 5
        if not self.game.complete['P']:
            bestlen = 5
            lengths = [len(hands.toMakePair(self.game.getbin(i))) for i in range(1,5)]
            for i in range(0,4):
                if lengths[i] > 0:
                    bestlen = min(bestlen, 5-len(self.game.getbin(i+1)))
            if bestlen < best:
                best = bestlen
        else:
            score -= 5
        return score-(5-best)