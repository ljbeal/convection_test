# -*- coding: utf-8 -*-
"""
Created on Sun May  9 12:14:40 2021

@author: pc
"""

from material import material

class boundary:
    
    def __init__(self, mat, c1, c2 = None, boundary_cond = "solid"):
        
        """
        
        pass cell objects to c1,2
        otherwise pass boundary condition to c2
        
        """
        
        self.modules = ["base"]
        
        self.c1 = c1
        self.c2 = c2
        
        self.connected = [c1, c2]
        
        if (type(c2) == str) or (c2 == None):
            self._type = self.c2 = boundary_cond
        else:
            self._type = "join"
            
        self.mat = mat
        
        
        self.maxflux = 1E6
        self._e = 0 #energy stored in this boundary
            
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
       
    def get_orient(self, cell):
        
        for key, val in cell.bounds.items():
            if val == self:
                return(key)
    
    def dt(self, step):
        #share energy across boundary
        store = self._e
        
        c1orient = self.get_orient(self.c1)
        if not self.edge:            
            
            c2orient = self.get_orient(self.c2)
            
            self.c1.move_energy(store/2, c1orient)
            self.c2.move_energy(store/2, c2orient)
            
        else:
            if self.type == "free":
                ratio = 2
            elif self.type == "solid":
                ratio = 1
            
            self.c1.move_energy(store/ratio, c1orient)
            
        self._e = 0 #reset energy
        
                
    
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