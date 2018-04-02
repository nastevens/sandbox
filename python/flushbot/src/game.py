import stacks,hands

''' Describes which hands are a superset of of a lesser hand.  For example,
a pair exists in a 3-of-a-kind, but we would choose the 3-of-a-kind over
the pair '''
superset = {'R': (),
            'T': ('R'),
            '4': (),
            'H': (),
            'F': ('T','R'),
            'S': ('T','R'),
            '3': ('H','4'),
            'X': ('H'),
            'P': ('X','3','H','4') }

expanded = {'R': "RoyalFlush",
            'T': "StraightFlush",
            '4': "FourOAK",
            'H': "FullHouse",
            'F': "Flush",
            'S': "Straight",
            '3': "ThreeOAK",
            'X': "TwoPair",
            'P': "Pair",
            'N': "Nothing",
            'D': "Duplicate"}

multiplier = {0: 2.0, 1: 1.8, 2: 1.6, 3: 1.4, 4: 1.2, 'default': 1.0}
 
class gamestate:
    
    def __init__(self):
        self.complete = {'R': False, 'T': False, '4': False, 'H': False, 'F': False,
                         'S': False, '3': False, 'X': False, 'P': False}
        self.raised = {1: 1.0, 2: 1.0, 3: 1.0, 4: 1.0}
        self.completecount = 0
        tmpstack = stacks.stack()
        tmpstack.populate("Full Deck")
        self.bins = {1: stacks.stack(), 2: stacks.stack(), 3: stacks.stack(), 4: stacks.stack(),
                     'discard': stacks.stack(), 'remaining': tmpstack}      
        self.score = {'R': 500, 'T': 450, '4': 400, 'H': 350, 'F': 300, 'S': 250, 
                      '3': 200, 'X': 100, 'P': 50, 'N': -50, 'D': -50}
        self.totalscore = 0
        self.penalties = 0
        self.raises = 4

    def addcard(self, bin, card):
        if not self.validbin(bin):
            raise RuntimeError, "Invalid bin", bin
        if card not in self.bins['remaining']:
            raise RuntimeError, "Card to add not found in remaining cards"
        self.bins['remaining'].remove(card)
        self.bins[bin].add(card)
        self.checkcomplete(bin)
        
    def foldbin(self, bin):
        if not self.validbin(bin):
            raise RuntimeError, "Invalid bin", bin
        self.bins['discard'].update(self.bins[bin])
        self.bins[bin].clear()
        self.raised[bin] = multiplier['default'] 

    def raisebin(self, bin):
        if not self.validbin(bin):
            raise RuntimeError, "Invalid bin", bin
        if self.raises <= 0 or self.raised[bin] > multiplier['default']:
            return
        else:
            self.raised[bin] = multiplier[len(self.bins[bin])]
            self.raises -= 1
                       
    def getbin(self, bin):
        if not self.validbin(bin):
            raise RuntimeError, "Invalid bin", bin
        return self.bins[bin]
        
    def checkcomplete(self, bin):
        if not self.validbin(bin):
            raise RuntimeError, "Invalid bin", bin
        for k, v in self.complete.iteritems():
            hassuper = False
            for super in superset[k]:
                function = getattr(hands, "is%s" % expanded[super])
                if function(self.bins[bin]): hassuper = True
            if hassuper: continue
            
            function = getattr(hands, "is%s" % expanded[k])
            if function(self.bins[bin]):
                self.totalscore += self.raised[bin]*self.score[k]
                if not self.complete[k]: self.completecount += 1 
                self.complete[k] = True
                self.score[k] = self.score['D']
                self.bins[bin].clear()
                self.raised[bin] = multiplier['default']
                
        if len(self.bins[bin]) == 5:
            self.totalscore += self.score['N']
            self.penalties += -self.score['N']
            self.bins[bin].clear()
            self.raised[bin] = multiplier['default']
    
    
    def completelist(self):
        completelist = [int(self.complete['R']), int(self.complete['T']),
                        int(self.complete['4']), int(self.complete['H']),
                        int(self.complete['F']), int(self.complete['S']),
                        int(self.complete['3']), int(self.complete['X']),
                        int(self.complete['P'])]
        return completelist

    def validbin(self, bin):
        if bin not in self.bins.keys():
            return False
        else:
            return True
    
    def dumpbins(self):
        print "======"
        print "Bins status:"
        for k,v in self.bins.iteritems():
            print "Bin",k,':',v
        print "======"
        
    def dumpcomplete(self):
        print "======"
        print "Completed status:"
        for k, v in self.complete.iteritems():
            print k, ':', v
        print "======"
