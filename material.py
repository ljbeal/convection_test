# -*- coding: utf-8 -*-
"""
Created on Wed May  5 13:19:29 2021

@author: pc
"""

kb = 8.314     #J /K /mol
R  = 1.381E-23 #J /K
N  = 6.022E23  #/mol

class material:
    
    """
    
    class for storage of material constants
    calculate things like mass, viscosity, temp, etc. from constants
    
    """
    
    def __init__(self):
        
        # material properties
        self.mat_props = {"cp":"specific heat",
                          "visc":"viscosity",
                          "mmass":"molar mass",
                          "rho":"density",
                          }
        
        self.mat_vals = {x:0 for x in self.mat_props}
        
    def validate_update(self, inp):
        
        t = type(inp)
        
        if t in (str,int,float):
            return([inp])
        
        elif t in (list, tuple):
            return(inp)
        
        elif t in(dict,):
            return(zip(inp.keys(), inp.values()))
        
        else:
            raise Exception("unknown validation in material of type ", t)
      
    def update_material(self, attrs, vals = None):
        
        if vals != None:
            attrs = self.validate_update(attrs)
            vals = self.validate_update(vals)
            
            upd = zip(attrs, vals)
            
        else:
            upd = self.validate_update(attrs)
        
        
        for a,v in upd:
        
            self.mat_vals[a] = v
            
    # calculated properties
    def m(self,h,w,d):
        v = h * w * d
        
        dens = self.mat_vals["rho"]
        
        return(dens * v)