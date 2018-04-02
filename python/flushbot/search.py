import stacks, hands, game, copy
from card import card
from heapq import heappush, heappop, heapify

testdeck = [card('Eight', 'Clubs'), card('Queen', 'Hearts'), card('Ace', 'Clubs'), 
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

def solsearch():
    new = []
    initstate = state(game.gamestate(), 0, testdeck)
    new.append(initstate)
    complete = search(new)
    print complete.history
    
def search(new):
    counter = 0
    best = 0
    completed = []
    heapify(new)
    while len(new) > 0:
        working = heappop(new)
        counter += 1
        if working.game.completecount > best:
            best = working.game.completecount
            completed = working.game.completelist()
        if counter % 2 == 0:
            print "Count:", counter, "Depth:", working.cost, "Best:", best, completed, "Current:", working.game.completelist()
        if working.game.completecount == 9:
            #Found our state - exit
            return working
        else:
            expandstate(working, new)
            del working
            
def expandstate(working, new):
    totallen = 0
    for i in range(1,5):
        totallen += len(working.game.getbin(i))
    totallen += len(working.game.getbin('remaining'))
    if (9 - working.game.completecount)*5 > totallen:
        return
    for i in range(1,5):
        cpy = copy.deepcopy(working)
        cpy.cost = working.cost + 1
        cpy.playnext(i)
        #Don't want to expand where there's been a penalty
        if cpy.game.penalties == 0:
            heappush(new, cpy)
        #Can't discard once past 3 cards
        if len(working.game.getbin(i)) < 4:
            cpy = copy.deepcopy(working)
            cpy.cost = working.cost + 1
            cpy.discard(i)
            heappush(new, cpy)

def rbfs(problem, node, flimit):
    if node.game.completecount == 9:
        return (node,0)
    successors = rbfs_expand(node, problem)
    if len(successors) == 0: return (None,-1)
    for s in successors:
        s.cost = max(s.pathcost + s.heuristic, node.cost)
    while True:
        best = None #TODO: Node with lowest cost in successors
        if best > flimit: return (None,best)
        alt = None #TODO: Node with second lowest cost in successors
        result,best.cost = rbfs(problem, best, min(flimit, alt))
        if result != None: return result
    
def rbfs_expand(node, problem):
    pass  

class state:
    
    # Can improve performance by caching value between calls.  Will need to modify
    # deep copy so that cached value is reset when copied.
    def __init__(self, game, cost, toplay):
        self.game = game
        self.cost = cost
        self.toplay = toplay
        self.history = []
        
    def __cmp__(self, other):
        if isinstance(other, state):
            if self.value() == other.value():
                return 0
            elif self.value() < other.value():
                return -1
            else:
                return 1
        else: 
            return NotImplemented
        
    def playnext(self, bin):
        card = self.toplay.pop()
        self.history.append((bin, card))
        self.game.addcard(bin, card)
        
    def discard(self, bin):
        self.history.append(('Discard', bin))
        self.game.foldbin(bin)
        
    def value(self):
        return self.cost + self.handvalue()
   
    def handvalue(self):
        score = 0
        if not self.game.complete['R']:
            bestlen = 5
            lengths = [len(hands.toMakeRoyalFlush(self.game.getbin(i))) for i in range(1,5)]
            for i in range(0,4):
                if lengths[i] > 0:
                    bestlen = min(bestlen, 5-len(self.game.getbin(i+1)))
            score += bestlen
        if not self.game.complete['T']:
            bestlen = 5
            lengths = [len(hands.toMakeStraightFlush(self.game.getbin(i))) for i in range(1,5)]
            for i in range(0,4):
                if lengths[i] > 0:
                    bestlen = min(bestlen, 5-len(self.game.getbin(i+1)))
            score += bestlen
        if not self.game.complete['4']:
            bestlen = 5
            lengths = [len(hands.toMakeFourOAK(self.game.getbin(i))) for i in range(1,5)]
            for i in range(0,4):
                if lengths[i] > 0:
                    bestlen = min(bestlen, 5-len(self.game.getbin(i+1)))
            score += bestlen
        if not self.game.complete['H']:
            bestlen = 5
            lengths = [len(hands.toMakeFullHouse(self.game.getbin(i))) for i in range(1,5)]
            for i in range(0,4):
                if lengths[i] > 0:
                    bestlen = min(bestlen, 5-len(self.game.getbin(i+1)))
            score += bestlen
        if not self.game.complete['F']:
            bestlen = 5
            lengths = [len(hands.toMakeFlush(self.game.getbin(i))) for i in range(1,5)]
            for i in range(0,4):
                if lengths[i] > 0:
                    bestlen = min(bestlen, 5-len(self.game.getbin(i+1)))
            score += bestlen
        if not self.game.complete['S']:
            bestlen = 5
            lengths = [len(hands.toMakeStraight(self.game.getbin(i))) for i in range(1,5)]
            for i in range(0,4):
                if lengths[i] > 0:
                    bestlen = min(bestlen, 5-len(self.game.getbin(i+1)))
            score += bestlen
        if not self.game.complete['3']:
            bestlen = 5
            lengths = [len(hands.toMakeThreeOAK(self.game.getbin(i))) for i in range(1,5)]
            for i in range(0,4):
                if lengths[i] > 0:
                    bestlen = min(bestlen, 5-len(self.game.getbin(i+1)))
            score += bestlen
        if not self.game.complete['X']:
            bestlen = 5
            lengths = [len(hands.toMakeTwoPair(self.game.getbin(i))) for i in range(1,5)]
            for i in range(0,4):
                if lengths[i] > 0:
                    bestlen = min(bestlen, 5-len(self.game.getbin(i+1)))
            score += bestlen
        if not self.game.complete['P']:
            bestlen = 5
            lengths = [len(hands.toMakePair(self.game.getbin(i))) for i in range(1,5)]
            for i in range(0,4):
                if lengths[i] > 0:
                    bestlen = min(bestlen, 5-len(self.game.getbin(i+1)))
            score += bestlen
        return score
    
    def appliedvalue(self, game):
        remain = len(game.getbin('remaining'))
        score = 0
        
        for i in range(1,5):
            tmp = game.getbin(i)
            # Cards of the same suit
            bestsuit = 0
            bestrank = 0
            
            for j in range(1,5):
                tmpsuit = len([card for card in tmp if card.suit() == j])
                if tmpsuit > bestsuit:
                    bestsuit = tmpsuit
            
            # Cards of the same rank
            for j in range(1,14):
                tmprank = len([card for card in tmp if card.rank() == j])
                if tmprank > bestrank:
                    bestrank = tmprank
                    
            # Cards in a series
            series = 0
            if len(tmp) > 0:
                hand = set([crd.rank() for crd in tmp])
                if 1 in hand: hand.add(14)
                needed = set(range(min(hand), min(hand)+5))
                series = len(needed.intersection(hand))
                
            # Bonus for all straight and flush
            sfbonus = 0
            if bestsuit == series:
                sfbonus = 10 * bestsuit
                
            # Bonus for royal flush
            rfbonus = 0
            if bestsuit == series:
                hand = set([crd.rank() for crd in tmp])
                if len(hand) > 0 and min(hand) == 10:
                    rfbonus = 20 * bestsuit
                    
            score += 3*bestsuit + 5*bestrank + 3*series + sfbonus + rfbonus

        return score 

    def appliedpenalty(self):
        return (self.cost - (self.game.completecount+1) * 5) ** 2
    
if __name__ == '__main__': solsearch() 
