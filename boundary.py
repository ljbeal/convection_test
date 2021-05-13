# -*- coding: utf-8 -*-
"""
Created on Sun May  9 12:14:40 2021

@author: pc
"""

from material import material

class boundary:
    
    def __init__(self, mat, c1, c2 = "solid"):
        
        """
        
        pass cell objects to c1,2
        otherwise pass boundary condition to c2
        
        """
        
        self.modules = ["base"]
        
        self.c1 = c1
        self.c2 = c2
        
        self.connected = [c1, c2]
        
        if type(c2) == str:
            self._type = c2
        else:
            self._type = "join"
            
        self.mat = mat
        
        self.t = 273
            
    def __repr__(self):
        ret = "bound: " + str(self.c1)
        
        if self.edge:
            ret += ", " + self.type
            
        else:
            ret += ", " + str(self.c2)
            
        return(ret)    
        
    @property
    def edge(self):
        #return True if this boundary is at the edge of the simspace
        return(self._type != "join")
    
    @property
    def type(self):
        return(self._type)    
    
    def extract(self):
        #set boundary to average of connected cells
        if not self.edge:
            self.t = (self.c1.t + self.c2.t)/2
    
if __name__ == "__main__":
    
    from cell import cell
    
    c1 = cell(0,0,0)
    c2 = cell(0,1,1)
    
    testjoin = boundary(c1, c2)
    testedge = boundary(c1, "solid")
    
    print(testjoin.type, testjoin.edge)
    print(testedge.type, testedge.edge)
    
    print(testjoin)
    print(testedge)