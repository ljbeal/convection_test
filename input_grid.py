# -*- coding: utf-8 -*-
"""
Created on Sun May 16 09:35:09 2021

@author: pc
"""

import numpy as np

class input_grid:
    
    def __init__(self, n, m):
        
        self.base = np.zeros((n,m))
        
        self.shape = n, m
        self.mid = [int(x/2) for x in (n,m)]
        
    @property
    def grid(self):
        return(self.base)
        
    def add_hline(self, y):
        
        self.base[y,:] = 1
        
    def add_vline(self,x):
        
        self.base[:,x] = 1
        
    def add_cross(self, cent_x = None, cent_y = None):
        
        if cent_x == None:
            cent_x = self.mid[0]
        if cent_y == None:
            cent_y = self.mid[1]
            
        self.add_hline(cent_y)
        self.add_vline(cent_x)
        
    def add_circle(self, r, cent_x = None, cent_y = None):
        
        n, m = self.shape
        
        if cent_x == None:
            cent_x = self.mid[0]
        if cent_y == None:
            cent_y = self.mid[1]
        
        for x in range(n):
            for y in range(m):
                
                dx = abs(cent_x - x)
                dy = abs(cent_y - y)
                
                if (dx**2 + dy**2)**0.5 <= r:
                    
                    self.base[x,y] = 1
        
if __name__ == "__main__":
    
    test = input_grid(11,11)
    test.add_hline(5)
    
    test.add_circle(2.5,5,5)
    
    grid = test