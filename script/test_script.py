from optparse import OptionParser
from ztf_simu import Simul_lc
from ZTF_hdf5 import Write_LightCurve, Read_LightCurve, Plot_LightCurve

parser = OptionParser()

## Folder directory and Files names ##
parser.add_option('--folder_dir', type=str, default='/Users/manon/ZTF/data/',
                  help='folder directory [%default]')
parser.add_option('--sfd98File', type=str, default='sfd98',
                  help='sfd98 file name [%default]')
parser.add_option('--rcidFile', type=str, default='ZTF_corners_rcid.txt',
                  help='rcid file name [%default]')
parser.add_option('--csvFile', type=str, default='2018_all_logs_from_dr1_rcid_zp_from_masci.csv',
                  help='csv file name for observation [%default]')
 
parser.add_option('--DataFile', type=str, default='Data',
                  help='csv file name for observation [%default]')
parser.add_option('--MetaFileName', type=str, default='Meta.hdf5',
                  help='csv file name for observation [%default]')

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


opts, args = parser.parse_args()

folder_dir = opts.folder_dir
sfd98File = opts.sfd98File
rcidFile = opts.rcidFile
csvFile = opts.csvFile
DataFile = opts.DataFile
MetaFileName = opts.MetaFileName

zmin = opts.zmin
zmax = opts.zmax
decmin = opts.decmin
decmax = opts.decmax
ndet = opts.ndet
ntransient = opts.ntransient
seed = opts.seed
threshold = opts.threshold

lc = Simul_lc(folder_dir=folder_dir, sfd98File=sfd98File, rcidFile=rcidFile, 
                csvFile =csvFile, z_range=(zmin, zmax), dec_range=(decmin, decmax),
                  n_det=ndet, ntransient=ntransient, seed=seed, threshold=threshold)()

Write = Write_LightCurve()
data = Write.write_data(DataFile, lc)
meta = Write.write_meta()

Read = Read_LightCurve(file_name=MetaFileName)
read_meta = Read.Read_file(path='meta')

if lc.meta_rejected is not None:
    meta_rej = Write.Tab_metaRejected(lc)
    for i, rows in enumerate(meta_rej):
        read_meta.add_row(rows)

print("Successfully simulated light curve ")
