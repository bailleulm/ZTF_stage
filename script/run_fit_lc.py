from optparse import OptionParser
from ztf_fit import SN_fit_tab
from ztf_hdf5 import Read_LightCurve
import astropy

parser = OptionParser()

parser.add_option('--metaFileInput', type=str, default='Meta_info.hdf5',
                  help='meta file name to process [%default]')
parser.add_option('--metaDirInput', type=str, default='dataLC',
                  help='meta dir [%default]')
parser.add_option('--metaFileOutput', type=str, default='Meta_fit.hdf5',
                  help='meta file name for output [%default]')
parser.add_option('--metaDirOutput', type=str, default='dataLC',
                  help='meta dir for output [%default]')
opts, args = parser.parse_args()

metaFileInput = opts.metaFileInput
metaDirInput = opts.metaDirInput
metaFileOutput = opts.metaFileOutput
metaDirOutput = opts.metaDirOutput

meta = Read_LightCurve(file_name=metaFileInput, inputDir=metaDirInput)
metaTable = meta.get_table(path='meta')

sn_fit = SN_fit_tab(metaTable)

resfit = sn_fit()
print(len(metaTable), len(resfit))
# write results in file
fOut = '{}/{}'.format(metaDirOutput, metaFileOutput)
astropy.io.misc.hdf5.write_table_hdf5(
    resfit, fOut, path='meta', overwrite=True, serialize_meta=False)
