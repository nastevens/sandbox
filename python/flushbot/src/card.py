class card():
    __SUITS = { 1 : "Clubs", 2 : "Diamonds", 3 : "Hearts", 4 : "Spades",
                "Clubs" : 1, "Diamonds" : 2, "Hearts" : 3, "Spades" : 4}
    __RANKS = { 1 : "Ace", 2 : "Two", 3 : "Three", 4 : "Four", 5 : "Five", 
                6 : "Six", 7 : "Seven", 8 : "Eight", 9 : "Nine", 10 : "Ten",
                11 : "Jack", 12 : "Queen", 13 : "King",
                "Ace" : 1, "Two" : 2, "Three" : 3, "Four" : 4, "Five" : 5, 
                "Six" : 6, "Seven" : 7, "Eight" : 8, "Nine" : 9, "Ten" : 10,
                "Jack" : 11, "Queen" : 12, "King" : 13 }
    
    def __init__(self, val1, val2=None):
        if val2==None:
            self.data = (self.__value(val1)[0], self.__value(val1)[1], val1)
        else:
            self.data = (self.__cleanrank(val1), self.__cleansuit(val2), self.__value(val1,val2))
        
    def __cmp__(self, other):
        if isinstance(other, card):
            if self.data[2] == other.data[2]:
                return 0
            elif self.data[2] < other.data[2]:
                return -1
            else:
                return 1
        else: 
            return NotImplemented
        
    def __hash__(self):
        return hash(self.data)
        
    def __repr__(self):
        return str((self.__RANKS[self.data[0]], self.__SUITS[self.data[1]]))
    
    def __str__(self):
        return self.__RANKS[self.data[0]] + " of " + self.__SUITS[self.data[1]]
        
    def rank(self):
        return self.data[0]
        
    def suit(self):
        return self.data[1]
    
    def value(self):
        return self.data[2]
    
    def __cleansuit(self, value):
        if isinstance(value, str):
            return self.__SUITS[value]
        elif isinstance(value,int):
            return value
        else:
            raise NotImplementedError, "__cleansuit must receive a string or an int"
    
    def __cleanrank(self, value):
        if isinstance(value, str):
            return self.__RANKS[value]
        elif isinstance(value,int):
            if value == 14:
                return 1
            else:
                return value
        raise NotImplementedError, "__cleanrank must receive a string or an int"
    
    def __value(self,val1,val2=None):
        if val2 == None:
            if val1 < 1 or val1 > 52:
                raise ValueError, "value must be between 1 and 52"
            if(val1 % 4) == 0:
                return (val1 / 4, 4)
            else:
                return (val1 / 4 + 1, val1 % 4) 
        else:
            return (self.__cleanrank(val1) - 1) * 4 + self.__cleansuit(val2)