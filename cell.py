# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 11:01:44 2021

@author: Louis Beal
"""

import math
import random
import itertools

import numpy as np

from boundary import boundary

class cell:
    """
    
    2D cell for convection surface simulation
    
    """
    
    def __init__(self, 
                 x, y, idx, 
                 w, h,
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
        
        # material properties
        self.mat_props = {"cp":"specific heat",
                          "visc":"viscosity",
                          "mmass":"molar mass",
                          "rho":"density",
                          }
        
        self.mat_vals = {x:0 for x in self.mat_props}
        
        # info storage
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
    
    #boundary connections
    @property
    def nbounds(self):
        n = len([x for x in self.bounds.values() if x != None])
        return(n)
        
    def update_bounds(self, side, bound):
        
        self.bounds[side] = bound
        
    # material storage
    def update_material(self, attr, value):
        self.mat_vals[attr] = value
    
    @property
    def t(self):
        # average cell temperature
        return(self._t)
    
    @property
    def m(self):
        #approximate mass
        a = self.h * self.w
        
        #take mean of width and height as depth for now
        d = math.mean(self.cell_shape)
        
        v = a * d
        
        dens = self.mat_vals["rho"]
        
        return(v * dens)
    
    
