#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
By Cordell Newmiller

The rainbowplot function plots each row of a 2D array as a color on a
single figure. Useful for getting a "side view" of your data. 

Usage: 
    ax = rainbowplot(data)
    ax = rainbowplot(x,data)
    
Arguments:
    
    x:              An optional scalar, vector, or grid (e.g. from meshgrid) 
                        that gives dimension to the horizontal axis. If x
                        is not supplied, the horizontal axis will be marked 
                        by array index.
    
    data:           The 2D array of values to be plotted. 

Other Arguments:
    
    fmt:            A matplotlib format string, e.g. fmt='--x'
    
    xrange, drange: Pairs determining the bounds for plotting. 
                        e.g. xrange=(-10,10)
                        Defaults to ten percent beyond each 
                        respective extremum value. 
                        
    transpose:      If transpose=True, rainbowplot will plot each column as
                        a color, rather than each row.
                        Defaults to False.
                        
    cbar:           If cbar=True, a colorbar will be added to identify 
                        which row is which color.
                        Defaults to False.

    colormapname:   The matplotlib color map from which to draw colors.
                        Defaults to 'rainbow'
                For other color options, see
                matplotlib.org/examples/color/colormaps_reference.html
    
    bgcolor:        Plot background color. Defaults to off-white.
    
    show:           A vector of booleans with the same length as the 
                        number of rows to be plotted. Used to plot only
                        certain desired rows, corresponding to 'True'
                        values in this vector. 
                        Defaults to plotting all rows. 
                        
    **kwargs:       Other keyword arguments can be passed to pyplot, 
                        such as 'title' or 'xlabel' 

Returns:
    
    ax:             the matplotlib axes object, which can be further
                        modified (e.g. to add labels)

"""

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import colors as cl
from matplotlib import colorbar as cb
from mpl_toolkits.axes_grid1 import make_axes_locatable
from astropy.io import fits


def displayrange(x,margin=0.1):
    x=x[np.isfinite(x)]
    xrange=(x.min(),x.max()) + margin*(x.max()-x.min())*np.array([-1,1])
    return(xrange)


def rainbowplot(x,data=None,
                fmt='',
                xrange=None,drange=None,
                transpose=False,
                cbar=False,
                colormapname='rainbow',
                bgcolor=(.9,.9,.9),
                show=None,
                **kwargs):
    
    
    # Interpret inputs
    if data is None: # Create x grid using indices
        data = x.copy()
        if transpose: data=data.T
        ny = data.shape[1]
        nx = data.shape[0]
        x = np.outer(np.arange(0,nx), np.ones(ny))
    else:
        if transpose: data=data.T
        ny = data.shape[1]
        if np.ndim(x) is 0: # cast x from scalar to grid
            nx = data.shape[0]
            x = np.outer(x*np.arange(0,nx), np.ones(ny))
        elif np.ndim(x) is 1: # cast x from vector to grid
            x = np.outer(x, np.ones(ny))
        
    assert x.shape == data.shape, ('Lengths of "x" and "data" are not compatible'
        + '\n x grid shape: '+str(np.shape(x))
        + '\n   data shape: '+str(np.shape(data)))
        
    if show is None: show = [True]*ny
    if len(show) is not ny:
        print('Length of "show" should match the length of the' +
              ' respective dimension in "data"')
        return(1)
    
    if xrange is None: xrange=displayrange(x)
    if drange is None: drange=displayrange(data)
    
    
    # Get colormap
    colormap=plt.get_cmap(colormapname)
    
    # Pull the ny specific color values for our plot 
    colors=colormap(np.linspace(0,1,ny))
    
    # Define blank axes
    ax = plt.subplot(1,1,1,**kwargs)
    
    # Plot each row
    for i in range(ny):
        if show[i]: 
            ax.plot(x[:,i],data[:,i],fmt,color=colors[i])
    
    ax.set_xlim(xrange)
    ax.set_ylim(drange)
    ax.set_facecolor(bgcolor)
    
    # Plot optional colorbar
    if cbar: 
        lmap=cl.ListedColormap(colors)
        divider=make_axes_locatable(ax)
        cbax=divider.append_axes('right',size='2%',pad=0.05)
        cbounds = np.arange(0,ny+1)
        cb.ColorbarBase(cbax,cmap=lmap,
                        boundaries=cbounds-.5,ticks=cbounds[:-1])        
    
    # Display plot
    plt.show()
    
    return(ax)




# Example of usage
def rainbowexample():
    xvec=np.linspace(0,1,5)
    plt.clf()
    exampledata =np.outer(np.arange(-2,3),np.arange(2,7))
    print(exampledata)
    rainbowplot(xvec,exampledata,
                     cbar=True,
                     title='Example Plot',
                     fmt='--',
                     drange=(-20,20),
                     xlabel='Label for X')


# What I wrote this to help visualize
def plotjupiter(**kwargs):
    filename='JupS0Bled.fits'
    hdulist=fits.open(filename)
    S0data = hdulist[0].data[0]
    
    scale = hdulist[0].header['CD1_1']
    
    ax = rainbowplot(scale,S0data,transpose=True,xlabel='Arcsec',**kwargs)
    return(ax)
    

