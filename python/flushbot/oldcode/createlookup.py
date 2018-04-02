import hands, stacks, sys, pickle
from card import card

def createdata(dataset):
    depth = 53
    dataset["all"] = set([])
    for i in range(1,depth):
        dataset[i] = set([])
    for i in range(1,depth):
        sys.stdout.writelines(["\n",str(i)])
        for j in range(i+1,depth):
            sys.stdout.write(".")
            for k in range(j+1,depth):
                for l in range(k+1,depth):
                    for m in range(l+1,depth):
                        res = "N"
                        st = stacks.stack([card(i),card(j),card(k),card(l),card(m)])
                        if hands.isRoyalFlush(st): res = "R"
                        elif hands.isStraightFlush(st): res = "T"
                        elif hands.isFourOAK(st): res = "4"
                        elif hands.isFullHouse(st): res = "H"
                        elif hands.isFlush(st): res = "F"            
                        elif hands.isStraight(st): res = "S"
                        elif hands.isThreeOAK(st): res = "3"
                        elif hands.isTwoPair(st): res = "X"
                        elif hands.isPair(st): res = "P"
                        t = (i,j,k,l,m,res)
                        dataset[i].add(t)
                        dataset[j].add(t)
                        dataset[k].add(t)
                        dataset[l].add(t)
                        dataset[m].add(t)
                        dataset["all"].add(t)
                        
if __name__ == '__main__':
    dataset = {}
    print "Creating data"
    createdata(dataset)
    print "Writing pickle"
    output = open('data2.pkl', 'wb')
    pickle.dump(dataset,output)
    output.close()