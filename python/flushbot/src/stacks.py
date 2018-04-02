import os, random
from card import *

class stack(set):
    
    def __init__(self,iter=None):
        if iter:
            for a in iter:
                self.add(a)

    def add(self,item):
        if isinstance(item,card):
            set.add(self,item)
            return
        raise NotImplementedError, "Cannot add non-card objects to stack"
            
    def dumpStack(self):
        for card in self:
            print card
            
    def getAsRandomList(self):
        rlist = list(self)
        for i in range(1,1000): random.shuffle(rlist)
        return rlist
    
    def populate(self, type="Empty", subtype="None"):
        ranklist = []
        suitlist = []
    
        if type == "Full Deck": ranklist,suitlist = range(1,14),range(1,5)
        if type == "Face Cards":
            if isinstance(subtype,card):
                ranklist,suitlist = range(11,14),[subtype.suit()]
            elif subtype=="None":
                ranklist,suitlist = range(11,14),range(1,5)
            else:
                ranklist,suitlist = range(11,14),[subtype]
        if type == "Royal Flush":
            if isinstance(subtype,card):
                ranklist,suitlist = [1,10,11,12,13],[subtype.suit()]
            elif subtype == "None":
                ranklist,suitlist = [1,10,11,12,13],range(1,5)
            else:
                ranklist,suitlist = [1,10,11,12,13],[subtype]
        if type == "Suit":
            if isinstance(subtype,card):
                ranklist,suitlist = range(1,14), [subtype.suit()]
            else:
                ranklist,suitlist = range(1,14), [subtype]
        if type == "Rank":
            if isinstance(subtype,card):
                ranklist,suitlist = [subtype.rank()], range(1,5)
            else:
                ranklist,suitlist = [subtype],range(1,5)
        for rank in ranklist:
            for suit in suitlist:
                self.add(card(rank,suit))

def empty():
    return stack()