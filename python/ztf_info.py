import operator
from astropy.table import Table


def get_info(data, info, selec=False):
    """"
    Function to estimate infos from data

    Parameters
    --------------
    data: astropy table
      data to process (lc, ...)
    info: astropy table
      values to estimate

    """

    res = Table()
    for row in info:

        col = row['col']
        op = eval(row['op1'])
        type_ = eval(row['type'])
        lim = type_(row['lim_col'])

        mask = op(data[col], lim)
        new_tab = data[mask]

        res[row['name']] = [len(new_tab)]

    return res
