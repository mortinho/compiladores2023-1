import token

class Tree:
    def __init__(self,name):
        self.name = name
        self.children = []
    
    def addChild(self,child):
        if child!=False: 
            self.children.append(child)
            return True
        else: return False
    
    def tab(self,n):
        for i in range(n):
            print("  ",end = '')
            
    def print(self,depth = 0):
        self.tab(depth)
        print(self.name)
        depth +=1
        for c in self.children:
            if type(c) == token.Token:
                self.tab(depth)
                print(c)
            elif type(c) == Tree: c.print(depth)
            else: print(c)