'''Unittest test suite for is* functions in hands.py''' 
import hands
import unittest
import stacks
from card import card

class All(unittest.TestCase):
    
    def setUp(self):
        self.teststack = stacks.stack()
      
    def testIsRoyalFlush(self):
        '''RoyalFlush_testIsRoyalFlush'''
        self.teststack.populate("Royal Flush",1)
        result = hands.isRoyalFlush(self.teststack)
        self.assertTrue(result)
    
    def testIsStraightFlush(self):
        '''All_testIsStraightFlush'''
        for rank in range (2,7):
            self.teststack.add(card(rank,1))
        result = hands.isStraightFlush(self.teststack)
        self.assertTrue(result)
        
    def testIsFourOAK(self):
        '''All_testIsFourOAK'''
        self.teststack.populate("Rank", 5)
        self.teststack.add(card(1,1))
        result = hands.isFourOAK(self.teststack)
        self.assertTrue(result)
        
    def testIsFullHouse(self):
        '''All_testIsFullHouse'''
        self.teststack.update([card(1,1),card(1,2),card(2,1),card(2,2),card(2,3)])
        result = hands.isFullHouse(self.teststack)
        self.assertTrue(result)
        
    def testIsFlush(self):
        '''All_testIsFlush'''
        self.teststack.update([card(1,1),card(2,1),card(5,1),card(6,1),card(9,1)])
        result = hands.isFlush(self.teststack)
        self.assertTrue(result)
        
    def testIsStraight(self):
        '''All_testIsStraight'''
        self.teststack.update([card(1,1),card(2,1),card(3,4),card(4,3),card(5,2)])
        result = hands.isStraight(self.teststack)
        self.assertTrue(result)
        
    def testIsThreeOAK(self):
        '''All_testIsThreeOAK'''
        self.teststack.update([card(3,1),card(3,2),card(3,3),card(4,1),card(8,1)])
        result = hands.isThreeOAK(self.teststack)
        self.assertTrue(result)
        
    def testIsTwoPair(self):
        '''All_testIsTwoPair'''
        self.teststack.update([card(3,1),card(3,3),card(6,1),card(6,4),card(8,1)])
        result = hands.isTwoPair(self.teststack)
        self.assertTrue(result)
        
    def testIsPair(self):
        '''All_testIsPair'''
        self.teststack.update([card(6,1),card(6,2),card(3,1),card(2,4),card(1,1)])
        result = hands.isPair(self.teststack)
        self.assertTrue(result)
    
if __name__ == "__main__":
    unittest.main()