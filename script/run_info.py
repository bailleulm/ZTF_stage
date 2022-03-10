from optparse import OptionParser
from ztf_info import get_info, get_selec
from ztf_hdf5 import Read_LightCurve
from astropy.table import Table, hstack, vstack
import astropy


def complete_lc(lc, snr):

    lc['SNR'] = lc['flux'] / lc['fluxerr']
    lc['phase'] = (lc['time'] - lc.meta['t0']) / (1-lc.meta['z'])
    idx = lc['SNR'] >= snr

    return lc[idx]


parser = OptionParser()

## Folder directory and Files names ##
parser.add_option('--csvInfo', type=str, default='ztf_stage/csv/selection_tab.csv',
                  help='csv file def [%default]')
parser.add_option('--csvSelect', type=str, default='ztf_stage/csv/seuil_name_selec.csv',
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
csv_tab = Table.read(csvInfo)
csv_tab_select = Table.read(csvSelect)
print(csv_tab)
print(csv_tab_select)

# read metadata
read_meta = Read_LightCurve(file_name=metaFile, inputDir=metaDir)
metadata = read_meta.get_table(path='meta')

print(metadata.meta)

lcDir = metadata.meta['directory']
lcName = metadata.meta['file_name']

read_lc = Read_LightCurve(file_name=lcName, inputDir=lcDir)

restab = Table()
restab.meta = metadata.meta
for meta in metadata:
    tt = Table(meta)
    path = meta['path']
    if 'bad' not in path:
        lc = read_lc.get_table(path)
        lc = complete_lc(lc, snr)
        res = get_info(lc, csv_tab)
        tt = hstack([tt, res])
    else:
        names = csv_tab['name'].tolist()
        vals = [[-1]]*len(csv_tab)
        tb = Table(vals, names=names)
        tt = hstack([tt, tb])
    restab = vstack([restab, tt])


# apply selection here
idx = True
print('baoo', csv_tab_select)
seltab = get_selec(restab, csv_tab_select)

# writing result
fOut = '{}/{}'.format(outDir, infoFile)
astropy.io.misc.hdf5.write_table_hdf5(
    seltab, fOut, path='meta', append=True, overwrite=True, serialize_meta=False)
