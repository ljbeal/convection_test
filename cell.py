# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 11:01:44 2021

@author: Louis Beal
"""

import math
import itertools

import numpy as np

class cell:
    """
    
    2D cell for convection surface simulation
    
    """
    
    def __init__(self, x, y, idx, t = 0):
        
        self._x = x
        self._y = y
        self._id = idx
        
        self._t = t
        
        self.adjacent = {}
    
    def __repr__(self):
        x, y = self.loc
        idx = self._id
        
        ret = "cell object, located at grid ({}, {}), id {}".format(x, y, idx)
        
        ret += "\n\t{} connected cells:".format(len(self.adjacent))
        
        for item in self.adjacent.values():
            ret += "\n\t{} {}".format(*item.loc)
        
        return(ret)
        
    @property
    def x(self):
        return(self._x)
    
    @property
    def y(self):
        return(self._y)
    
    @property
    def idx(self):
        return(self._id)
    
    @property
    def loc(self):
        return((self._x,self._y))
        
    def connect(self, grid):
        #find neighbours from the grid and connect with them
        
        x, y = self.loc
        n, m = grid.shape
        
        #initialise locals as None
        top = bot = rgt = lft = None
        
        if y > 0:
            top = (x, y-1)
        
        if y < m-1:
            bot = (x, y+1)
            
        if x < n-1:
            rgt = (x+1, y)
            
        if x > 0:
            lft = (x-1, y)
        
        adj = (top,bot,rgt,lft)
        
        pos = [grid.index(*x) for x in adj if x != None]
        
        # print(x,y,adj,pos)
        
        for p in pos:
            other = grid.storage[p]
            
            idx = other.idx
            
            if idx not in self.adjacent:
                self.adjacent[idx] = other
                
                

class simgrid:

    """
    iterable grid object
    allows for cell storage and easy iteration without faffing with x,y or i
    """
    
    def __init__(self, n, m):
        
        self._n = n
        self._m = m
        
        self._coords = itertools.product(range(n), range(m))
        self.storage = []
            
    def __iter__(self):
        for item in self.storage:
            yield(item)
            
    def __len__(self):
        return(len(self.storage))
    
    def __repr__(self):
        #formatted string representation of the grid layout
        
        ret = "grid coords:"
        
        for x in range(n):
            temp = []
            for y in range(m):
                temp.append("{}, {}".format(x,y))
                
            ret += "\n" + " | ".join(temp)
            
        ret += "\n"
        
        return(ret)
    
    @property
    def n(self):
        return(self._n)
    
    @property
    def m(self):
        return(self._m)
    
    @property
    def shape(self):
        #n, m shape of grid
        return(self._n, self._m)
        
    @property
    def coorditer(self):
        #iterable of coordinate pairs
        return(self._coords)
    
    #supplimentary property functions
    def index(self, x, y):
        #return flat index of x,y point on grid
        return(x*(self._m) + y)
    
    #housekeeping functions
    def mapobj(self, obj):
        # print(self.shape)
        for coord in self.coorditer:
            x, y = coord
            
            idx = self.index(x, y)
            
            # print(x,y,idx)
            
            self.storage.append(obj(x, y, idx))
        
        # print()
        for item in self.storage:
            item.connect(self)
            
            
    
if __name__ == "__main__":
    
    heat = np.zeros((3,2))
    
    n, m = heat.shape
    
    grid = simgrid(n,m)
    print(grid)
    grid.mapobj(cell)
    
    print()
    for c in grid:
        print(c)
        print()