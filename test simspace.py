# -*- coding: utf-8 -*-
"""
Created on Sun May  9 13:15:12 2021

@author: pc
"""

import unittest
import itertools

import numpy as np

from simspace import simgrid


class testing(unittest.TestCase):
    
    def setUp(self):
        
        self.n = 20
        self.m = 25
        
        self.test = simgrid((self.n, self.m))
        
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
                

if __name__ == "__main__":
    unittest.main()