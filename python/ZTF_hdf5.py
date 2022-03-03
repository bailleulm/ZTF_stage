#!/usr/bin/env python
# coding: utf-8

# In[91]:


#!/usr/bin/env python
# coding: utf-8

# In[253]:


import h5py
import ast
from astropy.table import QTable, Table, Column, vstack
import astropy.units as u
import astropy
import numpy as np
import simsurvey
import simsurvey_tools as sst
import matplotlib.pylab as plt
import pandas as pd
import os

class Write_LightCurve:
    "Definition of a class that records light curves and/or their meta data in an hdf5 file"
    
    def __init__(self, outputDir = 'dataLC', file_data = 'Data.hdf5', file_meta = 'Meta.hdf5'):
        """
        Parameters
        ----------
        file_data : str, ops
            Name of the data file that you want to write (default='Data.hdf5').
        file_meta : str, ops
            Name of the meta data file that you want to write (default='Meta.hdf5').
        """

        self.Summary = Table()
        self.List = ['z', 't0', 'x0', 'x1', 'c', 'mwebv', 'ra', 'dec', 'mwebv_sfd98', 'idx_orig']
        home_dir = os.environ.get('HOME')
        folder_dir = os.path.join(home_dir, outputDir)
        data_dir = os.path.join(folder_dir, file_data)
        self.meta_dir = os.path.join(folder_dir, file_meta)
        
        if not os.path.exists(folder_dir):
            os.makedirs(file_dir)
        elif (os.path.isfile(data_dir) and os.path.isfile(self.meta_dir)):
            os.remove(data_dir)
            os.remove(self.meta_dir)
            
        self.file_data = h5py.File('{}/{}'.format(folder_dir, file_data), 'w')
        self.file_meta = h5py.File('{}/{}'.format(folder_dir, file_meta), 'w')
        
    def write_data(self, path, lc, serialize_meta=True):
        """
        Parameters
        ----------
        path : str-
            Name of the key of the data file that you want to write.
        lc : LightcurveCollection
            List of AstropyTable with simulated lightcurve.
        """
       
        if isinstance(lc, astropy.table.table.Table):
            meta = lc.meta
            lc.meta = dict(zip(self.List, [meta[k] for k in self.List]))
            
            astropy.io.misc.hdf5.write_table_hdf5(lc, self.file_data, path=path, append=True,
                                                  overwrite=True, serialize_meta = serialize_meta)
        
            meta = dict(zip(lc.meta.keys(), [[lc.meta[k]] for k in lc.meta.keys()]))
            meta['path'] = [path]
            self.Summary = vstack([self.Summary, Table(meta)])
            
        else :
            print('lc is not an astropy.table.table.Table type', type(lc))
            for i, lc_b in enumerate(lc):
                self.write_data('SN_{}'.format(i), lc_b)
            
    def write_meta(self):
        self.Summary.meta["directory"]=self.meta_dir
        self.Summary.meta["file_name"]='Meta.dhf5'
        print(self.Summary.meta)
        
        astropy.io.misc.hdf5.write_table_hdf5(self.Summary, self.file_meta, path='meta', append=True,
                                                  overwrite=True, serialize_meta=True)
    
    def Tab_metaRejected(self, lc):
        meta_rej = Table(lc.meta_rejected)
        r = []
        for i, row in enumerate(meta_rej):
            path = 'bad_{}'.format(i)
            r.append(path)
            c = Column(r)
        meta_rej.add_column(c, name='path')
        return meta_rej

# In[255]:


class Read_LightCurve:
    
    def __init__(self, file_name='Data.hdf5', inputDir = 'dataLC'):
        """
        Parameters
        ----------
        file_name : str
            Name of the hdf5 file that you want to read.
        """
        self.file_name = file_name
        home_dir = os.environ.get('HOME')
        folder_dir = os.path.join(home_dir, inputDir)
        
        self.file = h5py.File('{}/{}'.format(folder_dir, file_name), 'r')
        
        
    def get_path(self):
        
        K = []
        with self.file as f:
            K.append([key for key in f.keys()])
        return K
    
    def Read_file(self, path):
        """
        Parameters
        ----------
        path : str
            hdf5 path for light curve.
            
        Returns
        -------
        AstropyTable
            Returns the reading of an .hdf5 file as an AstropyTable.
        """
        
        return astropy.io.misc.hdf5.read_table_hdf5(self.file, path=path, character_as_bytes=False)


# In[257]:


class Plot_LightCurve:
    
    def __init__(self, lc_sn=None):
        """
        Parameters
        ----------
        lc_sn : AstropyTable, ops
            AstropyTable containing light curves and their metadata (default=None).
        """
        self.lc_sn = lc_sn
    
    def Plot(self, file_name, path, figsize): # axs
        """
        Parameters
        ----------
        file_name : str
            name of the file to process.
        path : str
            hdf5 path for light curve.
        figsize : tuple (float, float)
            Size of my figure.
        """
        Self = Read_LightCurve()
        Data = Self.Read_hdf5_file(file_name=file_name, path=path)
        
        band = ['ztfr', 'ztfg', 'ztfi']
        dico = dict(zip(band, [(0,0), (0,1), (1,0)]))
        
        fig, axs = plt.subplots(2, 2, figsize=figsize)
        for color in band :
        
            mask_band = Data['band'] == color
            new_lc_sn = Data[mask_band]
            time = new_lc_sn['time']
            flux = new_lc_sn['flux']
            err = new_lc_sn['fluxerr']

            ipos = dico[color][0]
            jpos = dico[color][1]
        
            axs[ipos, jpos].errorbar(time, flux , yerr = err, fmt='.',
                                         ecolor='red', capsize=5, alpha = 0.5)
            axs[ipos, jpos].plot(time, flux)
            axs[ipos, jpos].set_title('Light Curve for {} band'.format(color))
            axs[ipos, jpos].grid(True)
            plt.subplots_adjust(hspace=0.3)
            
    def Histo(self, file_name, path, figsize):
        """
        Parameters
        ----------
        file_name : str
            name of the file to process
        path : str
            hdf5 path for light curve
        figsize : tuple (float, float)
            Size of my figure.
        """
        
        Self = Read_LightCurve()
        Data = Self.Read_hdf5_file(file_name=file_name, path=path)
        var = ['z', 'x0', 'x1', 'c']
        dico = dict(zip(var, [(0,0), (0,1), (1,0), (1,1)]))

        fig, axs = plt.subplots(2, 2, figsize=figsize)
        for variables in var :
            ipos = dico[variables][0]
            jpos = dico[variables][1]
        
            axs[ipos, jpos].hist(Data[variables], alpha = 0.3)
            axs[ipos, jpos].set_title('Histo var {}'.format(variables))

