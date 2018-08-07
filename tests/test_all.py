#!/usr/bin/env python
"""
examples:
./test_readtra.py tests/data/beam52/dir.output/transcar_output

"""
from pathlib import Path
import numpy as np
import pytest
from pytest import approx
import transcarread as tr
#
tdir = Path(__file__).parent
infn = tdir / 'data/beam52/dir.input/90kmmaxpt123.dat'


def test_readtra():
    # %% get sim parameters
    ifn = infn.parents[1] / 'dir.input/DATCAR'
    tcofn = tdir / 'data/beam52/dir.output/transcar_output'
    tReq = '2013-03-31T09:00:21'
    H = tr.readTranscarInput(ifn)
# %% load transcar output
    iono = tr.read_tra(tcofn, tReq)
# %% check
    assert H['latgeo_ini'] == approx(65.12)
    assert iono['iono'].loc[..., 'n1'][30] == approx(2.0969721e+11)
    assert iono.attrs['chi'] == approx(110.40122986)
    assert iono['pp'].loc[..., 'Ti'][53] == approx(1285.927001953125)


def test_readtranscar():
    e0 = 52.
    tReq = '2013-03-31T09:00:21'
    sim = tr.SimpleSim('bg3', tdir/f'data/beam{e0}/dir.output')
    rates = tr.calcVERtc('dir.output/emissions.dat',
                         tdir/'data', e0, tReq, sim)
# %%
    assert rates.loc[..., 'no1d'][0, 53] == approx(15638.62)
    assert rates.time.values == np.datetime64('2013-03-31T09:00:42')


def test_readmsis():
    msis = tr.readmsis(infn)
    assert msis['msis'].loc[..., 'no1d'][53] == approx(116101103616.0)


if __name__ == '__main__':
    pytest.main(['-x', __file__])
