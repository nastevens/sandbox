import hands, textwrap, stacks, sys, pickle
from card import card

def createdata(dic,depth,start,history):
    if depth == 2:
        print start
    if depth == 4:
        sys.stdout.write(".")
    if depth == 5:
        for i in range(start,53):
            li = map(lambda x: card(x),history+(i,))
            st = stacks.stack(li)
            res = "N"
            if hands.isRoyalFlush(st): res = "R"
            elif hands.isStraightFlush(st): res = "T"
            elif hands.isFourOAK(st): res = "4"
            elif hands.isFullHouse(st): res = "H"
            elif hands.isFlush(st): res = "F"            
            elif hands.isStraight(st): res = "S"
            elif hands.isThreeOAK(st): res = "3"
            elif hands.isTwoPair(st): res = "X"
            elif hands.isPair(st): res = "P"
            dic[i] = res
    else:
        for i in range(start,53):
            dic[i] = {}
            createdata(dic[i],depth+1,i+1,history+(i,))
            
def deleteempty(dic):
    if isinstance(dic,dict):
        for k,v in dic.items(): 
            if deleteempty(v): del dic[k]
        if len(dic) == 0:
            return True
        else:
            return False
    else:
        return

if __name__ == '__main__':
    test = {}
    print "Creating data"
    createdata(test,1,1,())
    print "Deleting blanks"
    deleteempty(test)
    print "Writing pickle"
    output = open('data1.pkl', 'wb')
    pickle.dump(test,output)
    output.close()