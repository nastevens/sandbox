import ai, game, stacks
from card import card

def main():
    agent = ai.lookaheadai()
    state = game.gamestate()
    tmpstack = stacks.stack()
    tmpstack.populate("Full Deck")
    deck = tmpstack.getAsRandomList()
    print len(deck)
    while len(deck) > 0:
        next = deck.pop()
        print "Feeding", next
        agent.feeder(state, next)
        
    print state.totalscore, state.handscompleted()
            
if __name__ == '__main__': main() 
