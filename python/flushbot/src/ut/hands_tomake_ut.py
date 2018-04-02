'''Unittest test suite for tomake* functions in hands.py''' 
import hands
import unittest
import stacks
from card import card

class Pair(unittest.TestCase): #All done
    '''hands.toMakePair test functions'''
    
    def testBogus(self):
        '''Pair_testBogus: Should fail if not given a stack'''
        self.assertRaises(NotImplementedError, hands.toMakePair, 5)
        
    def testEmpty(self):
        '''Pair_testEmpty: Should return full deck if given no input'''
        teststack = stacks.stack()
        teststack.populate("Full Deck")
        result = hands.toMakePair(stacks.stack())
        self.assertEqual(result,teststack)
        
    def testA(self):
        '''Pair_testA: Should return full deck except A'''
        teststack = stacks.stack()
        teststack.add(card(1,1))
        result = hands.toMakePair(teststack)
        workstack = stacks.stack()
        workstack.populate("Full Deck")
        workstack = workstack.difference([card(1,1)])
        self.assertEqual(result,workstack)
        
    def testAA(self):
        '''Pair_testAA: Should return full deck minus cards in A rank'''
        teststack = stacks.stack()
        teststack.add(card(1,1))
        teststack.add(card(1,2))
        result = hands.toMakePair(teststack)
        workstack = stacks.stack()
        workstack.populate("Full Deck")
        workstack = workstack.difference([card(1,1),card(1,2),card(1,3),card(1,4)])
        self.assertEqual(result,workstack)
        
    def testAB(self):
        '''Pair_testAB: Should return full deck minus cards given'''
        teststack = stacks.stack()
        teststack.add(card(1,1))
        teststack.add(card(2,2))
        result = hands.toMakePair(teststack)
        workstack = stacks.stack()
        workstack.populate("Full Deck")     
        workstack = workstack.difference(teststack)
        self.assertEqual(result,workstack)
    
    def testAAA(self):
        '''Pair_testAAA: Should return nothing (more than a pair)'''
        teststack = stacks.stack()
        teststack.add(card(1,1))
        teststack.add(card(1,2))
        teststack.add(card(1,3))
        result = hands.toMakePair(teststack)
        self.assertEqual(result,stacks.stack())

    def testAAB(self):
        '''Pair_testAAB: Should return full deck except cards in A, B ranks'''
        teststack = stacks.stack()
        teststack.add(card(1,1))
        teststack.add(card(1,2))
        teststack.add(card(2,2))
        result = hands.toMakePair(teststack)
        workstack = stacks.stack()
        workstack.populate("Rank",card(1,1))
        workstack.populate("Rank",card(2,2))
        goodstack = stacks.stack()
        goodstack.populate("Full Deck")
        goodstack = goodstack.difference(workstack)
        self.assertEqual(result,goodstack)
        
    def testABC(self):
        '''Pair_testABC: Should return full deck minus A,B,C'''
        teststack = stacks.stack()
        teststack.add(card(1,1))
        teststack.add(card(2,2))
        teststack.add(card(3,3))
        result = hands.toMakePair(teststack)
        workstack = stacks.stack()
        workstack.populate("Full Deck")
        workstack = workstack.difference(teststack)
        self.assertEqual(result,workstack)

    def testAAAA(self):
        '''Pair_testAAAA: Should return nothing (more than a pair)'''
        teststack = stacks.stack()
        teststack.add(card(1,1))
        teststack.add(card(1,2))
        teststack.add(card(1,3))
        teststack.add(card(1,4))
        result = hands.toMakePair(teststack)
        self.assertEqual(result,stacks.stack())
        
    def testAAAB(self):
        '''Pair_testAAAB: Should return nothing (more than a pair)'''
        teststack = stacks.stack()
        teststack.add(card(1,1))
        teststack.add(card(1,2))
        teststack.add(card(1,3))
        teststack.add(card(2,1))
        result = hands.toMakePair(teststack)
        self.assertEqual(result,stacks.stack())      

    def testAABB(self):
        '''Pair_testAABB: Should return nothing'''
        teststack = stacks.stack()
        teststack.add(card(1,1))
        teststack.add(card(1,2))
        teststack.add(card(2,1))
        teststack.add(card(2,2))
        result = hands.toMakePair(teststack)
        self.assertEqual(result,stacks.stack())
        
    def testAABC(self):
        '''Pair_testAABC: Should return full deck minus cards in A,B,C ranks'''
        teststack = stacks.stack()
        teststack.add(card(1,1))
        teststack.add(card(1,2))
        teststack.add(card(2,2))
        teststack.add(card(3,3))
        result = hands.toMakePair(teststack)
        workstack = stacks.stack()
        workstack.populate("Rank",card(1,1))
        workstack.populate("Rank",card(1,2))
        workstack.populate("Rank",card(2,2))
        workstack.populate("Rank",card(3,3))
        goodstack = stacks.stack()
        goodstack.populate("Full Deck")
        goodstack = goodstack.difference(workstack)
        self.assertEqual(result,goodstack)
        
    def testABCD(self):
        '''Pair_testABCD: Should return cards in ranks A,B,C,D except A,B,C,D themselves'''
        teststack = stacks.stack()
        teststack.add(card(1,1))
        teststack.add(card(2,2))
        teststack.add(card(3,3))
        teststack.add(card(4,4))
        result = hands.toMakePair(teststack)
        workstack = stacks.stack()
        workstack.populate("Rank",card(1,1))
        workstack.populate("Rank",card(2,2))
        workstack.populate("Rank",card(3,3))
        workstack.populate("Rank",card(4,5))
        workstack = workstack.difference(teststack)
        self.assertEqual(result,workstack)
        
    def testFive(self):
        '''Pair_testFive: Should return nothing'''
        teststack = stacks.stack()
        teststack.add(card(1,1))
        teststack.add(card(2,2))
        teststack.add(card(3,3))
        teststack.add(card(4,4))
        teststack.add(card(5,5))
        result = hands.toMakePair(teststack)
        self.assertEqual(result,stacks.stack())
        
class TwoPair(unittest.TestCase): #All done
    def testBogus(self):
        '''TwoPair_testBogus: Should fail if not given a stack'''
        self.assertRaises(NotImplementedError, hands.toMakeTwoPair, 5)
        
    def testEmpty(self):
        '''TwoPair_testEmpty: Should return full deck if given no input'''
        teststack = stacks.stack()
        teststack.populate("Full Deck")
        result = hands.toMakeTwoPair(stacks.stack())
        self.assertEqual(result,teststack)
        
    def testA(self):
        '''TwoPair_testA: Should return all cards except A'''
        teststack = stacks.stack()
        teststack.add(card(1,1))
        result = hands.toMakeTwoPair(teststack)
        workstack = stacks.stack()
        workstack.populate("Full Deck")
        workstack = workstack.difference(teststack)
        self.assertEqual(result,workstack)
        
    def testAA(self):
        '''TwoPair_testAA: Should return all cards those in A rank'''
        teststack = stacks.stack()
        teststack.add(card(1,1))
        teststack.add(card(1,2))
        result = hands.toMakeTwoPair(teststack)
        workstack = stacks.stack()
        workstack.populate("Full Deck")
        workstack = workstack.difference([card(1,1),card(1,2),card(1,3),card(1,4)])
        self.assertEqual(result,workstack)
        
    def testAB(self):
        '''TwoPair_testAB: Should return all cards except A and B'''
        teststack = stacks.stack()
        teststack.add(card(1,1))
        teststack.add(card(2,2))
        result = hands.toMakeTwoPair(teststack)
        workstack = stacks.stack()
        workstack.populate("Full Deck")     
        workstack = workstack.difference(teststack)
        self.assertEqual(result,workstack)
        
    def testAAA(self):
        '''TwoPair_testAAA: Should return nothing'''
        teststack = stacks.stack()
        teststack.add(card(1,1))
        teststack.add(card(1,2))
        teststack.add(card(1,3))
        result = hands.toMakeTwoPair(teststack)
        self.assertEqual(result,stacks.stack())
        
    def testAAB(self):
        '''TwoPair_testAAB: Should return all cards except in A rank and B'''
        teststack = stacks.stack()
        teststack.add(card(1,1))
        teststack.add(card(1,2))
        teststack.add(card(2,1))
        result = hands.toMakeTwoPair(teststack)
        workstack = stacks.stack()
        workstack.populate("Full Deck")     
        workstack = workstack.difference([card(1,1),card(1,2),card(1,3),card(1,4),card(2,1)])
        self.assertEqual(result,workstack)
        
    def testABC(self):
        '''TwoPair_testABC: Should return cards in A,B,or C's rank except A,B,and C'''
        teststack = stacks.stack()
        teststack.add(card(1,1))
        teststack.add(card(2,1))
        teststack.add(card(3,1))
        result = hands.toMakeTwoPair(teststack)
        workstack = stacks.stack()
        workstack.populate("Rank",card(1,1))
        workstack.populate("Rank",card(2,1))
        workstack.populate("Rank",card(3,1))
        self.assertEqual(result,workstack.difference(teststack))

    def testAAAA(self):
        '''TwoPair_testAAAA: Should return nothing'''
        teststack = stacks.stack()
        teststack.add(card(1,1))
        teststack.add(card(1,2))
        teststack.add(card(1,3))
        teststack.add(card(1,4))
        result = hands.toMakeTwoPair(teststack)
        self.assertEqual(result,stacks.stack())

    def testAAAB(self):
        '''TwoPair_testAAAB: Should return nothing'''
        teststack = stacks.stack()
        teststack.add(card(1,1))
        teststack.add(card(1,2))
        teststack.add(card(1,3))
        teststack.add(card(2,1))
        result = hands.toMakeTwoPair(teststack)
        self.assertEqual(result,stacks.stack())
        
    def testAABB(self):
        '''TwoPair_testAABB: Should return all cards except those in A and B's ranks'''
        teststack = stacks.stack()
        teststack.add(card(1,1))
        teststack.add(card(1,2))
        teststack.add(card(2,1))
        teststack.add(card(2,2))
        result = hands.toMakeTwoPair(teststack)
        workstack = stacks.stack()
        workstack.populate("Rank",card(1,1))
        workstack.populate("Rank",card(2,1))
        goodstack = stacks.stack()
        goodstack.populate("Full Deck")
        goodstack = goodstack.difference(workstack)
        self.assertEqual(result,goodstack)
        
    def testAABC(self):
        '''twoPair_testAABC: Should return cards in B or C's ranks except B or C'''
        teststack = stacks.stack()
        teststack.add(card(1,1))
        teststack.add(card(1,2))
        teststack.add(card(2,1))
        teststack.add(card(3,1))
        result = hands.toMakeTwoPair(teststack)
        workstack = stacks.stack()
        workstack.populate("Rank",card(2,1))
        workstack.populate("Rank",card(3,1))
        self.assertEqual(result,workstack.difference(teststack))
        
    def testABCD(self):
        '''twoPair_testABCD: Should return nothing'''
        teststack = stacks.stack()
        teststack.add(card(1,1))
        teststack.add(card(2,1))
        teststack.add(card(3,1))
        teststack.add(card(4,1))
        result = hands.toMakeTwoPair(teststack)
        self.assertEqual(result,stacks.stack())
        
    def testFive(self):
        '''twoPair_testFive: Should return nothing'''
        teststack = stacks.stack()
        teststack.add(card(1,1))
        teststack.add(card(1,2))
        teststack.add(card(1,3))
        teststack.add(card(1,4))
        teststack.add(card(2,1))
        result = hands.toMakeTwoPair(teststack)
        self.assertEqual(result,stacks.stack())
        
class ThreeOAK(unittest.TestCase): #All done
    def testBogus(self):
        '''ThreeOAK_testBogus: Should fail if not given a stack'''
        self.assertRaises(NotImplementedError, hands.toMakeThreeOAK, 5)
        
    def testEmpty(self):
        '''ThreeOAK_testEmpty: Should return full deck if given no input'''
        teststack = stacks.stack()
        teststack.populate("Full Deck")
        result = hands.toMakeThreeOAK(stacks.stack())
        self.assertEqual(result,teststack)
        
    def testA(self):
        '''ThreeOAK_testA: Should return all cards except A'''
        teststack = stacks.stack()
        teststack.add(card(1,1))
        result = hands.toMakeThreeOAK(teststack)
        workstack = stacks.stack()
        workstack.populate("Full Deck")
        workstack = workstack.difference(teststack)
        self.assertEqual(result,workstack)
        
    def testAA(self):
        '''ThreeOAK_testAA: Should return all cards except A's'''
        teststack = stacks.stack()
        teststack.add(card(1,1))
        teststack.add(card(1,2))
        result = hands.toMakeThreeOAK(teststack)
        workstack = stacks.stack()
        workstack.populate("Full Deck")
        workstack = workstack.difference(teststack)
        self.assertEqual(result,workstack)
    
    def testAB(self):
        '''ThreeOAK_testAB: Should return all cards except A and B'''
        teststack = stacks.stack()
        teststack.add(card(1,1))
        teststack.add(card(2,2))
        result = hands.toMakeThreeOAK(teststack)
        workstack = stacks.stack()
        workstack.populate("Full Deck")
        workstack = workstack.difference(teststack)
        self.assertEqual(result,workstack)
        
    def testAAA(self):
        '''ThreeOAK_testAAA: Should return all cards except cards in A rank'''
        teststack = stacks.stack()
        teststack.add(card(1,1))
        teststack.add(card(1,2))
        teststack.add(card(1,3))
        result = hands.toMakeThreeOAK(teststack)
        workstack = stacks.stack()
        workstack.populate("Full Deck")
        workstack = workstack.difference(teststack).difference([card(1,4)])
        self.assertEqual(result,workstack)
    
    def testAAB(self):
        '''ThreeOAK_testAAB: Should return all cards except input'''
        teststack = stacks.stack()
        teststack.add(card(1,1))
        teststack.add(card(1,2))
        teststack.add(card(2,1))
        result = hands.toMakeThreeOAK(teststack)
        workstack = stacks.stack()
        workstack.populate("Full Deck")
        workstack = workstack.difference(teststack)
        self.assertEqual(result,workstack)
        
    def testABC(self):
        '''ThreeOAK_testABC: Should return cards from A,B,C ranks except A,B,C'''
        teststack = stacks.stack()
        teststack.add(card(1,1))
        teststack.add(card(2,1))
        teststack.add(card(3,1))
        result = hands.toMakeThreeOAK(teststack)
        workstack = stacks.stack()
        workstack.populate("Rank",card(1,1))
        workstack.populate("Rank",card(2,1))
        workstack.populate("Rank",card(3,1))
        workstack = workstack.difference([card(1,1),card(2,1),card(3,1)])
        self.assertEqual(result,workstack)
    
    def testAAAA(self):
        '''ThreeOAK_testAAAA: Should return nothing'''
        teststack = stacks.stack()
        teststack.add(card(1,1))
        teststack.add(card(1,2))
        teststack.add(card(1,3))
        teststack.add(card(1,4))
        result = hands.toMakeThreeOAK(teststack)
        self.assertEqual(result,stacks.stack())

    def testAAAB(self):
        '''ThreeOAK_testAAAB: Should return all cards except A/B ranks ranks (avoid full house/4OAK)'''
        teststack = stacks.stack()
        teststack.add(card(1,1))
        teststack.add(card(1,2))
        teststack.add(card(1,3))
        teststack.add(card(2,1))
        result = hands.toMakeThreeOAK(teststack)
        workstack = stacks.stack()
        workstack.populate("Full Deck")
        workstack = workstack.difference(teststack).difference([card(1,4),card(2,2),card(2,3),card(2,4)])
        self.assertEqual(result,workstack)
    
    def testAABB(self):
        '''ThreeOAK_testAABB: Should return nothing (anything from either rank makes a full house)'''
        teststack = stacks.stack()
        teststack.add(card(1,1))
        teststack.add(card(1,2))
        teststack.add(card(2,1))
        teststack.add(card(2,2))
        result = hands.toMakeThreeOAK(teststack)
        self.assertEqual(result,stacks.stack())
        
    def testAABC(self):
        '''ThreeOAK_testAABC: Should return remaining cards in rank of A'''
        teststack = stacks.stack()
        teststack.add(card(1,1))
        teststack.add(card(1,2))
        teststack.add(card(2,1))
        teststack.add(card(3,1))
        result = hands.toMakeThreeOAK(teststack)
        workstack = stacks.stack()
        workstack.add(card(1,3))
        workstack.add(card(1,4))
        self.assertEqual(result,workstack)
        
    def testABCD(self):
        '''ThreeOAK_testABCD: Should return nothing'''
        teststack = stacks.stack()
        teststack.add(card(1,1))
        teststack.add(card(2,1))
        teststack.add(card(3,1))
        teststack.add(card(4,1))
        result = hands.toMakeThreeOAK(teststack)
        self.assertEqual(result,stacks.stack())
        
    def testFive(self):
        '''ThreeOAK_testFive: Should return nothing'''
        teststack = stacks.stack()
        teststack.add(card(1,1))
        teststack.add(card(1,2))
        teststack.add(card(2,1))
        teststack.add(card(2,2))
        teststack.add(card(2,3))
        result = hands.toMakeThreeOAK(teststack)
        self.assertEqual(result,stacks.stack())
        
class Straight(unittest.TestCase):  #All done
    def setUp(self):
        self.fulldeck = stacks.stack()
        self.fulldeck.populate("Full Deck")
        self.emptystack = stacks.stack()
        self.teststack = stacks.stack()
        self.workstack = stacks.stack()
        self.goodstack = stacks.stack()

    def testBogus(self):
        '''Straight_testBogus: Should fail if not given a stack'''
        self.assertRaises(NotImplementedError, hands.toMakeStraight, 5)
        
    def testEmpty(self):
        '''Straight_testEmpty: Should return full deck if given no input'''
        result = hands.toMakeStraight(stacks.stack())
        self.assertEqual(result,self.fulldeck)
        
    def testOneCard(self):
        '''Straight_testOneCard: Should return ranks around all values minus original card'''
        valid = set(range(1,15))
        for c in range(2,14):
            self.teststack.clear()
            self.goodstack.clear()
            self.workstack.clear()
            self.teststack.add(card(c,1))
            result = hands.toMakeStraight(self.teststack)            
            for rank in valid.intersection(range(c-4,c+5)):
                self.goodstack.populate("Rank", rank)
            self.workstack.populate("Rank",c)
            self.goodstack = self.goodstack.difference(self.workstack)
            self.assertEqual(result,self.goodstack)
        
    def testOneAce(self):
        '''Straight_testOneAce: Should return 10-J-Q-K and 2-3-4-5'''
        self.teststack.add(card(1,1))
        result = hands.toMakeStraight(self.teststack)
        for rank in (range(10,14)+range(2,6)):
            self.goodstack.populate("Rank", rank)
        self.workstack.populate("Rank", 1)
        self.goodstack = self.goodstack.difference(self.workstack)
        self.assertEqual(result,self.goodstack)    
    
    #TODO: This is wrong when looking at aces
    def testTwoCards(self):
        '''Straight_testTwoCards: Should return remaining cards in ranks to complete the straight'''
        invalid = set([-3,-2,-1,0,15,16,17,18])
        for c1 in range(1,13):
            for c2 in range(c1,14):
                self.teststack.clear()
                self.goodstack.clear()
                self.workstack.clear()
                self.teststack.add(card(c1,1))
                self.teststack.add(card(c2,2))
                result = hands.toMakeStraight(self.teststack)
                top = max(c1,c2)
                bottom = min(c1,c2)
                if abs(top-bottom) > 4:
                    if bottom == 1:
                        if abs(14-top) <= 4:
                            self.workstack.populate("Rank", c1)
                            self.workstack.populate("Rank", c2)
                            for rank in range(10,14):
                                self.goodstack.populate("Rank", rank)
                            self.goodstack = self.goodstack.difference(self.workstack)
                            self.assertEqual(result,self.goodstack)
                        else:
                            self.assertEqual(result,self.emptystack)
                    else:
                        self.assertEqual(result,self.emptystack) #Should be nothing - cards are spread too far apart
                elif c2-c1 == 0:
                    self.assertEqual(result,self.emptystack) #A pair - should be nothing
                else:
                    adj = 4-abs(top-bottom)
                    for rank in set(range(bottom-adj,top+adj+1)).difference(invalid):
                        self.goodstack.populate("Rank",rank)
                    self.workstack.populate("Rank",c1)
                    self.workstack.populate("Rank",c2)
                    self.goodstack = self.goodstack.difference(self.workstack)
                    self.assertEqual(result,self.goodstack)

    #TODO: This is also wrong when looking at aces 
    def testThreeCards(self):
        '''Straight_testThreeCards: Should return remaining cards in ranks to complete the straight'''
        invalid = set([-3,-2,-1,0,15,16,17,18])
        for c1 in range(1,12):
            for c2 in range(c1+1,13):
                for c3 in range(c2+1,14):
                    self.teststack.clear()
                    self.goodstack.clear()
                    self.workstack.clear()
                    self.teststack.add(card(c1,1))
                    self.teststack.add(card(c2,2))
                    self.teststack.add(card(c3,3))
                    result = hands.toMakeStraight(self.teststack)
                    top = max(c1,c2,c3)
                    bottom = min(c1,c2,c3)
                    if abs(top-bottom) > 4:
                        if bottom == 1:
                            if abs(14-c2) <= 4:
                                self.workstack.populate("Rank", c1)
                                self.workstack.populate("Rank", c2)
                                self.workstack.populate("Rank", c3)
                                for rank in range(10,14):
                                    self.goodstack.populate("Rank", rank)
                                self.goodstack = self.goodstack.difference(self.workstack)
                                self.assertEqual(result,self.goodstack)
                            else:
                                self.assertEqual(result,self.emptystack)
                        else:
                            self.assertEqual(result,self.emptystack) #Should be nothing - cards are spread too far apart
                    elif (c3-c1 == 0) or (c3-c2 == 0) or (c2-c1 == 0):
                        self.assertEqual(result,self.emptystack) #A pair - should be nothing
                    else:
                        adj = 4-abs(top-bottom)
                        for rank in set(range(bottom-adj,top+adj+1)).difference(invalid):
                            self.goodstack.populate("Rank",rank)
                        self.workstack.populate("Rank",c1)
                        self.workstack.populate("Rank",c2)
                        self.workstack.populate("Rank",c3)
                        self.assertEqual(result,self.goodstack.difference(self.workstack))
    
    def testStraightFlushLow(self):
        self.teststack.add(card(1,1))
        self.teststack.add(card(2,1))
        self.teststack.add(card(3,1))
        self.teststack.add(card(4,1))
        result = hands.toMakeStraight(self.teststack)
        self.workstack.add(card(5,2))
        self.workstack.add(card(5,3))
        self.workstack.add(card(5,4))
        self.assertEqual(result,self.workstack)
        
    def testRoyalFlush(self):
        '''Straight_testRoyalFlush: Should return cards on suits that don't complete Royal Flush'''
        self.teststack.add(card(10,1))
        self.teststack.add(card(11,1))
        self.teststack.add(card(12,1))
        self.teststack.add(card(13,1))
        result = hands.toMakeStraight(self.teststack)
        self.goodstack.update([card(14,2),card(14,3),card(14,4)])
        self.goodstack.update([card(9,2),card(9,3),card(9,4)])
        self.assertEqual(result,self.goodstack)
        
    def testFive(self):
        '''Straight_testFive: Should return nothing'''
        self.teststack.add(card(1,1))
        self.teststack.add(card(1,2))
        self.teststack.add(card(1,3))
        self.teststack.add(card(1,4))
        self.teststack.add(card(2,1))
        result = hands.toMakeStraight(self.teststack)
        self.assertEqual(result,self.emptystack)
       
class Flush(unittest.TestCase): #All done
    def testBogus(self):
        '''Flush_testBogus: Should fail if not given a stack'''
        self.assertRaises(NotImplementedError, hands.toMakeFlush, 5)
        
    def testEmpty(self):
        '''Flush_testBogus: Should return full deck if given no input'''
        teststack = stacks.stack()
        teststack.populate("Full Deck")
        result = hands.toMakeFlush(stacks.stack())
        self.assertEqual(result,teststack)
        
    def testA(self):
        '''Flush_testA: Single card should return all cards in that suit minus card given'''
        teststack = stacks.stack()
        teststack.add(card(1,1))
        result = hands.toMakeFlush(teststack)
        goodstack = stacks.stack()
        goodstack.populate("Suit",card(1,1))
        goodstack = goodstack.difference([card(1,1)])
        self.assertEqual(result,goodstack)

    def testAA(self):
        '''Flush_testAA: Two cards one suit should return all cards in that suit minus cards given'''
        teststack = stacks.stack()
        teststack.add(card(1,1))
        teststack.add(card(2,1))
        result = hands.toMakeFlush(teststack)
        goodstack = stacks.stack()
        goodstack.populate("Suit",card(1,1))
        goodstack = goodstack.difference([card(1,1),card(2,1)])
        self.assertEqual(result,goodstack)
        
    def testAB(self):
        '''Flush_testAB: Two cards different suits should return nothing'''
        teststack = stacks.stack()
        teststack.add(card(1,1))
        teststack.add(card(2,2))
        result = hands.toMakeFlush(teststack)
        self.assertEqual(result,stacks.stack())

    def testAAAA(self):
        '''Flush_testAAAA: Four of same suit should return all cards in that suit except cards given'''
        teststack = stacks.stack()
        teststack.add(card(3,1))
        teststack.add(card(11,1))
        teststack.add(card(12,1))
        teststack.add(card(13,1))
        result = hands.toMakeFlush(teststack)
        goodstack = stacks.stack()
        goodstack.populate("Suit",card(1,1))
        goodstack = goodstack.difference([card(3,1),card(11,1),card(12,1),card(13,1)])
        self.assertEqual(result,goodstack)
        
    def testFourCardRoyalFlush(self):
        '''Flush_testFourCardRoyalFlush: Four of same suit that are in 10-J-Q-K-A should 
        return all in suit except one that completes the royal flush'''
        teststack = stacks.stack()
        teststack.add(card(1,1))
        teststack.add(card(10,1))
        teststack.add(card(11,1))
        teststack.add(card(12,1))
        result = hands.toMakeFlush(teststack)
        workstack = stacks.stack()
        workstack.populate("Suit",1)
        workstack = workstack.difference([card(1,1),card(10,1),card(11,1),card(12,1),card(13,1)])
        self.assertEqual(result,workstack)
        
    def testFourCardInsideStraightFlush(self):
        '''Flush_testFourCardInsideStraightFlush: Four of same suit that could make an inside 
        straight flush should return all in suit except inside card'''
        teststack = stacks.stack()
        teststack.add(card(3,1))
        teststack.add(card(4,1))
        teststack.add(card(6,1))
        teststack.add(card(7,1))
        result = hands.toMakeFlush(teststack)
        workstack = stacks.stack()
        workstack.populate("Suit",1)
        workstack = workstack.difference([card(3,1),card(4,1),card(5,1),card(6,1),card(7,1)])
        self.assertEqual(result,workstack)
        
    def testFourCardOutsideStraightFlush(self):
        '''Flush_testFourCardOutsideStraightFlush: Four of same suit in a straight should return 
        all in suit except outside card(s)'''
        teststack = stacks.stack()
        teststack.add(card(3,1))
        teststack.add(card(4,1))
        teststack.add(card(5,1))
        teststack.add(card(6,1))
        result = hands.toMakeFlush(teststack)
        workstack = stacks.stack()
        workstack.populate("Suit",1)
        workstack = workstack.difference([card(2,1),card(3,1),card(4,1),card(5,1),card(6,1),card(7,1)])
        self.assertEqual(result,workstack)
        
    def testFive(self):
        '''Flush_testFive: Five cards should return nothing (even if they're the same suit)'''
        teststack = stacks.stack()
        teststack.add(card(1,1))
        teststack.add(card(2,1))
        teststack.add(card(3,1))
        teststack.add(card(4,1))
        teststack.add(card(5,1))
        result = hands.toMakeFlush(teststack)
        self.assertEqual(result,stacks.stack())
        
class FullHouse(unittest.TestCase): #All done
    def testBogus(self):
        '''FullHouse_testBogus: Should fail if not given a stack'''
        self.assertRaises(NotImplementedError, hands.toMakeFullHouse, 5)
        
    def testEmpty(self):
        '''FullHouse_testEmpty: Should return full deck if given no input'''
        teststack = stacks.stack()
        teststack.populate("Full Deck")
        result = hands.toMakeFullHouse(stacks.stack())
        self.assertEqual(result,teststack)
        
    def testA(self):
        '''FullHouse_testA: Should return all cards except A'''
        teststack = stacks.stack()
        teststack.add(card(1,1))
        result = hands.toMakeFullHouse(teststack)
        workstack = stacks.stack()
        workstack.populate("Full Deck")
        workstack = workstack.difference(teststack)
        self.assertEqual(result,workstack)
        
    def testAA(self):
        '''FullHouse_testAA: Should return all cards except A's'''
        teststack = stacks.stack()
        teststack.add(card(1,1))
        teststack.add(card(1,2))
        result = hands.toMakeFullHouse(teststack)
        workstack = stacks.stack()
        workstack.populate("Full Deck")
        workstack = workstack.difference(teststack)
        self.assertEqual(result,workstack)
        
    def testAB(self):
        '''FullHouse_testAB: Should return cards in A/B rank except A/B'''
        teststack = stacks.stack()
        teststack.add(card(1,1))
        teststack.add(card(2,1))
        result = hands.toMakeFullHouse(teststack)
        workstack = stacks.stack()
        workstack.populate("Rank",card(1,1))
        workstack.populate("Rank",card(2,1))
        workstack = workstack.difference([card(1,1),card(2,1)])
        self.assertEqual(result,workstack)
        
    def testAAA(self):
        '''FullHouse_testAAA: Should return all cards except those in A rank'''
        teststack = stacks.stack()
        teststack.add(card(1,1))
        teststack.add(card(1,2))
        teststack.add(card(1,3))
        result = hands.toMakeFullHouse(teststack)
        workstack = stacks.stack()
        workstack.populate("Full Deck")
        workstack = workstack.difference(teststack).difference([card(1,4)])
        self.assertEqual(result,workstack)
        
    def testAAB(self):
        '''FullHouse_testAAB: Should return cards in A/B rank except A/B'''
        teststack = stacks.stack()
        teststack.add(card(1,1))
        teststack.add(card(1,2))
        teststack.add(card(2,1))
        result = hands.toMakeFullHouse(teststack)
        workstack = stacks.stack()
        workstack.populate("Rank",card(1,1))
        workstack.populate("Rank",card(2,1))
        workstack = workstack.difference([card(1,1),card(1,2),card(2,1)])
        self.assertEqual(result,workstack)
        
    def testABC(self):
        '''FullHouse_testABC: Should return nothing'''
        teststack = stacks.stack()
        teststack.add(card(1,1))
        teststack.add(card(2,1))
        teststack.add(card(3,1))
        result = hands.toMakeFullHouse(teststack)
        self.assertEqual(result,stacks.stack())
        
    def testAAAA(self):
        '''FullHouse_testAAAA: Should return nothing'''
        teststack = stacks.stack()
        teststack.add(card(1,1))
        teststack.add(card(1,2))
        teststack.add(card(1,3))
        teststack.add(card(1,4))
        result = hands.toMakeFullHouse(teststack)
        self.assertEqual(result,stacks.stack())
        
    def testAAAB(self):
        '''FullHouse_testAAAB: Should return B rank except B'''
        teststack = stacks.stack()
        teststack.add(card(1,1))
        teststack.add(card(1,2))
        teststack.add(card(1,3))
        teststack.add(card(2,1))
        result = hands.toMakeFullHouse(teststack)
        workstack = stacks.stack()
        workstack.populate("Rank",card(2,1))
        workstack = workstack.difference([card(2,1)])
        self.assertEqual(result,workstack)
        
    def testAABB(self):
        '''FullHouse_testAABB: Should return A/B ranks except A/B'''
        teststack = stacks.stack()
        teststack.add(card(1,1))
        teststack.add(card(1,2))
        teststack.add(card(2,1))
        teststack.add(card(2,2))
        result = hands.toMakeFullHouse(teststack)
        workstack = stacks.stack()
        workstack.populate("Rank",card(1,1))
        workstack.populate("Rank",card(2,1))
        workstack = workstack.difference([card(1,1),card(1,2),card(2,1),card(2,2)])
        self.assertEqual(result,workstack)
        
    def testAABC(self):
        '''FullHouse_testAABC: Should return nothing'''
        teststack = stacks.stack()
        teststack.add(card(1,1))
        teststack.add(card(1,2))
        teststack.add(card(2,1))
        teststack.add(card(3,1))
        result = hands.toMakeFullHouse(teststack)
        self.assertEqual(result,stacks.stack())
        
    def testABCD(self):
        '''FullHouse_testABCD: Should return nothing'''
        teststack = stacks.stack()
        teststack.add(card(1,1))
        teststack.add(card(2,1))
        teststack.add(card(3,1))
        teststack.add(card(4,1))
        result = hands.toMakeFullHouse(teststack)
        self.assertEqual(result,stacks.stack())
        
    def testFive(self):
        '''FullHouse_testFive: Should return nothing'''
        teststack = stacks.stack()
        teststack.add(card(1,1))
        teststack.add(card(1,2))
        teststack.add(card(1,3))
        teststack.add(card(1,4))
        teststack.add(card(2,1))
        result = hands.toMakeFullHouse(teststack)
        self.assertEqual(result,stacks.stack())
        
class FourOAK(unittest.TestCase): #All done

    def testBogus(self):
        '''FourOAK_testBogus: Should fail if not given a stack'''
        self.assertRaises(NotImplementedError, hands.toMakeFourOAK, 5)
        
    def testEmpty(self):
        '''FourOAK_testEmpty; Should return all cards if given no input'''
        result = hands.toMakeFourOAK(stacks.stack())
        workstack = stacks.stack()
        workstack.populate("Full Deck")
        self.assertEqual(result,workstack)
        
    def testA(self):
        '''FourOAK_testA: Should return all cards except A'''
        teststack = stacks.stack()
        teststack.add(card(1,1))
        result = hands.toMakeFourOAK(teststack)
        workstack = stacks.stack()
        workstack.populate("Full Deck")
        workstack = workstack.difference(teststack)
        self.assertEqual(result,workstack)
        
    def testAA(self):
        '''FourOAK_testAA: Should return all cards except A's'''
        teststack = stacks.stack()
        teststack.add(card(1,1))
        teststack.add(card(1,2))
        result = hands.toMakeFourOAK(teststack)
        workstack = stacks.stack()
        workstack.populate("Full Deck")
        workstack = workstack.difference(teststack)
        self.assertEqual(result,workstack)
    
    def testAB(self):
        '''FourOAK_testAB: Should return cards from both A/B ranks except A/B'''
        teststack = stacks.stack()
        teststack.add(card(1,1))
        teststack.add(card(2,1))
        result = hands.toMakeFourOAK(teststack)
        workstack = stacks.stack()
        workstack.populate("Rank",card(1,1))
        workstack.populate("Rank",card(2,1))
        workstack = workstack.difference(teststack)
        self.assertEqual(result,workstack)
        
    def testAAA(self):
        '''FourOAK_testAAA: Should return all cards except A's'''
        teststack = stacks.stack()
        teststack.add(card(1,1))
        teststack.add(card(1,2))
        teststack.add(card(1,3))
        result = hands.toMakeFourOAK(teststack)
        workstack = stacks.stack()
        workstack.populate("Full Deck")
        workstack = workstack.difference(teststack)
        self.assertEqual(result,workstack)
        
    def testAAB(self):
        '''FourOAK_testAAB: Should return only cards in the same rank as A's'''
        teststack = stacks.stack()
        teststack.add(card(1,1))
        teststack.add(card(1,2))
        teststack.add(card(2,1))
        result = hands.toMakeFourOAK(teststack)
        workstack = stacks.stack()
        workstack.add(card(1,3))
        workstack.add(card(1,4))
        self.assertEqual(result,workstack)
        
    def testABC(self):
        '''FourOAK_testABC: Should return nothing'''
        teststack = stacks.stack()
        teststack.add(card(1,1))
        teststack.add(card(2,1))
        teststack.add(card(3,1))
        result = hands.toMakeFourOAK(teststack)
        self.assertEqual(result,stacks.stack())

    def testAAAA(self):
        '''FourOAK_testAAAA: Should return all cards except A's'''
        teststack = stacks.stack()
        teststack.add(card(1,1))
        teststack.add(card(1,2))
        teststack.add(card(1,3))
        teststack.add(card(1,4))
        result = hands.toMakeFourOAK(teststack)
        workstack = stacks.stack()
        workstack.populate("Full Deck")
        workstack = workstack.difference(teststack)
        self.assertEqual(result,workstack) 
                
    def testAAAB(self):
        '''FourOAK_testAAAB: Should only return remaining card in same rank as A's'''
        teststack = stacks.stack()
        teststack.add(card(1,1))
        teststack.add(card(1,2))
        teststack.add(card(1,3))
        teststack.add(card(2,1))
        result = hands.toMakeFourOAK(teststack)
        workstack = stacks.stack()
        workstack.add(card(1,4))
        self.assertEqual(result,workstack)
     
    def testAABB(self):
        '''FourOAK_testAABB: Should return nothing'''
        teststack = stacks.stack()
        teststack.add(card(1,1))
        teststack.add(card(1,2))
        teststack.add(card(2,1))
        teststack.add(card(2,2))
        result = hands.toMakeFourOAK(teststack)
        self.assertEqual(result,stacks.stack())
    
    def testAABC(self):
        '''FourOAK_testAABC: Should return nothing'''
        teststack = stacks.stack()
        teststack.add(card(1,1))
        teststack.add(card(1,2))
        teststack.add(card(2,1))
        teststack.add(card(3,1))
        result = hands.toMakeFourOAK(teststack)
        self.assertEqual(result,stacks.stack())
        
    def testABCD(self):
        '''FourOAK_testABCD: Should return nothing'''
        teststack = stacks.stack()
        teststack.add(card(1,1))
        teststack.add(card(2,1))
        teststack.add(card(3,1))
        teststack.add(card(4,1))
        result = hands.toMakeFourOAK(teststack)
        self.assertEqual(result,stacks.stack())
        
    def testFive(self):
        '''FourOAK_testFive: Should return nothing'''
        teststack = stacks.stack()
        teststack.add(card(1,1))
        teststack.add(card(1,2))
        teststack.add(card(2,1))
        teststack.add(card(2,2))
        teststack.add(card(2,3))
        result = hands.toMakeFourOAK(teststack)
        self.assertEqual(result,stacks.stack())
        
class StraightFlush(unittest.TestCase):
    def setUp(self):
        self.fulldeck = stacks.stack()
        self.fulldeck.populate("Full Deck")
        self.emptystack = stacks.stack()
        self.teststack = stacks.stack()
        self.workstack = stacks.stack()
        self.goodstack = stacks.stack()

    def testBogus(self):
        '''StraightFlush_testBogus: Should fail if not given a stack'''
        self.assertRaises(NotImplementedError, hands.toMakeStraightFlush, 5)
        
    def testEmpty(self):
        '''StraightFlush_testEmpty: Should return full deck if given no input'''
        result = hands.toMakeStraightFlush(stacks.stack())
        self.assertEqual(result,self.fulldeck)
        
    def testOneCard(self):
        '''StraightFlush_testOneCard: Should return cards to make straight in one suit'''
        valid = set(range(1,15))
        for c in range(2,14):
            self.teststack.clear()
            self.goodstack.clear()
            self.workstack.clear()
            self.teststack.add(card(c,1))
            result = hands.toMakeStraightFlush(self.teststack)    
            for rank in valid.intersection(range(c-4,c+5)):
                self.goodstack.add(card(rank,1))
            self.workstack.add(card(c,1))
            self.goodstack = self.goodstack.difference(self.workstack)
            self.assertEqual(result,self.goodstack)
        
    def testOneAce(self):
        '''StraightFlush_testOneAce: Should return 10-J-Q-K and 2-3-4-5 in one suit'''
        self.teststack.add(card(1,1))
        result = hands.toMakeStraightFlush(self.teststack)
        for rank in (range(10,14)+range(2,6)):
            self.goodstack.add(card(rank,1))
        self.workstack.add(card(1,1))
        self.goodstack = self.goodstack.difference(self.workstack)
        self.assertEqual(result,self.goodstack)    
    
    def testTwoCards(self):
        '''StraightFlush_testTwoCards: Should return remaining cards in ranks to complete the straight flush''' 
        invalid = set([-3,-2,-1,0,15,16,17,18])
        for c1 in range(1,13):
            for c2 in range(c1+1,14):
                self.teststack.clear()
                self.goodstack.clear()
                self.workstack.clear()
                self.teststack.add(card(c1,1))
                self.teststack.add(card(c2,1))
                result = hands.toMakeStraightFlush(self.teststack)
                top = max(c1,c2)
                bottom = min(c1,c2)
                if abs(top-bottom) > 4:
                    if bottom == 1:
                        if abs(14-top) <= 4:
                            self.workstack.add(card(c1,1))
                            self.workstack.add(card(c2,1))
                            for rank in range(10,14):
                                self.goodstack.add(card(rank,1))
                            self.goodstack = self.goodstack.difference(self.workstack)
                            self.assertEqual(result,self.goodstack)
                        else:
                            self.assertEqual(result,self.emptystack)
                    else:
                        self.assertEqual(result,self.emptystack) #Should be nothing - cards are spread too far apart
                elif c2-c1 == 0:
                    self.assertEqual(result,self.emptystack) #A pair - should be nothing
                else:
                    adj = 4-abs(top-bottom)
                    for rank in set(range(bottom-adj,top+adj+1)).difference(invalid):
                        self.goodstack.add(card(rank,1))
                    self.workstack.add(card(c1,1))
                    self.workstack.add(card(c2,1))
                    self.goodstack = self.goodstack.difference(self.workstack)
                    self.assertEqual(result,self.goodstack)
 
    def testThreeCards(self):
        '''StraightFlush_testThreeCards: Should return remaining cards in ranks to complete the straight'''
        invalid = set([-3,-2,-1,0,15,16,17,18])
        for c1 in range(1,12):
            for c2 in range(c1+1,13):
                for c3 in range(c2+1,14):
                    self.teststack.clear()
                    self.goodstack.clear()
                    self.workstack.clear()
                    self.teststack.add(card(c1,1))
                    self.teststack.add(card(c2,1))
                    self.teststack.add(card(c3,1))
                    result = hands.toMakeStraightFlush(self.teststack)
                    top = max(c1,c2,c3)
                    bottom = min(c1,c2,c3)
                    if abs(top-bottom) > 4:
                        if bottom == 1:
                            if abs(14-c2) <= 4:
                                self.workstack.add(card(c1,1))
                                self.workstack.add(card(c2,1))
                                self.workstack.add(card(c3,1))
                                for rank in range(10,14):
                                    self.goodstack.add(card(rank,1))
                                self.goodstack = self.goodstack.difference(self.workstack)
                                self.assertEqual(result,self.goodstack)
                            else:
                                self.assertEqual(result,self.emptystack)
                        else:
                            self.assertEqual(result,self.emptystack) #Should be nothing - cards are spread too far apart                        
                    elif (c3-c1 == 0) or (c3-c2 == 0) or (c2-c1 == 0):
                        self.assertEqual(result,self.emptystack) #A pair - should be nothing
                    else:
                        adj = 4-abs(top-bottom)
                        for rank in set(range(bottom-adj,top+adj+1)).difference(invalid):
                            self.goodstack.add(card(rank,1))
                        self.workstack.add(card(c1,1))
                        self.workstack.add(card(c2,1))
                        self.workstack.add(card(c3,1))
                        self.assertEqual(result,self.goodstack.difference(self.workstack))
    
    def testStraightFlushLow(self):
        self.teststack.add(card(1,1))
        self.teststack.add(card(2,1))
        self.teststack.add(card(3,1))
        self.teststack.add(card(4,1))
        result = hands.toMakeStraightFlush(self.teststack)
        self.workstack.add(card(5,1))
        self.assertEqual(result,self.workstack)
        
    def testRoyalFlush(self):
        '''StraightFlush_testRoyalFlush: Should return cards on suits that don't complete Royal Flush'''
        self.teststack.add(card(10,1))
        self.teststack.add(card(11,1))
        self.teststack.add(card(12,1))
        self.teststack.add(card(13,1))
        result = hands.toMakeStraightFlush(self.teststack)
        self.goodstack.add(card(9,1))
        self.assertEqual(result,self.goodstack)
        
    def testFive(self):
        '''StraightFlush_testFive: Should return nothing'''
        self.teststack.add(card(1,1))
        self.teststack.add(card(1,2))
        self.teststack.add(card(1,3))
        self.teststack.add(card(1,4))
        self.teststack.add(card(2,1))
        result = hands.toMakeStraightFlush(self.teststack)
        self.assertEqual(result,self.emptystack)
           
class RoyalFlush(unittest.TestCase): #All done

    def testBogus(self):
        '''RoyalFlush_testBogus: Should fail if not given a stack'''
        self.assertRaises(NotImplementedError, hands.toMakeRoyalFlush, 5)
        
    def testEmpty(self):
        '''RoyalFlush_testEmpty: Should return all royal flush cards if given no input'''
        result = hands.toMakeRoyalFlush(stacks.stack())
        workstack = stacks.stack()
        workstack.populate("Royal Flush")
        self.assertEqual(result,workstack)
        
    def testNonRFCards(self):
        '''RoyalFlush_testNonRFCards: Should return nothing since a 2-9 can't make a royal flush'''
        teststack = stacks.stack()
        for rank in range(2,10):
            for suit in range(1,5):
                teststack.clear()
                teststack.add(card(rank,suit))
                result = hands.toMakeRoyalFlush(teststack)
                self.assertEqual(result,stacks.stack())     
        
    def testRFCards(self):
        '''RoyalFlush_testRFCards: Should return the royal flush cards for the suit given minus initial card'''
        teststack = stacks.stack()
        goodstack = stacks.stack()
        for rank in [1,10,11,12,13]:
            for suit in range(1,5):
                teststack.clear()
                teststack.add(card(rank,suit))
                result = hands.toMakeRoyalFlush(teststack)
                goodstack.clear()
                goodstack.populate("Face Cards",suit)
                goodstack.add(card(10,suit))
                goodstack.add(card(1,suit))
                goodstack = goodstack.difference(teststack)
                self.assertEqual(result,goodstack)
                
    def testFourCardRF(self):
        '''RoyalFlush_testFourcardRF: Should return the one remaining royal flush card'''
        teststack = stacks.stack()
        teststack.populate("Face Cards",1)
        teststack.add(card(10,1))
        result = hands.toMakeRoyalFlush(teststack)
        goodstack = stacks.stack()
        goodstack.add(card(1,1))
        self.assertEqual(result,goodstack)
                
    def testFive(self):
        '''RoyalFlush_testFive: Should return nothing'''
        teststack = stacks.stack()
        teststack.populate("Royal Flush",1)
        result = hands.toMakeRoyalFlush(teststack)
        self.assertEqual(result,stacks.stack())
    
if __name__ == "__main__":
    unittest.main()