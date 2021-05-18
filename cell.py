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
    stores energy and momentum terms
    instantaneous properties calculated from the material class
    
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
        
        self.outside = False
    
        self.mat = mat   
        
        #initial temperature
        self.t = t
        
        #vector attributes
        self.evect = {"u":0,"v":0}
        self.mvect = {"u":0,"v":0}
        
        #config
        self.rad_loss = True
        
    
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
    def a(self):
        return(self.h * self.w)
        
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
        
    @property
    def p(self):
        
        p = self.mat.p(self.v, self.t)
        
        return(p)
        
    @property
    def state(self):
        #return everything in a dict
        props = {"t":self.t,
                 "e":self._e,
                 "p":self.p,
                 }
        
        return(props)
    
    #energetics
    def move_energy(self, de = None, orient = None, dt = 0):
        # e0 = self._e
        if de == None:
            de = self._e
            self._e = 0
            
        else:
            self._e += de
        
        # print("cell {} e {} -> {}J".format(self.idx, e0, self._e))
        
            
        self.update_vector(self.evect, orient, de)
            
        return(abs(de))
    
    def move_material(self, dm, orient, dt = 0):
        
        self.update_vector(self.mvect, orient, dm)
        
    def update_vector(self, vect, orient, val):
        
        if orient != None:
            
            if orient == "r":
                vect["u"] -= val
            elif orient == "l":
                vect["u"] += val
            elif orient == "t":
                vect["v"] += val
            elif orient == "b":
                vect["v"] -= val
            else:
                raise Exception("unkown orient {}".format(orient))
        
    @property
    def bbody_power(self):
        #call the emissivity function with stored values
        
        P = self.mat.emittance(self.a, self.t)
        
        return(P)
        
    def dt(self, dt):
        
        p_init = self.p
        
        if self.rad_loss:
            P = self.bbody_power
            de = P * dt #amount lost to emission
            
            e_rad = self.move_energy(-de)
        
        e_share = self.move_energy() #all remaining energy is shared
        
        for b in self.bounds.values():
            
            b._e += e_share/4
            
            b.pressure[b.connected.index(self)] = p_init
            
        return(e_rad)
            
    def get_vect(self):
        eu,ev = self.evect.values()
        mu,mv = self.mvect.values()
        self.evect = {"u":0,"v":0}
        self.mvect = {"u":0,"v":0}
        
        vect = {"e":(eu,ev),
                "m":(mu,mv)}
        
        return(vect)
    
    #boundary connections
    @property
    def nbounds(self):
        n = len([x for x in self.bounds.values() if x != None])
        return(n)
        
    def update_bounds(self, side, bound):
        
        # if self.idx == 4:
        #     print(side, bound)
        
        self.bounds[side] = bound