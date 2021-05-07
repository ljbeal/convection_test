# -*- coding: utf-8 -*-
"""
Created on Thu May  6 11:47:17 2021

@author: pc
"""

import itertools

import numpy as np

#module imports
from cell import cell

class simspace:
    
    def __init__(self, grid):
        
        self._n, self._m = grid.shape
        self.heatgrid = np.array(grid).flatten()
        
        self.cells = []
        
    def assign(self, cell):
        
        """
        
        map cell object to the stored grid
        handle locations and adjacency assigment
        
        """
        
        n = self._n
        m = self._m
        
        xy = list(itertools.product(range(n), range(m)))
        
        for i in range(len(xy)):
            x = xy[i][0]
            y = xy[i][1]
            t = self.heatgrid[i]
            
            self.cells.append(cell(x, y, t))
        


if __name__ == "__main__":
    
    grid = np.zeros((5,5))
    
    test = simspace(grid)
    
    test.assign(cell)