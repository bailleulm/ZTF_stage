from optparse import OptionParser
from ztf_info import get_selec, Info
import astropy

parser = OptionParser()

parser.add_option('--csvInfo', type=str, default='ztf_stage/csv/info.csv',
                  help='csv file def [%default]')
parser.add_option('--csvSelect', type=str, default='ztf_stage/csv/selection.csv',
                  help='csv selec def [%default]')
parser.add_option('--metaFile', type=str, default='Meta.hdf5',
                  help='meta file name to process [%default]')
parser.add_option('--metaDir', type=str, default='dataLC',
                  help='meta dir [%default]')
parser.add_option('--snr', type=float, default=5.,
                  help='SNR sel for info estimation [%default]')
parser.add_option('--infoFile', type=str, default='Meta_info.hdf5',
                  help='info file name to process [%default]')
parser.add_option('--outputDir', type=str, default='dataLC',
                  help='outputdir [%default]')

opts, args = parser.parse_args()

csvInfo = opts.csvInfo
csvSelect = opts.csvSelect
metaFile = opts.metaFile
metaDir = opts.metaDir
snr = opts.snr
infoFile = opts.infoFile
outDir = opts.outputDir

# load csv  file in Table
tab_info = astropy.io.ascii.read(csvInfo, format='csv', comment='#')
tab_select = astropy.io.ascii.read(csvSelect, format='csv', comment='#')

# get infos
info = Info(metaFile, metaDir, tab_info, snr)
restab = info()

# apply selection
seltab = get_selec(restab, tab_select)

print(seltab['n_phase_neg', 'n_phase_pos',
             'n_phase_min', 'n_phase_max', 'sel'])

# writing result
fOut = '{}/{}'.format(outDir, infoFile)
astropy.io.misc.hdf5.write_table_hdf5(
    seltab, fOut, path='meta', append=True, overwrite=True, serialize_meta=False)
