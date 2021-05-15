# -*- coding: utf-8 -*-
"""
Created on Thu May  6 11:47:17 2021

@author: pc
"""

import os
import copy
import glob
import random
import itertools

import matplotlib
matplotlib.use('Agg')

import numpy as np
import matplotlib.pyplot as plt

from datetime import datetime

#module imports
from cell import cell
from boundary import boundary
from material import material



class simgrid:

    """
    iterable grid object
    allows for cell storage and easy iteration without faffing with x,y or i
    """
    
    def __init__(self, shape, 
                 cell_obj = None, bound_obj = None, material_obj = None,
                 cell_size = None, grid_size = None,):
        
        #shape derivation and truth mapping for non-rectangular areas
        if type(shape) in (list, tuple):
            n = shape[0]
            m = shape[1]
            
            self.mapping = np.ones((n, m), dtype = bool)
        
        #bool array passed for non-rectangular shapes
        elif type(shape) == np.ndarray:
            n, m = shape.shape
            
            self.mapping = shape
            
        else:
            raise Exception("shape derivation failed from type ", type(shape))
        
        #final grid handling
        self._n = n # number of cells in x
        self._m = m # number of cells in y
        # generate list of x,y coords
        self._coords = list(itertools.product(range(n), range(m)))
        
        #cell sizing
        if cell_size != None: # prefer explicit cell size
            self._cell_w = cell_size[0]
            self._cell_h = cell_size[1]
        elif grid_size != None: # else calculate from axis
            self._cell_w = grid_size[0]/self._n
            self._cell_h = grid_size[1]/self._m
        else:
            raise Exception("require (x,y) size for grid or cells /m")
            
        
        #object handling
        #save object if passed, initialise cell and boundary lists
        self.obj = {"cell":cell_obj, "bound":bound_obj, "material":material_obj}
        self.cells = {} #linear dict of cells
        self.bounds = {} #linear dict of boundaries
        
    # dunder functions
    def __iter__(self):
        #iterating the grid will yield each cell
        for item in self.cells.values():
            yield(item)
            
    def __len__(self):
        return(len(self.cells))
    
    def __repr__(self):
        #formatted string representation of the grid layout
        
        ret = ""
        
        #if we have stuff in storage, show a representation of that
        if len(self.cells) != 0:
            ret += "{} stored cells:".format(len(self.cells))
            
            #poor attempt to make the output prettier
            #guess it would work if written to file?
            #accounts for max n, m, idx lengths as string
            textlen = len(str(self.cells[list(self.cells.keys())[-1]]))
            
            for row in self.grid:
                
                ret += "\n" + " | ".join([str(x).ljust(textlen) for x in row])
                
            ret += "\n\n{} boundary connections:".format(len(self.bounds))
            for b in self.bounds.values():
                ret += "\n" + str(b)
                
        else:
            ret += "grid coords:"
            
        ret += "\n"
        
        return(ret)
    
    # grid spatial properties
    @property
    def shape(self):
        #n, m shape of grid
        return(self._n, self._m)
        
    @property
    def coords(self):
        #iterable of coordinate pairs
        return(self._coords)
    
    @property
    def cell_shape(self):
        return(self._cell_w,self._cell_h)
    
    #supplimentary property functions
    def index(self, x, y):
        #return flat index of x,y point on grid
        return(x*(self._m) + y)
    
    #grid mapping functions
    def validate_obj(self, name, obj):
        #check that an object is passed for grid filling
        #return initialised ones if not
        v_obj = None
        
        if self.obj[name] != None:
            v_obj = self.obj[name]
        elif obj != None:
            v_obj = obj
            self.obj[name] = obj
        else:
            raise Exception(name + " object required")
            
        return(v_obj)
        
    def fill(self, cell_obj = None, bound_obj = None, material_obj = None):
        
        """
        
        create grid of objects, taking into account mapping
        
        """
        # gather objects
        cell = self.validate_obj("cell", cell_obj)
        bound = self.validate_obj("bound", bound_obj)
        mat = self.validate_obj("material", material_obj)
        # grid shape and cell size
        n, m = self.shape
        w, h = self.cell_shape
        
        store = [] #storage for cells
        boundary_names = {} #dict for boundary condition checking
        idx = 0 #cell id
        print("setting up cell grid")
        for i in range(n):
            
            temp = []            
            for j in range(m): #standard row/col looping
                
                place = self.mapping[i,j] #is there a cell here?
                
                if place:
                    # if there is a cell required at this location
                    # add to grid, and append to cells list
                    c = cell(i, j, idx, w, h, mat)
                    
                    temp.append(c)
                    self.cells[idx] = c
                    
                    # handle boundary conditions
                    # generate names based on half-coordinates
                    # e.g. a cell at 1,1 would have bounds at
                    # n1 m0.5, n1 m1.5, n0.5 m1, n1.5 m1
                    base = "n{} m{}"
                    t = base.format(i, j-0.5)
                    b = base.format(i, j+0.5)
                    l = base.format(i-0.5, j)
                    r = base.format(i+0.5, j)
                    
                    adj = (t,b,l,r)
                    
                    # for each surrounding half-coord;
                    for name in adj:
                        # if this is a new region, add to dict
                        if name not in boundary_names:
                            boundary_names[name] = [idx]
                        #if this region exists, append this id
                        else:
                            boundary_names[name] += [idx]                 
                    
                    idx += 1
                    
                else:
                    temp.append(None)
                
            store.append(temp)
        
        self.grid = np.array(store)
        
        print("connecting cells")
        #parse boundary list
        idx = 0
        for half in boundary_names.keys():
            ids = boundary_names[half] # cell ids in this connection
            
            cells = [self.cells[x] for x in ids] # grab references
            thisbound = bound(mat, *cells)
            
            self.bounds[idx] = thisbound # generate and register this boundary
            
            #ensure connection is registered in the cells also
            # print("bound {}; {}".format(idx, half))
            
            # determine if horizontal or vertical based on decimal location
            # define h or v bound based on which id we check for the decimal
            # id 0 corresponds to orientation as a line drawn between cells
            # e.g. vert = True connects cells above and below (top/bottom)
            vert = "." in half.split()[0]
            # print(vert)
            
            if vert:
                orient = ("b","t")
            else:
                orient = ("r","l")
            
            if len(cells) == 2:
                # if we have both cells, can make assumptions about the orientation
                    
                baseline = list(zip(cells,orient))
            
                for cell, side in baseline:
                    # print("\timplicit",cell,side)
                    
                    cell.update_bounds(side, thisbound)
                    
            else:
                #otherwise we have to explicitly check orient
                if "-" in half:
                    side = orient[1]
                else:
                    side = orient[0]
                   
                cell = cells[0] 
                   
                # print("\texplicit",cell,side)
                    
                cell.update_bounds(side, thisbound)
            
            # print()
            
            idx += 1
            
        
    # global update and extraction functions  
                
    @property
    def temp(self):        
        # get param from each cell and return        
        data = np.zeros((self.shape))
        for c in self:
            
            t = c.t
            # print(t)
            data[c.x, c.y] = round(t,2)
            
        return(data)
    
    @property
    def e(self):
        # get param from each cell and return        
        data = np.zeros((self.shape))
        for c in self:
            
            t = c._e
            # print(t)
            data[c.x, c.y] = round(t,2)
            
        return(data)        
    
    @property
    def state(self):
        pass
    
    
    # calculate DT
    def dt(self, energy = None, step = 1):
        
        #ensure sensible energy grid for energy injection
        if type(energy) != np.ndarray:
            energy = np.zeros(self.shape)
            
        assert energy.shape == self.shape
        
        energy = energy.flatten()
        
        # testb = list(self.bounds.values())[int(len(self.bounds)/2)]
        # testc = testb.c1
        idx = 0
        for c in self:
            #first stage - energy increase and dump to bounds
            e = energy[idx]
            
            c.move_energy(e)
            
            idx += 1
            
            c.dt(step)
            
        for b in self.bounds.values():
            
            b.dt(step)
        
        u = np.zeros(self.shape)
        v = np.zeros(self.shape)
        for c in self:
            x, y = c.loc
            
            u[x,y], v[x,y] = c.get_vect()
            
        return(u,v)
    
if __name__ == "__main__":
    
    fig = False
    
    placement = np.array([[True, True, False],
                          [True, True, True],
                          [True, True, False]])
    
    placement = 15,15
    
    
    # water
    # cs 4184 J /k /kg    
    # rho 997 kg /m3
    water = material()
    water.update_material({"cp": 4184, "rho": 997})
    
    grid = simgrid(placement, cell, boundary, water, cell_size = (0.1, 0.1))    
    grid.fill()
    
    if not os.path.exists("./tests/"):
        os.mkdir("./tests/")
    
    data = []
    fwidth = 4
    
    
    x2 = int(grid.shape[0]/2)
    y2 = int(grid.shape[1]/2)
    
    x2 = 3
    y2 = 3
    
    r = 2
    
    fig = True
    
    items = glob.glob("./tests/*")
    
    for item in items:
        os.remove(item)
    
    steps = 150
    
    
    t0 = datetime.now()
    for i in range(steps):
        
        e = np.zeros(grid.shape)
        if i < 50:
            # e[x2-r+1:x2+r, y2-r+1:y2+r] = 10000
            e[y2,:] = 10000
            e[:,x2] = 10000
        
        # print()
        print("processing timestep {}".format(i+1))
        t = grid.temp
        data.append(t)
        u,v = grid.dt(e)
        
        if fig:
            fig, ax = plt.subplots(1,1,figsize=(15,15))
            
            im = ax.imshow(t, cmap = "seismic", vmin = 273, vmax = 323, origin='lower')
            ax.quiver(u,v)
            fig.colorbar(im)
            
            title = "timestep "
            title += "{}/{}".format(i+1,steps).ljust(len(str(steps))*2+2)
            
            ax.set_title(title)
            
            istr = str(i).rjust(fwidth,"0")
            plt.savefig("./tests/{}.png".format(istr), bbox_inches="tight")
            
    dt = (datetime.now() - t0).total_seconds()
    print("time taken: {:.2f}s".format(dt))
        
    #ffmpeg -r 12 -f image2 -i %04d.png -vcodec libx264 -crf 25 test.mp4