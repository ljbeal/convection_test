# -*- coding: utf-8 -*-
"""
Created on Sun May  9 13:15:12 2021

@author: pc
"""

import unittest
import itertools

import numpy as np

from cell import cell
from simspace import simgrid
from boundary import boundary
from material import material
from input_grid import input_grid


class testing(unittest.TestCase):
    
    def setUp(self):
        
        self.n = 20
        self.m = 25
        
        cell_size = (0.1,0.1)
        
        self.test = simgrid((self.n, self.m), cell_size=cell_size)
        
        #grid and companion flat, for testing indices
        self.testflat = np.array(list(range(self.n * self.m)))
        self.testgrid = self.testflat.reshape(self.n, self.m)
        
    def testShape(self):
        
        self.assertEqual(self.test.shape, (self.n, self.m))
        
    def testCoords(self):
        
        #check coordlist length
        self.assertEqual(len(self.test.coords), self.n * self.m)
        
        #ensure equality
        testlist = list(itertools.product(range(self.n), range(self.m)))        
        self.assertEqual(self.test.coords, testlist)

    def testIndexing(self):

        idn = 15 #x id to check
        idm = 7 #y id to check

        #collect corresponding number and index it from flat array
        linear = self.testflat[self.testgrid[idn,idm]]
        
        #check for equality => indexing behaves in accordance with np.flatten()
        self.assertEqual(self.test.index(idn,idm), linear)
        
    def testCellSizing(self):
        
        n = 5
        m = 5
        
        #test explicit cell sizing
        test = simgrid((n,m), cell_size = (0.1,0.1))        
        self.assertEqual(test.cell_shape, (0.1,0.1))
        
        #test implicit cell sizing
        test = simgrid((n,m), grid_size = (0.5,0.5))        
        self.assertEqual(test.cell_shape, (0.1,0.1))
                
    def testIrregularGrid(self):
        
        placement = np.array([[True,True,False,False],
                              [True,True,True,True],
                              [True,True,False,False],
                              [True,True,False,True]])
        
        test = simgrid(placement, cell_size = (0.1,0.1))
        
        for c in test:
            connected = [x for x in c.bounds.values() if x != None]
            
            if len(connected) != 4:
                    
                print()   
                uniq = list(set(test))
                for u in uniq:
                    print(u, test.count(u))
                
                raise Exception("{} != 4 bounds in cell {} ({}, {})".format(len(connected), c.idx, *c.loc))
                  

if __name__ == "__main__":
    unittest.main()