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
        
        self.material_properties = []
        
        self.t = t
    
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
    def d(self):
        #approximate depth from mean of other attributes
        return(sum((self.w, self.h))/2)
    
    @property
    def v(self):
        #volume analogue
        return(self.h * self.w * self.d)
    
    @property
    def idx(self):
        return(self._id)
    
    @property
    def loc(self):
        return((self._x,self._y))
    
    
    #material based properties        
    @property
    def e(self):
        return(self._e)
    
    @property
    def m(self):
        # mass
        
        return(self.mat.m(self.v))
    
    @property
    def t(self):
        #get temperature value from heat energy stored
        #!!!TODO split energy types
        
        
        t = self.mat.t(self.m, self.e)
        
        return(t)
    
    @t.setter
    def t(self, t):
        # print("overriding temperature for cell {} to {}k".format(self.idx, t))
        # to set temperature, need to override energy storage
        
        # require mass
        m = self.m
        self._e = m * t * self.mat.vals["cp"]
        
    
    #energetics
    def energy(self, de):
        e0 = self._e
        self._e += de
        
        # print("cell {} e {} -> {}J".format(self.idx, e0, self._e))
    
    def subtract_e(self):
        
        de = self._e/4
        
        self.energy(-de)
        
        return(de)
    
    def add_e(self, e):
        
        self.energy(e)
    
    #boundary connections
    @property
    def nbounds(self):
        n = len([x for x in self.bounds.values() if x != None])
        return(n)
        
    def update_bounds(self, side, bound):
        
        self.bounds[side] = bound