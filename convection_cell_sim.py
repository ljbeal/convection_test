# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28 21:35:41 2021

@author: pc
"""

import os
import sys
import math
import glob
import random
import itertools
import subprocess

import numpy as np
import matplotlib.pyplot as plt

import matplotlib
matplotlib.use('Agg')

#sim module imports
from cell import cell

#progess module
sys.path.append("../progress/")

from progress import progress

class simspace:
    
    def __init__(self, x_lim, y_lim):
        
        self.x_lim = x_lim
        self.y_lim = y_lim
        
        self.maxspeed = 10
        
        self.gridcoords = list(itertools.product(range(x_lim),range(y_lim)))
        
        mag = 1
        
        self.grid = []
        for x,y in self.gridcoords:
            u = random.randint(-mag,mag)
            v = random.randint(-mag,mag)
            
            self.grid.append(cell(x,y,u,v))
            
        self.stepdata = []
        
    def step(self):
        """
        
        step time forward, applying vector effects
        
        """
        
        #add random noise
        lo = -1
        hi = 1
        shape = (self.x_lim + 2, self.y_lim + 2)
        u_update = np.random.uniform(low = lo, high = hi, size = shape)
        v_update = np.random.uniform(low = lo, high = hi, size = shape)
        w_update = np.random.uniform(low = lo, high = hi, size = shape)
        
        for i in range(len(self.gridcoords)):
            
            x,y = self.gridcoords[i]
            
            u,v,w = self.grid[i].effect
            
            #sum all effects into an update array
            u_update[x:x+3,y:y+3] += u
            v_update[x:x+3,y:y+3] += v
            w_update[x:x+3,y:y+3] += w
            
        u_update = u_update[1:-1,1:-1].flatten()
        v_update = v_update[1:-1,1:-1].flatten()
        w_update = w_update[1:-1,1:-1].flatten()
        
        u_update = np.clip(u_update, a_min = -self.maxspeed, a_max = self.maxspeed)
        v_update = np.clip(v_update, a_min = -self.maxspeed, a_max = self.maxspeed)
        w_update = np.clip(w_update, a_min = -self.maxspeed, a_max = self.maxspeed)
        
        data = {
            "u":(u_update.min(), u_update.max()),
            "v":(v_update.min(), v_update.max()),
            "w":(w_update.min(), w_update.max())            
            }
        
        self.stepdata.append(data)
        
        for i in range(len(self.grid)):
            
            c = self.grid[i]
            u = u_update[i]
            v = v_update[i]
            w = w_update[i]
            
            c.update(u,v,w)
            
    def display(self, save = None):
        
        cells = []
        for c in self.grid:
            cells.append(c.data)
            
        cells = np.array(cells)
        
        X = cells[:,0]
        Y = cells[:,1]
        U = cells[:,2]
        V = cells[:,3]
        W = cells[:,4]
        
        zmap = np.array(W).reshape(self.x_lim,self.y_lim)
                
        fig, ax = plt.subplots(1,2,figsize=(30,15))
        ax[0].quiver(X,Y,U,V)
        im = ax[1].imshow(zmap, cmap = "seismic")
        plt.gca().invert_yaxis()
        ax[0].axis('off')
        ax[1].axis('off')
        
        fig.colorbar(im)
        
        # for x in range(self.x_lim-1):
        #     ax.axvline(x+.5)
        # for y in range(self.y_lim-1):
        #     ax.axhline(y+.5)
        
        if save is None:
            plt.show()
        else:
            plt.savefig(save, bbox_inches="tight")
            
        del fig, ax
        
if __name__ == "__main__":
    
    sim = simspace(30,30)
    
    folder = "./images/"
    if not os.path.exists(folder):
        os.mkdir(folder)
    
    old = glob.glob(folder+"*")
    for file in old:
        os.remove(file)
        
    steps = 100
    # fwidth = len(str(steps))
    fwidth = 4
    p = progress(steps)
    for i in range(steps):
        
        p()
        
        istr = str(i).rjust(fwidth,"0")
        
        sim.display(save="./images/{}.png".format(istr))
        sim.step()
        
    stats = sim.stepdata
        
        
    #ffmpeg -r 12 -f image2 -i %04d.png -vcodec libx264 -crf 25 test.mp4