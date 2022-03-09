import simsurvey_tools as sst
import pandas as pd
import simsurvey
import os

class Simul_lc:
    "Definition of a class that simule light curve"
    
    def __init__(self, folder_dir, sfd98File, rcidFile, csvFile, ZTF_Fields, z_range=(0.01, 0.1), dec_range=(-30, 90), n_det=1, 
                 ntransient=11, seed=70, threshold=1):
        """
        Parameters
        ----------
        folder_dir : str
            Name of the folder directory to find sfd98 file.
        z_range : (int,int)
            redshift range (default=(0.01, 0.1)).
        dec_range : (int,int)
            declinaison range for observation (default=(-30, 90)).
        n_det : int
            required number of detections (default=1).
        n_transient : int
            we can change the number of transientor the rate (default=11).
        seed : int
            default=70
        threshold : int
            S/N requirement for detection (default=1).
        """
        self.home_dir = os.environ.get('HOME')
        self.folder_dir = os.path.join(self.home_dir, folder_dir)
        
        self.sfd98_dir = os.path.join(self.folder_dir, sfd98File)
        self.rcid_dir = os.path.join(self.folder_dir, rcidFile)
        self.csv_dir = os.path.join(self.folder_dir, csvFile)
        self.ZTF_Fields_dir = os.path.join(self.folder_dir, ZTF_Fields)
        
        self.fields = sst.load_ztf_fields(filename=self.ZTF_Fields_dir)
        self.ccds = sst.load_ztf_ccds(filename=self.rcid_dir, num_segs=64) #it's rcid
        
        self.obs = pd.read_csv(self.csv_dir)
        self.simul = self.simul_lc(z_range, dec_range, ntransient, seed, n_det, threshold)
        
    def __call__(self):
        """
        Return
        ------
        lc : LightcurveCollection
            Collection of simulated light curve, to cheak the firt lc : lc[0]
        """
        survey = self.simul
        print(survey)
        lc = survey.get_lightcurves()
        
        return lc
        
    def simul_lc(self, z_range, dec_range, ntransient, seed, n_det, threshold):
        
        self.obs[self.obs['rcid']==26]
        self.obs['field'] = self.obs['field'].astype('int64')
        self.obs['time'] = self.obs['time'] - 2400000.5
        
        plan = simsurvey.SurveyPlan(time=self.obs['time'], band=self.obs['band'], zp=self.obs['zp'], obs_field=self.obs['field'],
                                obs_ccd=self.obs['rcid'],skynoise=self.obs['skynoise'], 
                                fields={k: v for k, v in self.fields.items() if k in ['ra', 'dec', 'field_id', 'width','height']}, 
                                      ccds=self.ccds)
        
        mjd_range = (plan.cadence['time'].min()- 30, plan.cadence['time'].max() + 30)
        
        tr = simsurvey.get_transient_generator(zrange=z_range, transient='Ia', template='salt2',
                                               dec_range=dec_range, mjd_range=mjd_range, sfd98_dir=self.sfd98_dir,
                                               ntransient=ntransient, seed=seed)
            
        survey = simsurvey.SimulSurvey(generator=tr, plan=plan, n_det=n_det, threshold=threshold)
        return survey