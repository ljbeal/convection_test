# -*- coding: utf-8 -*-
"""
Created on Wed May  5 13:19:29 2021

@author: pc
"""

kb = 8.314     #J /K /mol
R  = 1.381E-23 #J /K
N  = 6.022E23  #/mol

class material:
    
    def __init__(self, t_melt):
        
        #cheat and model as ideal gas
        #PV = nRT
        
        self._t_melt
        
    @property
    def is_liquid(self, t):
        return(t > self._t_melt)