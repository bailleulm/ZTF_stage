from optparse import OptionParser
from ztf_simu import Simul_lc
from ztf_hdf5 import Write_LightCurve
from ztf_util import multiproc
from astropy.table import Table, vstack


def simu(index, params, j=0, output_q=None):

    params['ntransient'] = index[0]
    params['seed'] += j

    folder_dir = params['folder_dir']
    sfd98File = params['sfd98File']
    rcidFile = params['rcidFile']
    csvFile = params['csvFile']
    ztf_fields = params['ztf_fields']
    zmin = params['zmin']
    zmax = params['zmax']
    decmin = params['decmin']
    decmax = params['decmax']
    ndet = params['ndet']
    ntransient = params['ntransient']
    seed = params['seed']
    threshold = params['threshold']
    path_prefix = params['path_prefix']

    # lc simulation
    lc = Simul_lc(folder_dir=folder_dir, sfd98File=sfd98File, rcidFile=rcidFile,
                  csvFile=csvFile, ztf_fields=ztf_fields, z_range=(
                      zmin, zmax), dec_range=(decmin, decmax),
                  n_det=ndet, ntransient=ntransient, seed=seed, threshold=threshold)()

    if output_q is not None:
        return output_q.put({j: lc})
    else:
        return 0


parser = OptionParser()

## Folder directory and Files names ##
parser.add_option('--folder_dir', type=str, default='data',
                  help='folder directory [%default]')
parser.add_option('--sfd98File', type=str, default='sfd98',
                  help='sfd98 file name [%default]')
parser.add_option('--rcidFile', type=str, default='ZTF_corners_rcid.txt',
                  help='rcid file name [%default]')
parser.add_option('--csvFile', type=str, default='2018_all_logs_from_dr1_rcid_zp_from_masci.csv',
                  help='csv file name for observation [%default]')
parser.add_option('--ztf_fields', type=str, default='ZTF_Fields.txt',
                  help='ztf field file name for observation [%default]')
parser.add_option('--lcName', type=str, default='Data.hdf5',
                  help='Data file name [%default]')
parser.add_option('--metaName', type=str, default='Meta.hdf5',
                  help='Meta data file name [%default]')
parser.add_option('--outputDir', type=str, default='dataLC',
                  help='output directory [%default]')
parser.add_option('--path_prefix', type=str, default='SN',
                  help='path prefix for hdf5 [%default]')

## args ##
parser.add_option('--zmin', type=float, default=0.01,
                  help='min redshift [%default]')
parser.add_option('--zmax', type=float, default=0.1,
                  help='max redshift [%default]')
parser.add_option('--decmin', type=int, default=-30,
                  help='min declinaison [%default]')
parser.add_option('--decmax', type=int, default=90,
                  help='max declinaison [%default]')
parser.add_option('--ndet', type=int, default=1,
                  help='required number of detections [%default]')
parser.add_option('--ntransient', type=int, default=11,
                  help='number of transientor [%default]')
parser.add_option('--seed', type=int, default=70,
                  help='seed [%default]')
parser.add_option('--threshold', type=int, default=1,
                  help='S/N requirement for detection [%default]')
parser.add_option('--nproc', type=int, default=1,
                  help='number of procs for multiprocessing [%default]')

opts, args = parser.parse_args()

folder_dir = opts.folder_dir
sfd98File = opts.sfd98File
rcidFile = opts.rcidFile
csvFile = opts.csvFile
ztf_fields = opts.ztf_fields
lcName = opts.lcName
metaName = opts.metaName
outputDir = opts.outputDir
path_prefix = opts.path_prefix

zmin = opts.zmin
zmax = opts.zmax
decmin = opts.decmin
decmax = opts.decmax
ndet = opts.ndet
ntransient = opts.ntransient
seed = opts.seed
threshold = opts.threshold
nproc = opts.nproc

params = {}
params['folder_dir'] = folder_dir
params['sfd98File'] = sfd98File
params['rcidFile'] = rcidFile
params['csvFile'] = csvFile
params['ztf_fields'] = ztf_fields
params['zmin'] = zmin
params['zmax'] = zmax
params['decmin'] = decmin
params['decmax'] = decmax
params['ndet'] = ndet
params['ntransient'] = ntransient
params['seed'] = seed
params['threshold'] = threshold
params['path_prefix'] = path_prefix

# the multiprocessing is done according to ntransients

if __name__ == '__main__':
    step = int(ntransient/nproc)
    ffi = [step]*nproc
    lc_dict = multiproc(ffi, params, simu, nproc, gather=False)

    # write LC and metadata
    Write = Write_LightCurve(
        outputDir=outputDir, file_data=lcName, file_meta=metaName, path_prefix=path_prefix)
    rlc = []
    meta_rejected = Table()
    for i, lcl in lc_dict.items():
        if lcl.meta_rejected is not None:
            meta_rejected = vstack([meta_rejected, Table(lcl.meta_rejected)])
        for lc in lcl:
            rlc.append(lc)

    data = Write.write_data(rlc, meta_rejected)
