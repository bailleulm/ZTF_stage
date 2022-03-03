#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import simsurvey_tools as sst
import pandas as pd
import simsurvey
import os

class Simul_lc:
    "Definition of a class that simule light curve"
    
    def __init__(self, folder_dir,  z_range=(0.01, 0.1), dec_range=(-30, 90), n_det=1, 
                 ntransient=11, seed=70, threshold=1):
        
        self.folder_dir = folder_dir
        self.z_range = z_range
        self.dec_range = dec_range
        self.ntransient = ntransient
        self.seed = seed
        self.n_det = n_det
        self.threshold = threshold
        
        self.sfd98_dir = os.path.join(folder_dir, 'sfd98')
        self.fields = sst.load_ztf_fields()
        self.ccds = sst.load_ztf_ccds(filename='data/ZTF_corners_rcid.txt', num_segs=64) #it's rcid
        
        self.obs = pd.read_csv('data/2018_all_logs_from_dr1_rcid_zp_from_masci.csv')
        
    def simul_lc(self, ntrans=False):
            
        self.obs[self.obs['rcid']==26]
        self.obs['field'] = self.obs['field'].astype('int64')
        self.obs['time'] = self.obs['time'] - 2400000.5
        
        plan = simsurvey.SurveyPlan(time=self.obs['time'], band=self.obs['band'], zp=self.obs['zp'], obs_field=self.obs['field'],
                                obs_ccd=self.obs['rcid'],skynoise=self.obs['skynoise'], 
                                fields={k: v for k, v in self.fields.items() if k in ['ra', 'dec', 'field_id', 'width', 'height']}, ccds=self.ccds)
        
        mjd_range = (plan.cadence['time'].min()- 30, plan.cadence['time'].max() + 30)
        
        if not ntrans:
            tr = simsurvey.get_transient_generator(zrange=self.z_range, transient='Ia', template='salt2', dec_range=self.dec_range,
                     mjd_range=mjd_range, sfd98_dir=self.sfd98_dir, ntransient=self.ntransient, seed=self.seed)
        else:
            tr = simsurvey.get_transient_generator(zrange=self.z_range, transient='Ia', template='salt2', dec_range=self.dec_range,
                     mjd_range=mjd_range, sfd98_dir=self.sfd98_dir, seed=self.seed)
            
        survey = simsurvey.SimulSurvey(generator=tr, plan=plan, 
                                       n_det=self.n_det, threshold=self.threshold)
        lc = survey.get_lightcurves(progress_bar=True, notebook=True)
        
        return lc

