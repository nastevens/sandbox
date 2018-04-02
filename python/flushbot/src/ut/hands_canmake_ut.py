'''Unittest test suite for is* functions in hands.py''' 
import hands
import unittest
import stacks
from card import card

class All(unittest.TestCase):
    
    def setUp(self):
        self.teststack = stacks.stack()
            
    def test1(self):
        self.teststack.populate("Full Deck")
        result = hands.canMakeRoyalFlush(self.teststack)
        self.assertTrue(result)
        self.teststack.remove(card(13,1))
        self.teststack.remove(card(13,2))
        self.teststack.remove(card(13,3))
        self.teststack.remove(card(13,4))
        result = hands.canMakeRoyalFlush(self.teststack)
        self.assertFalse(result)
    
if __name__ == "__main__":
    unittest.main()