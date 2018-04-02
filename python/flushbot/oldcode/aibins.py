import stacks,hands,game

class groups:

class groups2:

    def __init__(self):
        self.favor = {"RoyalFlush" : game.score["RoyalFlush"],
                      "StraightFlush" : game.score["StraightFlush"],
                      "FourOAK" : game.score["FourOAK"],
                      "FullHouse" : game.score["FullHouse"],
                      "Flush" : game.score["Flush"],
                      "Straight" : game.score["Straight"],
                      "ThreeOAK" : game.score["ThreeOAK"],
                      "TwoPair" : game.score["TwoPair"],
                      "Pair" : game.score["Pair"]}

    def feeder(self,game,card,remaining):
        if len(remaining) == 51:
            game.addcard(1,card)
            return
        placed = False
        bestprob = 0
        bestbin = 4
        besthand = ""
        for bin in range(1,5):
            binprob = 0
            for name in game.complete.keys():
                if not game.complete[name]:
                    function = getattr(hands, "is%s" % name)
                    if function(game.getbin(bin).union([card])):
                        game.addcard(bin,card)
                        placed = True
                    break
            if placed: break
            
            for name in game.complete.keys():
                function = getattr(hands, "toMake%s" % name)
                top = float(len(function(game.getbin(bin).union([card])).intersection(remaining)))
                bottom = float(len(remaining)+1)
                prob = top / bottom
                if game.complete[name]:
                    adjprob = 0
                else:
                    adjprob = prob * self.favor[name]
                #if(adjprob != 0): print "|Bin|",bin,len(game.getbin(bin)),"|Hand|",name,"|Prob|",prob,"|Adjprob|",adjprob,"|Favor|",self.favor[name]
            
                binprob += adjprob
            
            if (binprob == 0) and (len(game.getbin(bin))) < 4:
                game.emptybin(bin)
                
            if binprob > bestprob:
                bestbin = bin
                bestprob = binprob

        #print besthand,bestprob,bestbin

        if not placed:
            if bestprob > 0:
                game.addcard(bestbin,card)
            else:
                game.addcard(4,card)
    def __init__(self):
        self.favor = {"RoyalFlush" : game.score["RoyalFlush"],
                      "StraightFlush" : game.score["StraightFlush"],
                      "FourOAK" : game.score["FourOAK"],
                      "FullHouse" : game.score["FullHouse"],
                      "Flush" : game.score["Flush"],
                      "Straight" : game.score["Straight"],
                      "ThreeOAK" : game.score["ThreeOAK"],
                      "TwoPair" : game.score["TwoPair"],
                      "Pair" : game.score["Pair"]}
        self.target = ["FourOAK","Straight","Flush","ThreeOAK","TwoPair","Pair"]
        self.target1 = "RoyalFlush"
        self.target2 = "StraightFlush"
        self.target3 = "FullHouse"

    def feeder(self,game,card,remaining):
        
        game.raisebin(1)
        game.raisebin(2)
        game.raisebin(3)        
        
        function = getattr(hands, "toMake%s" % self.target1)
        if card in function(game.getbin(1)):
            game.addcard(1,card)
            if len(game.getbin(1)) == 5:
                self.target1 = self.target.pop(0)
            return
        
        function = getattr(hands, "toMake%s" % self.target2)
        if card in function(game.getbin(2)):
            game.addcard(2,card)
            if len(game.getbin(2)) == 5:
                self.target2 = self.target.pop(0)
            return

        function = getattr(hands, "toMake%s" % self.target3)
        if card in function(game.getbin(3)):
            game.addcard(3,card)
            if len(game.getbin(3)) == 5:
                self.target3 = self.target.pop(0)
            return
        
        game.addcard(4,card)

        prob = 0
        for name in game.complete.keys():
            function = getattr(hands, "toMake%s" % name)
            top = float(len(function(game.getbin(4)).intersection(remaining)))
            bottom = float(len(remaining)+1)
            prob = top / bottom
                
        if (prob == 0) and (len(game.getbin(4))) < 4:
            game.emptybin(4)