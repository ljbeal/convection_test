# -*- coding: utf-8 -*-
"""
Created on Thu May  6 11:47:17 2021

@author: pc
"""

import random
import itertools

import numpy as np

#module imports
from cell import cell
from boundary import boundary


class simgrid:

    """
    iterable grid object
    allows for cell storage and easy iteration without faffing with x,y or i
    """
    
    def __init__(self, shape, 
                 cell_obj = None, bound_obj = None,
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
        self.obj = {"cell":cell_obj, "bound":bound_obj}
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
        
    def fill(self, cell_obj = None, bound_obj = None):
        
        """
        
        create grid of objects, taking into account mapping
        
        """
        # gather objects
        cell = self.validate_obj("cell", cell_obj)
        bound = self.validate_obj("bound", bound_obj)
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
                    c = cell(i, j, w, h, idx)
                    
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
            thisbound = bound(*cells)
            
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
    def validate_update(self, inp):
        
        t = type(inp)
        
        if t in (str,int,float):
            return([inp])
        
        elif t in (list, tuple):
            return(inp)
        
        elif t in(dict,):
            return(zip(inp.keys(), inp.values()))
        
        else:
            raise Exception("unknown validationf or type ", t)

      
    def update_material(self, attrs, vals = None):
        
        if vals != None:
            attrs = self.validate_update(attrs)
            vals = self.validate_update(vals)
            
            upd = zip(attrs, vals)
            
        else:
            upd = self.validate_update(attrs)
        
        
        for c in self:
            
            for a,v in upd:
            
                c.update_material(a, v)
            
    
if __name__ == "__main__":
    
    placement = np.array([[True, True, False],
                          [True, True, True],
                          [True, True, False]])
    
    # placement = 10,10
    
    grid = simgrid(placement, cell, boundary, cell_size = (0.1, 0.1))    
    grid.fill()
    
    # water
    # cs 4184 J /k /kg    
    # rho 997 kg /m3
    grid.update_material({"cp": 4184,
                          "rho": 997})
    
    print(list(grid)[0].mat_vals)