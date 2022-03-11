import os

ntransient = 88
nproc = 8

# simulation
simu_script = 'ztf_stage/script/run_simulation.py'
simu_cmd = 'python {}  --ntransient {} --nproc {}'.format(
    simu_script, ntransient, nproc)
os.system(simu_cmd)

# info+selec
info_script = 'ztf_stage/script/run_info.py'
info_cmd = 'python {}'.format(info_script)
os.system(info_cmd)

# fit
fit_script = 'ztf_stage/script/run_fit_lc.py'
fit_cmd = 'python {} --nproc {}'.format(fit_script, ntransient, nproc)
os.system(fit_cmd)
