#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import sncosmo

class SN_fit:
    "Definition of a class fit lightcurve"
    
    def __init__(self,lc, z_bounds={'z':(0.01, 0.1)}):
        """
        Parameters
        ----------
        lc : AstropyTable
            AstropyTable of your selecting light curve.
        """
        self.lc = lc
        self.model = sncosmo.Model(source='salt2')
        self.param = ['z', 't0', 'x0', 'x1', 'c']
        self.z_bounds = z_bounds
    
    def fit_sn(self):
        try:
            result, fitted_model = sncosmo.fit_lc(self.lc, self.model, self.param, bounds=self.z_bounds)
            return result, fitted_model
        except:
            return print("WARNING : That was no valid light curve.")
    
    def plot_sn(self):
        fit = self.fit_sn()
        return sncosmo.plot_lc(self.lc, model=fit[1], errors=fit[0].errors)
    
    def info(self):
        result = self.fit_sn()[0]
        print("Number of chi^2 function calls:", result.ncall)
        print("Number of degrees of freedom in fit:", result.ndof)
        print("chi^2 value at minimum:", result.chisq)
        print("model parameters:", result.param_names)
        print("best-fit values:", result.parameters)
        print("The result contains the following attributes:\n", result.keys())
        print("Errors corresponding to the different fitting parameters:\n", result.errors)
        print('result.success: \n', result.success)
        print('result.message: \n', result.message)
        print('result.vparam_names: \n', result.vparam_names)
        print('Matrice de covariance : \n', result.covariance)
        print('result.nfit: \n', result.nfit)
        print('result.data_mask: \n', result.data_mask)
