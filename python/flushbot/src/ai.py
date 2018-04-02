import stacks, hands, game, copy
from card import card

class lookaheadai:
 
    def feeder(self,game,card):
        if len(game.getbin('remaining')) == 52:
            game.addcard(1,card)
            return
        nextaction = self.actionvalues(game,card,0,2)
        print nextaction
        if int(nextaction[0]) > 0:
            game.addcard(int(nextaction[0]), card)
        else:
            game.foldbin(-int(nextaction[0]))
    
    def actionvalues(self,game,known,depth,maxdepth):
        if depth == maxdepth: return ('1',0)
        bestvalue = -99999
        bestaction = '1'
        for bin in range(1,5):
            gamecopy = copy.deepcopy(game)
            gamecopy.totalscore = 0
            gamecopy.addcard(bin,known)
            playvalue = gamecopy.totalscore
            gamecopy.totalscore = 0
            for card in gamecopy.getbin('remaining'):
                gamecopy.totalscore += self.actionvalues(gamecopy,card,depth+1,maxdepth)[1]
            #Calculate the average
            avvalue = ((gamecopy.totalscore / len(gamecopy.getbin('remaining'))) + playvalue) / 2
            if avvalue > bestvalue:
                bestvalue = avvalue
                bestaction = str(bin)
            gamecopy = copy.deepcopy(game)
            gamecopy.totalscore = 0
            gamecopy.foldbin(bin)
            value = self.actionvalues(gamecopy,known,depth+1,maxdepth)[1]
            if value > bestvalue:
                bestvalue = value
                bestaction = str(-bin)
        #check discards
        #check raises
        return (bestaction, bestvalue)