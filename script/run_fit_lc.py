from optparse import OptionParser
from ztf_fit import SN_fit_tab
from ztf_hdf5 import Read_LightCurve
import astropy
from ztf_util import multiproc


def fit(metaTable, params, j=0, output_q=None):

    sn_fit = SN_fit_tab(metaTable)

    resfit = sn_fit()

    if output_q is not None:
        return output_q.put({j: resfit})
    else:
        return 0


parser = OptionParser()

parser.add_option('--metaFileInput', type=str, default='Meta_info.hdf5',
                  help='meta file name to process [%default]')
parser.add_option('--metaDirInput', type=str, default='dataLC',
                  help='meta dir [%default]')
parser.add_option('--metaFileOutput', type=str, default='Meta_fit.hdf5',
                  help='meta file name for output [%default]')
parser.add_option('--metaDirOutput', type=str, default='dataLC',
                  help='meta dir for output [%default]')
parser.add_option('--nproc', type=int, default=1,
                  help='number of procs for multiprocessing [%default]')

opts, args = parser.parse_args()

metaFileInput = opts.metaFileInput
metaDirInput = opts.metaDirInput
metaFileOutput = opts.metaFileOutput
metaDirOutput = opts.metaDirOutput
nproc = opts.nproc

if __name__ == '__main__':
    meta = Read_LightCurve(file_name=metaFileInput, inputDir=metaDirInput)
    metaTable = meta.get_table(path='meta')

    params = {}
    resfit = multiproc(metaTable, params, fit, nproc)

    print(len(metaTable), len(resfit))

    # write results in file
    fOut = '{}/{}'.format(metaDirOutput, metaFileOutput)
    astropy.io.misc.hdf5.write_table_hdf5(
        resfit, fOut, path='meta', overwrite=True, serialize_meta=False)
