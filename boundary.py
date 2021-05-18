# -*- coding: utf-8 -*-
"""
Created on Sun May  9 12:14:40 2021

@author: pc
"""

class edge:
    
    def __init__(self, loss):
        """
        dummy cell for edge boundary condition handling
        """
        
        self.loss = loss #heat loss in watts across whole simulation
        
        self.bounds = {}
        
        self.outside = True
        self.connected = 0
        
        self.p = 0
        self.idx = -1
        
    def __repr__(self):
        return("edge region")
        
    def incr_connector(self):
        
        self.connected += 1
        return(self.connected)
    
    def move_energy(self, de, orient = None, dt = 0):
        
        loss = self.loss/self.connected #max loss in W
        P = loss * dt
        
        return(P)
    
    def move_material(self, *args):
        pass

class boundary:
    
    def __init__(self, mat, c1, c2, flow = True):
        
        """
        
        pass cell objects to c1,2
        otherwise pass boundary condition to c2
        
        """
        
        self.modules = ["base"]
        
        self.c1 = c1            
        self.c2 = c2
        
        self.connected = [c1, c2]
        self.pressure = [0, 0]
            
        self.mat = mat
        
        self.flow = flow
        
        self._e = 0 #energy stored in this boundary
            
    def __repr__(self):
        ret = "bound: " + str(self.c1)
        
        ret += ", " + str(self.c2)
            
        return(ret)
    
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
        
        c1e1 = self.c1._e
        
        c1orient = self.get_orient(self.c1)            
        c2orient = self.get_orient(self.c2)
        
        if (self.flow) and (not self.c2.outside):
            #ratio of pressures in cells
            forward_pressure_ratio = self.pressure[0]/self.pressure[1]
            
            
            mvect = 1 - forward_pressure_ratio
            
            self.c1.move_material(mvect, c1orient)
            self.c2.move_material(-mvect, c2orient) #assumptions, assumptions
        
        if c2orient == None:
            share = self.c2.move_energy(store, c2orient, step)    
        else:
            share = self.c2.move_energy(store/2, c2orient, step)   
            
        self.c1.move_energy(store - share, c1orient)
        
        # if c2orient == None:
        #     print("\ttimestep {}s, stored {}J. lost {} to c2".format(step, store, share))
        #     print("\tc1 e {} -> {}J".format(c1e1, self.c1._e))
        
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