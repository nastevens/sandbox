import cPickle, stacks
from card import card
from itertools import groupby

class lookup():
    
    def __init__(self, pkl):
        FILE = open(pkl,"rb")
        self.table = cPickle.load(FILE)
        
    def removecard(self, crd):
        if not isinstance(crd,card):
            raise ValueError, "Must pass card"
        self.__remove(self.table,crd.value())
        
    def __remove(self, dic, value):
        if isinstance(dic,dict):
            for k, v in dic.items():
                if k == value:
                    del dic[k]
                else:
                    self.__remove(dic[k],value)
    
    def canmake(self,cards,mask):
        li = [x.value() for x in cards]
        li.sort()
        return self.__readnodes(self.table,1,li,mask)
        
    def __getvalat(self,dic,indices):
#        if not isinstance(indices,list):
#            raise ValueError, "Must pass sorted list"
        if len(indices) == 1:
            index = indices.pop(0)
            return dic[index]
        elif len(indices) < 1:
            return dic
        else:
            index = indices.pop(0)
            return self.__getvalat(dic[index],indices)
        
    def __getallnodes(self,dic,mask=set([])):
        if isinstance(dic,dict):
            li = []
            for k in set(dic.keys()).difference(mask):
            #for v in [y for x,y in dic.items() if x not in mask]:
                li.extend(self.__getallnodes(dic[k],mask))
            return li
        else:
            return [dic] 

    def __groupdict(self,li):
        g = {}
        for val in li:
            g[val] = g.get(val,0) + 1
        return g
    
    def __readnodes(self,dic,level,have,mask=set([])):
        if isinstance(dic,dict):
            
            if len(have) == 0:
                return self.__getallnodes(dic,mask)
            
            if len(have) > 6-level:
                return []
            
            if len(have) == 6-level:
                return self.__getvalat(dic,have[:])
                        
            #reads all trees below our list of indices
            li = []
            for i in [x for x in dic.keys() if x<have[0] and x not in mask]:
                li.extend(self.__readnodes(dic[i],level+1,have,mask))
            
            #reads tree at first level of 'have'
            for i in [x for x in dic.keys() if x==have[0]]:
                li.extend(self.__readnodes(dic[have[0]],level+1,have[1:],mask))
            
            return li
            
if __name__ == '__main__':
    lu = lookup("C:\\data1.pkl")
    v = lu.canmake(stacks.stack([card(48)]),stacks.stack())
    v.sort()
    val = [(k, len(list(g))) for k, g in groupby(v)]
    print val