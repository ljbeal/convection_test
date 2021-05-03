# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 11:01:44 2021

@author: Louis Beal
"""

import math
import unittest

import numpy as np
import matplotlib.pyplot as plt

from scipy import ndimage

class cell:
    """
    
    2D cell for convection surface simulation
    represent cell space as vector
    
    """
    
    def __init__(self, x, y, u = 0, v = 0,test = False):
        
        self._x = x
        self._y = y
        
        self._u = u
        self._v = v
        self._w = 0
        
        self.test = test
        
        self.rounding = 2
        
    ### property functions
    #x location
    @property
    def x(self):
        return(self._x)
    
    @x.setter
    def x(self,x):
        self._x = x
    
    #y location
    @property
    def y(self):
        return(self._y)
    
    @y.setter
    def y(self,y):
        self._y = y
       
    ### vector attributes    
    #x cartesian component
    @property
    def u(self):
        return(self._u)
    
    @u.setter
    def u(self,u):
        self._u = u
    
    #y cartesian component
    @property
    def v(self):
        return(self._v)
    
    @v.setter
    def v(self,v):
        self._v = v
        
    #z cartesian component
    @property
    def w(self):
        return(self._w)
    
    @w.setter
    def w(self,w):
        self._w = w
        
    @property
    def data(self):
        
        return(self.x,self.y,self.u,self.v,self.w)
        
    def update(self,u,v,w):
        
        self.w = w
        self.u = u/abs(w)
        self.v = v/abs(w)
    
    def polar(self):
        
        # print("polar coords from {}x, {}y".format(self.u,self.v))
        
        #pythagorean magnitude
        m = math.hypot(self.u, self.v)
        
        #angle from x axis
        #not on any axis
        r = math.atan2(self.v, self.u)
        
        #convert to degrees
        r *= 180/math.pi
        
        # print("\ninternal {}".format(r))
                
        polar = (round(m,self.rounding),round(r,self.rounding))
        
        # print('\t',polar)
        
        return(polar)
        
    @property
    def effect(self):
        """
        
        vector effect array
        converts this vector into a convection cell simulant
        
        vector will :
        - attempt to pull opposing vectors antiparallel
            => subduction
        - attempt to align adjacent vectors parallel
            => assimilation
        
        """
        
        m, r = self.polar()
        
        #vector-aligned effect matrix for r = 0
        basew = [[0,0,0],
                 [0.5,0,-0.5],
                 [0,0,0]]
        
        basef = [[0.0,0.1,0.0],
                 [0.1,-0.1,0.1],
                 [0.0,0.1,0.0]]
        
        rotated = rotate(basef,r)
        
        u_rot = self.u * np.array(rotated)
        v_rot = self.v * np.array(rotated)
        w_rot = rotate(basew,r)
        
        return((u_rot,v_rot,w_rot))
 
def rotate(base,r):

    if r != 0:
        r_rot = math.floor(r/45)
        r_rem = r % 45
    else:
        r_rot = 0
        r_rem = 0
            
    #get outer ring as list
    lin = base[0]\
        + [base[1][2]]\
        + list(reversed(base[2]))\
        + [base[1][0]]
        
    rot_int = lin[r_rot:] + lin[:r_rot]
    
    #fraction to bleed over to interpolate
    bleed = r_rem/45
    
    rot_int_2 = rot_int[1:] + rot_int[:1]
    
    merged = list(bleed*np.array(rot_int_2) + (1-bleed)*np.array(rot_int))        
    
    rotated = [merged[:3],
               [merged[7],base[1][1],merged[3]],
               merged[6:3:-1]]
    
    return(rotated)       
        

### testing class ###      
        
class test_cell(unittest.TestCase):
    
    def setUp(self):
        
        self.focus = cell(0,0,test = True)
    
    def test_polar(self):
        
        self.focus.u = 10        
        self.focus.v = 5
        
        self.assertEqual(self.focus.polar(), (11.18, 26.57))
        
        self.focus.u = 0        
        self.focus.v = 10
        
        self.assertEqual(self.focus.polar(), (10.0, 90.0))
        
        self.focus.u = 10        
        self.focus.v = 0
        
        self.assertEqual(self.focus.polar(), (10.0, 0.0))
        
        self.focus.u = -10        
        self.focus.v = 5
        
        self.assertEqual(self.focus.polar(), (11.18, 153.43))
        
        self.focus.u = -10        
        self.focus.v = -7
        
        self.assertEqual(self.focus.polar(), (12.21, -145.01))
        
        self.focus.u = 9
        self.focus.v = -7
        
        self.assertEqual(self.focus.polar(), (11.40, -37.87))
        
    def test_rotation(self):
        
        self.focus.u = 10
        self.focus.v = 0
        
        test = self.focus.effect
        
        print(test)
        
        self.focus.u = 0
        self.focus.v = 10
        
        test = self.focus.effect
        
        print(test)
        
        self.focus.u = 5
        self.focus.v = 6
        
        test = self.focus.effect
        
        print(test)
        
        self.focus.u = 9
        self.focus.v = -7
        
        test = self.focus.effect
        
        print(test)
        
        self.focus.u = 1
        self.focus.v = 10
        
        test = self.focus.effect
        
        print(test)
        
        self.focus.u = -2
        self.focus.v = 10
        
        test = self.focus.effect
        
        print(test)
        
        
if __name__ == "__main__":
    unittest.main()
    
    u = 10
    v = 0
    test = cell(0,0,u,v)
    
    ue,ve = test.effect
    
        
    fig, ax = plt.subplots()
    ax.quiver(ue,ve)
    plt.gca().invert_yaxis()
    plt.axis('off')
    
    plt.show()