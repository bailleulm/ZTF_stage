import os
from optparse import OptionParser

parser = OptionParser()
parser.add_option('--nproc', type=int, default=1,
                  help='number of procs for multiprocessing [%default]')
parser.add_option('--ntransient', type=int, default=11,
                  help='number of transientor [%default]')
parser.add_option('--zmin', type=int, default=0.01,
                  help='zmin [%default]')
parser.add_option('--zmax', type=int, default=0.1,
                  help='zmax [%default]')

opts, args = parser.parse_args()
ntransient = opts.ntransient
nproc = opts.nproc

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
fit_cmd = 'python {} --nproc {}'.format(fit_script, nproc)
os.system(fit_cmd)
