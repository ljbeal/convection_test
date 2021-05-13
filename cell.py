# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 11:01:44 2021

@author: Louis Beal
"""

import math
import random
import itertools

import numpy as np

from material import material

class cell:
    """
    
    2D cell for convection surface simulation
    
    """
    
    def __init__(self, 
                 x, y, idx, 
                 w, h,
                 mat,
                 t = 273):
        
        self._x = x
        self._y = y
        self._id = idx
        
        self._w = w
        self._h = h
        
        # boundary conditions
        self.bounds = {"t":None,
                       "b":None,
                       "l":None,
                       "r":None,
                       }
    
        self.mat = mat
        
        self._t = t
    
    def __repr__(self):
        x, y = self.loc
        idx = self._id
        
        # ret = "cell {} ({}, {})".format(idx, x, y)
        ret = "cell {}".format(idx)
        
        return(ret)
        
    #spatial properties
    @property
    def x(self):
        return(self._x)
    
    @property
    def y(self):
        return(self._y)
    
    @property
    def w(self):
        return(self._w)
    
    @property
    def h(self):
        return(self._h)
    
    @property
    def idx(self):
        return(self._id)
    
    @property
    def loc(self):
        return((self._x,self._y))
    
    #material based properties
    @property
    def t(self):
        return(self._t)
    
    @t.setter
    def t(self, t):
        # print("overriding temperature for cell {} to {}k".format(self.idx, t))
        self._t = t
    
    #boundary connections
    @property
    def nbounds(self):
        n = len([x for x in self.bounds.values() if x != None])
        return(n)
        
    def update_bounds(self, side, bound):
        
        self.bounds[side] = bound
        
    def propagate(self):
        
        t = 0
        for bound in self.bounds.values():
            t += bound.t/4
            
        self.t = round(t,2)
    
    
