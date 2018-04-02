import cPickle, stacks
from card import card
from itertools import groupby

class lookup():
    
    def __init__(self, pkl):
        FILE = open(pkl,"rb")
        self.table = cPickle.load(FILE)
        self.cache = {}
            
    def canmake(self,cards,mask):
        masklist = [x.value() for x in mask]
        masklist.sort()
        t = tuple(masklist)
        if len(cards) == 0:
            haveset = set([])
            if t in self.cache:
                return self.cache[t]
            for i in range(1,53): haveset = haveset.union(self.table[i])
        else:
            cardlist = [x.value() for x in cards]
            haveset = self.table[cardlist[0]]
            for i in cardlist: haveset = haveset.intersection(self.table[i])
        masklist = [x.value() for x in mask]
        maskset = set([])
        for i in masklist: maskset = maskset.union(self.table[i])
        goodset = haveset.difference(maskset)
        value = {}
        for i in goodset:
            value[i[5]] = value.get(i[5],0)+1
        if len(cards) == 0:
            self.cache[t] = value
        return value

if __name__ == '__main__':
    lu = lookup("C:\\data2.pkl")
    v = lu.canmake(stacks.stack([card(30)]),stacks.stack())
    print v