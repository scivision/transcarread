#!/usr/bin/env python
"""
Show auroral output, optionally with simulated optical filter.

python transcar2aurora.py tests/data/
"""
from dateutil.parser import parse
import transcarread as tr
#
kinfn ='dir.output/emissions.dat'
#%% main (sanity test with hard coded values)
if __name__ == '__main__':

    from argparse import ArgumentParser
    p = ArgumentParser(description='Makes auroral emissions based on transcar sim')
    p.add_argument('path',help='root path that beam directories live in')
    p.add_argument('-e','--energy',help='energy of this beam [eV]',default=52,type=float)
    p.add_argument('-t','--treq',help='date/time  YYYY-MM-DDTHH-MM-SS',default='2013-03-31T09:00:30Z')
    p.add_argument('--filter',help='optical filter choices: bg3   none',default='bg3')
    p.add_argument('--tcopath',help='set path from which to read transcar output files',default='dir.output')
    p = p.parse_args()


    sim = tr.SimpleSim(p.filter,p.tcopath,transcarutc=p.treq)
#%% run sim
    rates, tUsed, tReqInd = tr.calcVERtc(kinfn,p.path,p.energy,parse(p.treq),sim)
