
class lookupai:

    def __init__(self):
        self.favor = {'R' : game.score["RoyalFlush"],
                      'T' : game.score["StraightFlush"],
                      '4' : game.score["FourOAK"],
                      'H' : game.score["FullHouse"],
                      'F' : game.score["Flush"],
                      'S' : game.score["Straight"],
                      '3' : game.score["ThreeOAK"],
                      'X' : game.score["TwoPair"],
                      'P' : game.score["Pair"],
                      'N' : 0}
        self.trslt = {"RoyalFlush" : 'R',
                      "StraightFlush" : 'T',
                      "FourOAK" : '4',
                      "FullHouse" : 'H',
                      "Flush" : 'F',
                      "Straight" : 'S',
                      "ThreeOAK" : '3',
                      "TwoPair" : 'X',
                      "Pair" : 'P'}
        self.lock  = {'R' : 0,
                      'T' : 0,
                      '4' : 0,
                      'H' : 0,
                      'F' : 0,
                      'S' : 0,
                      '3' : 0,
                      'X' : 0,
                      'P' : 0}
        print "Loading pickle"
        self.lu = lookup.lookup("C:\\data2.pkl")
        print "Done loading pickle"


    def feeder(self,game,card,remaining):
        
        remw = {}
        remwo = {}
        binw = {}
        binwo = {}
        ratiow = {}
        ratiowo = {}
        mask = stacks.stack()
        bins = set([1,2,3,4])
        
        #Calculate what bins can make when using feeder card
        for b in bins:
            mask.clear()
            for i in bins.difference([b]): mask = mask.union(game.getbin(i))
            binw[b] = self.lu.canmake(game.getbin(b).union([card]), mask)
                                     
        #Check if card fits in a locked bin
        needcard = []
        for k,v in self.lock.items():
            if (v != 0) and (k in binw[v]): #There is a lock and the locked hand needs it
                needcard.append((k,v)) #Make a list of hand/bin in case more than one bin needs card
        if len(needcard) == 1:
            game.addcard(needcard[0][1])
            return
        elif len(needcard) > 1:  #TODO: Make multiple locked hands work
            raise NotImplementedError, "Ahhh! More than one locked hand!"
            return
        
        #Calculate what hands can be made with remaining cards (w/ and w/o feeder)
        mask.clear()
        mask = mask.union(game.discard)
        for b in bins: mask = mask.union(game.getbin(i))
        remwo = self.lu.canmake(stacks.stack(), mask)
        mask = mask.union([card])
        remw = self.lu.canmake(stacks.stack(), mask)
        
        #Are there any hands that playing this card will make it so we can't make anymore?
        for n in [k for k in remw if k not in remwo]:
            bestbin = 0
            bestlen = 0
            for i in [b for b in bins if n in binw[b]]:
                if len(game.getbin(i)) > bestlen:
                    bestlen = len(game.getbin(i))
                    bestbin = i
            if bestbin == 0:  #No bins are started
                canuse = bins.difference([v for k,v in self.lock.items() if v != 0]) #Bins with a lock
                random.shuffle(canuse) #TODO: Randomly picking bin - pick lowest value
                game.emptybin(canuse[0])
                game.addcard(canuse[0], card)
                self.lock[n] = canuse[0]
            else:
                game.addcard(bestbin, card)
                self.lock[n] = bestbin

        #Calculate what bins can make without using feeder card
        for b in bins:
            mask.clear()
            for i in bins.difference([b]): mask = mask.union(game.getbin(i))
            mask.union([card])
            binwo[b] = self.lu.canmake(game.getbin(b), mask)

        #Calculate ratio of hands/nothing for each bin.  Only need non-locked bins.
        for i in bins.difference([v for k,v in self.lock.items() if v != 0]):
            binwN, binwoN = 1, 1
            sumw, sumwo = 0, 0
            exclude = [self.trslt[k] for k in game.complete.keys() if game.complete[k] == True] + ['N']
            if 'N' in binw[i]: binwN = binw[i]['N']
            if 'N' in binwo[i]: binwoN = binwo[i]['N']
            sumw = sum([v for k,v in binw[i].items() if k not in exclude])
            sumwo = sum([v for k,v in binwo[i].items() if k not in exclude])
            ratiow[i] = float(sumw) / float(binwN)
            ratiowo[i] = float(sumwo) / float(binwoN)
        
        print ratiow
            
        #Figure out the bin with the best ratio
        bestbin = 0
        bestratio = 0
        for k, v in ratiow.items():
            if v > bestratio:
                bestratio = v
                bestbin = k
                
        #Put card in that bin
        game.addcard(bestbin, card)
        