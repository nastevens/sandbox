import stacks
from card import card
    
def groups(cards):
    '''Checks for groups of cards
    Returns a list of lists with the cards grouped by rank'''
    group = []
    for v in range(0,13): group.append([])
    for card in cards: group[card.rank()-1].append(card)
    return group

def flushes(cards):
    '''Checks for groups of flushes
    Returns a list of lists with the cards group by suit'''
    group = []
    for v in range(0,4): group.append([])
    for card in cards: group[card.suit()-1].append(card)
    return group

def toMakeRoyalFlush(cards):
    if not isinstance(cards,stacks.stack):
        raise NotImplementedError, "toMakeRoyalFlush only works on stacks"
    rset = stacks.stack()
    
    if len(cards) < 1:  #No cards played yet - any face card combination will work
        rset.populate("Royal Flush")
        return rset.difference(cards)
        
    if len(cards) >= 5:  #Five cards played - nothing else will work
        rset.clear()
        return rset
    
    rset.populate("Royal Flush",list(cards)[0].suit())  #Get the suit of one of the cards in the stack
    if len(rset.intersection(cards)) == len(cards):
        rset = rset.difference(cards)
        return rset
    else:
        rset.clear()
        return rset
        
def isRoyalFlush(cards):
    if not isinstance(cards,stacks.stack):
        raise NotImplementedError, "toMakeRoyalFlush only works on stacks"
    rset = stacks.stack()
    
    if len(cards) != 5:
        return False
    
    rset.populate("Royal Flush",list(cards)[0].suit())  #Get a set of Royal Flush cards in the same suit as one of the cards in the stack
    if cards == rset:
        return True
    else:
        return False
    
def toMakeStraightFlush(cards):
    if not isinstance(cards,stacks.stack):
        raise NotImplementedError, "toMakeStraightFlush only works on stacks"
    rset = stacks.stack()
    exclude = stacks.stack()
    rset.populate("Full Deck")
    if (len(cards) < 1):  #No cards played yet - anything will work
        return rset
    if (len(cards) > 4):  #Five cards played - nothing else will work
        rset.clear()
        return rset
    if len(cards) == 1 and list(cards)[0].rank() == 1: #Special case for single ace
        rset.clear()
        for rank in range(10,14)+range(2,6):
            rset.add(card(rank,list(cards)[0].suit()))
        return rset
    if len(cards) == 4 and len(toMakeRoyalFlush(cards)) != 0:
        exclude = toMakeRoyalFlush(cards)
        
    invalid = set([-3,-2,-1,0,15,16,17,18])
    grouped = groups(cards)
    wset = stacks.stack()
    maxgroup = max([len(v) for v in grouped]) #Calculates the number of cards in the rank with the most cards
    if maxgroup > 1:  #If there's more than one in the maxgroup, can't continue to make a straight
        rset.clear()
        return rset
    flushed = flushes(cards)
    maxflush = max([len(v) for v in flushed])
    if maxflush != len(cards):
        rset.clear()
        return rset
    #Calculate max and min rank
    ranks = [group[0].rank() for group in grouped if len(group) != 0]
    mn = min(ranks)
    mx = max(ranks)
    ranks.sort()
    if 1 in ranks:
        spanlo = abs(1-max(ranks))
        spanhi = abs(ranks[1]-14)
        if min(spanhi,spanlo) == spanlo:
            mx = max(ranks)
            mn = 1
        else:
            mx = 14
            mn = ranks[1]
        span = abs(mx-mn)
    else:
        span = abs(min(ranks)-max(ranks))
    if span > 4:  #No good - cards we have are too far apart
        rset.clear()
        return rset
    
    rset.clear()
    adj = 4-span
    for rank in set(range(mn-adj,mx+adj+1)).difference(invalid):
        rset.add(card(rank,list(cards)[0].suit()))
    for crd in cards:
        wset.add(crd)
    return rset.difference(wset).difference(exclude)

def isStraightFlush(cards):
    if not isinstance(cards,stacks.stack):
        raise NotImplementedError, "isStraightFlush only works on stacks"
    rset = stacks.stack()
    
    if len(cards) != 5:
        return False
        
    if isStraight(cards) and isFlush(cards):
        return True
    else:
        return False
    
def toMakeFourOAK(cards):
    if not isinstance(cards,stacks.stack):
        raise NotImplementedError, "toMakeFourOAK only works on stacks"
    rset = stacks.stack()
    rset.populate("Full Deck")

    if len(cards) < 1:  #No cards played yet - anything will work
        return rset
        
    if len(cards) >= 5:  #Five cards played, nothing else will work
        rset.clear()
        return rset
        
    grouped = groups(cards)
    maxgroup = max([len(v) for v in grouped]) #Calculates the number of cards in the rank with the most cards
    if maxgroup == len(cards):  #All cards are same rank - anything else will work
        return rset.difference(cards)
    if maxgroup == len(cards)-1:  #3OAK + 1, 2OAK + 1, or split - need remaining card in rank
        rset.clear()
        for group in grouped:
            if len(group) == maxgroup:
                rset.populate("Rank",group[0].rank())
        return rset.difference(cards)
    else:  #There are already too many non-matching cards - nothing will work
        rset.clear()
        return rset
        
def isFourOAK(cards):
    if not isinstance(cards,stacks.stack):
        raise NotImplementedError, "toMakeFourOAK only works on stacks"
    rset = stacks.stack()
    
    if len(cards) != 5:
        return False
        
    grouped = groups(cards)
    maxgroup = max([len(v) for v in grouped])
    if maxgroup != len(cards)-1:
        return False
    else:
        return True
        
def toMakeFullHouse(cards):
    if not isinstance(cards,stacks.stack):
        raise NotImplementedError, "toMakeFullHouse only works on stacks"
    rset = stacks.stack()
    rset.populate("Full Deck")

    if len(cards) < 1:  #No cards played yet - anything will work
        return rset
        
    if len(cards) >= 5:  #Five cards played, nothing else will work
        rset.clear()
        return rset

    grouped = groups(cards)
    wset = stacks.stack()
    maxgroup = max([len(v) for v in grouped]) #Calculates the number of cards in the rank with the most cards
    if maxgroup == len(cards):  #All cards are in the same rank
        if maxgroup > 3:  #Already a 4OAK - nothing will work
            rset.clear()
            return rset
        if maxgroup == 3:  #A 3OAK - anything will work except another of the same rank
            for card in cards: wset.populate("Rank",card)
            return rset.difference(wset)
        if maxgroup < 3:  #A safe pair - anything except the given cards will work
            return rset.difference(cards)
    if maxgroup == len(cards)-1:  #3OAK +1, Pair+1, or split
        if maxgroup == 3:  #Have a 3OAK and one single - need to finish the single
            rset.clear()
            for group in grouped:
                if len(group) == 1:
                    rset.populate("Rank",group[0])
            return rset.difference(cards)           
        if maxgroup < 3:  #Need to return only cards from the two ranks given
            rset.clear()
            for group in filter(None,grouped):
                rset.populate("Rank",group[0])
            return rset.difference(cards)
    if maxgroup == len(cards)-2: # 2-1-1,2-2,1-1-1,2-2,etc
        if (maxgroup == 2) and (len(filter(None,grouped)) == 2): #2-2 - need one of the remaining cards in the rank
            rset.clear()
            for group in filter(None,grouped):
                rset.populate("Rank",group[0])
            return rset.difference(cards)
        else:
            rset.clear()
            return rset
    else:  #There are already too many non-matching cards - nothing will work
        rset.clear()
        return rset
    
def isFullHouse(cards):
    if not isinstance(cards,stacks.stack):
        raise NotImplementedError, "isFullHouse only works on stacks"
    rset = stacks.stack()
    
    if len(cards) != 5:
        return False
        
    grouped = [len(group) for group in groups(cards) if len(group) != 0]
    if set(grouped) == set([2,3]):
        return True
    else:
        return False
    
def toMakeFlush(cards):
    if not isinstance(cards,stacks.stack):
        raise NotImplementedError, "toMakeFlush only works on stacks"
    rset = stacks.stack()
    
    if len(cards) < 1:  #No cards played yet - anything can make a flush
        rset.populate("Full Deck")
        return rset
        
    if len(cards) >= 5:  #Five cards played, nothing else will work
        rset.clear()
        return rset
        
    rset.populate("Suit",list(cards)[0].suit())  #Get the suit of one of the cards in the stack
    if len(rset.intersection(cards)) == len(cards):
        if len(cards) == 4:  #Need to make special considerations for straight flush and royal flush
            rset = rset.difference(toMakeRoyalFlush(cards))
            rset = rset.difference(toMakeStraightFlush(cards))
            return rset.difference(cards)
        else:
            rset = rset.difference(cards)
            return rset
    else:
        rset.clear()
        return rset
    
def isFlush(cards):
    if not isinstance(cards,stacks.stack):
        raise NotImplementedError, "isFlush only works on stacks"
    
    if len(cards) != 5:
        return False
        
    flushed = flushes(cards)
    maxflush = max([len(v) for v in flushed])
    if maxflush != 5:
        return False
    else:
        return True
    
def toMakeStraight(cards):
    if not isinstance(cards,stacks.stack):
        raise NotImplementedError, "toMakeStraight only works on stacks"
    
    rset = stacks.stack()
    exclude = stacks.stack()
    rset.populate("Full Deck")
    if (len(cards) < 1):  #No cards played yet - anything will work
        return rset
    if (len(cards) > 4):  #Five cards played - nothing else will work
        rset.clear()
        return rset
    if len(cards) == 1 and list(cards)[0].rank() == 1: #Special case for single ace
        rset.clear()
        for rank in range(10,14)+range(2,6):
            rset.populate("Rank",rank)
        return rset
    if len(cards) == 4 and len(toMakeRoyalFlush(cards)) != 0:
        exclude = toMakeRoyalFlush(cards)
        
    invalid = set([-3,-2,-1,0,15,16,17,18])
    grouped = groups(cards)
    wset = stacks.stack()
    maxgroup = max([len(v) for v in grouped]) #Calculates the number of cards in the rank with the most cards
    if maxgroup > 1:  #If there's more than one in the maxgroup, can't continue to make a straight
        rset.clear()
        return rset
    if len(cards) == 4: #Could bump into a straight flush
        flushed = flushes(cards)
        maxflush = max([len(v) for v in flushed])
        if maxflush >= 4:
            for card in cards: wset.populate("Suit",card)
    #Calculate max and min rank
    ranks = [group[0].rank() for group in grouped if len(group) != 0]
    mn = min(ranks)
    mx = max(ranks)
    ranks.sort()
    if 1 in ranks:
        spanlo = abs(1-max(ranks))
        spanhi = abs(ranks[1]-14)
        if min(spanhi,spanlo) == spanlo:
            mx = max(ranks)
            mn = 1
        else:
            mx = 14
            mn = ranks[1]
        span = abs(mx-mn)
    else:
        span = abs(min(ranks)-max(ranks))
    if span > 4:  #No good - cards we have are too far apart
        rset.clear()
        return rset
    
    rset.clear()
    adj = 4-span
    for rank in set(range(mn-adj,mx+adj+1)).difference(invalid):
        rset.populate("Rank",rank)
    for card in cards:
        wset.populate("Rank",card.rank())
    return rset.difference(wset).difference(exclude)

def isStraight(cards):
    if not isinstance(cards,stacks.stack):
        raise NotImplementedError, "isStraight only works on stacks"
    rset = stacks.stack()
    
    if len(cards) != 5:
        return False
        
    hand = set([crd.rank() for crd in cards])
    if 1 in hand: hand.add(14)
    for low in range(10,0,-1):
        needed = set(range(low, low+5))
        if len(needed.intersection(hand)) == 5:
            return True
    return False
    
def toMakeThreeOAK(cards):
    if not isinstance(cards,stacks.stack):
        raise NotImplementedError, "toMakeThreeOAK only works on stacks"
    
    rset = stacks.stack()
    rset.populate("Full Deck")
    if (len(cards) < 1):  #No cards played yet - anything will work
        return rset
    if (len(cards) > 4):  #Five cards played - nothing else will work
        rset.clear()
        return rset
        
    grouped = groups(cards)
    wset = stacks.stack()
    maxgroup = max([len(v) for v in grouped]) #Calculates the number of cards in the rank with the most cards
    if maxgroup == len(cards):  #All cards are in the same rank
        if maxgroup > 3:  #Already a 4OAK - nothing will work
            rset.clear()
            return rset
        if maxgroup == 3:  #A 3OAK - anything will work except another of the same rank
            for card in cards: wset.populate("Rank",card)
            return rset.difference(wset)
        if maxgroup < 3:  #A safe pair - anything except the given cards will work
            return rset.difference(cards)
    if maxgroup == len(cards)-1:  #3OAK +1, Pair+1, or split
        if maxgroup == 3:  #Need to avoid full house and 4 OAK - cannot be of either rank we already have
            for group in filter(None,grouped):
                wset.populate("Rank",group[0])
            return rset.difference(wset)                
        if maxgroup < 3:
            return rset.difference(cards)
    if maxgroup == len(cards)-2: # 2-1-1,2-2,1-1-1,
        if (maxgroup == 2) and (len(filter(None,grouped)) == 2): #Can't win - anything is a full house
            rset.clear()
            return rset
        elif (maxgroup == 2) and (len(filter(None,grouped)) == 3):
            rset.clear()
            for group in grouped:
                if len(group) == 2:
                    rset.populate("Rank",group[0])
                    return rset.difference(cards)
        else:
            rset.clear()
            for card in cards:
                rset.populate("Rank",card)
            return rset.difference(cards)
    else:  #There are already too many non-matching cards - nothing will work
        rset.clear()
        return rset

def isThreeOAK(cards):
    if not isinstance(cards,stacks.stack):
        raise NotImplementedError, "isThreeOAK only works on stacks"
    rset = stacks.stack()
    
    if len(cards) != 5:
        return False
        
    grouped = [len(group) for group in groups(cards) if len(group) != 0]
    if max(grouped) >= 3:
        return True
    else:
        return False

def toMakeTwoPair(cards):
    if not isinstance(cards,stacks.stack):
        raise NotImplementedError, "toMakeTwoPair only works on stacks"
    
    rset = stacks.stack()
    rset.populate("Full Deck")
    if (len(cards) < 1):  #No cards played yet - anything will work
        return rset
    if (len(cards) > 4):  #Five cards played - nothing else will work
        rset.clear()
        return rset
        
    grouped = groups(cards)
    wset = stacks.stack()
    maxgroup = max([len(v) for v in grouped]) #Calculates the number of cards in the rank with the most cards
    if maxgroup > 2: #Already a 3OAK or better - nothing will work
        rset.clear()
        return rset
    if len(filter(None,grouped)) > 3:  #Have more than 3 unique cards - nothing will work
        rset.clear()
        return rset
    if maxgroup == 2:
        if len(cards) == 4: #Either 2-1-1 or 2-2
            if len(filter(None,grouped)) == 3:
                rset.clear()
                for group in grouped:
                    if len(group) == 1:
                        rset.populate("Rank",group[0])
                    if len(group) == 2:
                        wset.populate("Rank",group[0])
                return rset.difference(wset).difference(cards)
            else:
                for group in grouped:
                    if len(group) > 0: wset.populate("Rank",group[0])
                return rset.difference(wset).difference(cards)
        if len(cards) <= 3:
            for group in grouped:
                if len(group) == 2:
                    wset.populate("Rank",group[0])
            return rset.difference(cards).difference(wset)
    if maxgroup == 1:  
        if len(cards) == 3: #3 unique cards
            rset.clear()
            for card in cards: rset.populate("Rank",card)
            return rset.difference(cards)
        else:
            return rset.difference(cards)   
    
def isTwoPair(cards):
    if not isinstance(cards,stacks.stack):
        raise NotImplementedError, "isTwoPair only works on stacks"
    rset = stacks.stack()
    
    if len(cards) != 5:
        return False
        
    grouped = [len(group) for group in groups(cards) if len(group) != 0]
    grouped.sort()
    if grouped == [1,2,2]:
        return True
    else:
        return False
    
def toMakePair(cards):
    if not isinstance(cards,stacks.stack):
        raise NotImplementedError, "toMakePair only works on stacks"
    rset = stacks.stack()
    rset.populate("Full Deck")
    wset = stacks.stack()
    if (len(cards) < 1):  #No cards played yet - anything will work
        return rset
    if (len(cards) > 4):  #Five cards played - nothing else will work
        rset.clear()
        return rset
    
    grouped = groups(cards)
    maxgroup = max([len(v) for v in grouped]) #Calculates the number of cards in the rank with the most cards
    if maxgroup > 2: #Already a 3OAK or better, nothing will work
        rset.clear()
        return rset
        
    if len(cards) == 4:
        paircount = 0
        if maxgroup == 2: #A pair+2 or two pair.  Need to avoid matching cards we already have.
            for group in grouped:
                if len(group) == 0: continue
                if len(group) == 1: # Pair +2 - need to avoid the single cards to prevent making 2 pair 
                    wset.clear()
                    wset.populate("Rank",group[0])
                    rset = rset.difference(wset)
                if len(group) == 2:
                    if paircount >= 1: # Have two pairs, nothing will work
                        rset.clear()
                        return rset
                    wset.clear()
                    wset.populate("Rank",group[0])
                    rset = rset.difference(wset)
                    paircount+=1
        if maxgroup == 1: #All unique cards - need a match of the same rank from a different suit
            rset.clear()
            for card in cards: rset.populate("Rank",card)
            return rset.difference(cards)
                    
    if len(cards) == 3:
        if maxgroup == 2: #A pair+1.  Need to avoid matching cards we already have.
            for group in grouped:
                if len(group) == 0: continue
                else:
                    wset.clear()
                    wset.populate("Rank",group[0])
                    rset = rset.difference(wset)
        if maxgroup == 1: #Three unique cards - we can take anything
            return rset.difference(cards)
    
    if len(cards) == 2:
        if maxgroup == 2:  #A perfect pair - we can accept anything that doesn't make a 3OAK
            wset.clear()
            for card in cards: wset.populate("Rank",card)
            return rset.difference(wset)
        if maxgroup == 1:  #Two different cards - we can accept anything
            return rset.difference(cards)

    if len(cards) == 1:
        return rset.difference(cards)
        
    return rset

def isPair(cards):
    if not isinstance(cards,stacks.stack):
        raise NotImplementedError, "isPair only works on stacks"
    rset = stacks.stack()
    
    if len(cards) != 5:
        return False
        
    grouped = [len(group) for group in groups(cards) if len(group) != 0]
    if max(grouped) >= 2:
        return True
    else:
        return False
