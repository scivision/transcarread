from pathlib import Path
import logging
from datetime import datetime
from dateutil.parser import parse
#
from .readExcrates import ExcitationRates
from .parseTranscar import readTranscarInput
from histutils.findnearest import find_nearest
#
'''
calcVERtc is the function called by "hist-feasibility" to get Transcar modeled VER/flux

outputs:
--------
spec: Panel of excitation rates: reaction x altitude x time

We use pcolormesh instead of imshow to enable correct log-plot labeling/coloring

References include:
Zettergren, M. "Model-based optical and radar remote sensing of transport and composition in the auroral ionosphere" PhD Thesis, Boston Univ., 2009
Zettergren, M. et al "Optical estimation of auroral ion upflow: 2. A case study" JGR Vol 113 A7  2008 DOI:10.1029/2007JA012691
Zettergren, M. et al "Optical estimation of auroral ion upflow: Theory"          JGR Vol 112 A12 2007 DOI: 10.1029/2007JA012691

Tested with:
Matplotlib 1.4 (1.3.1 does NOT work for pcolormesh)

Plambda contains all the wavelengths generated for the reactions at a particular beam energy level
Plambda row: wavelength col: altitude
for each energy bin, we take Plambda through the EMCCD window and optional BG3 filter,
yielding Peigen, a ver eigenprofile p(z,E) for that particular energy
'''

def calcVERtc(infile,datadir,beamEnergy,tReq,sim):
#%% get beam directory
    beamdir = Path(datadir) / 'beam{}'.format(beamEnergy)
    logging.debug(beamEnergy)
#%% read simulation parameters
    tctime = readTranscarInput(beamdir/'dir.input'/sim.transcarconfig)
    if tctime is None:
        return None, None #leave here

    try:
      if not tctime['tstartPrecip'] < tReq < tctime['tendPrecip']:
        logging.info('precip start/end: {} / {}'.format(tctime['tstartPrecip'],tctime['tendPrecip']) )
        logging.error('your requested time {} is outside the precipitation time'.format(tReq))
        tReq = tctime['tendPrecip']
        logging.warning('falling back to using the end simulation time: {}'.format(tReq))
    except TypeError as e:
        tReq=None
        logging.error('problem with requested time : {} beam {}  {}'.format(tReq,beamEnergy,e))
#%% convert transcar output
    spec, tTC, dipangle = ExcitationRates(beamdir,infile)

    tReqInd,tUsed = picktime(tTC,tReq,beamEnergy)

    return spec,tUsed,tReqInd

def picktime(tTC,tReq,beamEnergy):
    try:
        tReqInd = find_nearest(tTC,tReq)[0]
    except TypeError as e:
        logging.error('using last time in place of requested time for beam {}  {}'.format(beamEnergy,e))
        tReqInd = -1

    tUsed = tTC[tReqInd]

    return tReqInd,tUsed

#%% for testing only
class SimpleSim():
    """
    simple input for debugging/self test
    """
    def __init__(self,filt,inpath,reacreq=None,lambminmax=None,transcarutc=None):
        self.loadver = False
        self.loadverfn = Path('precompute/01Mar2011_FA.h5')
        self.opticalfilter = filt
        self.minbeamev = 0
        self.obsalt_km=0
        self.zenang=77.5
        #self.maxbeamev = #future
        self.transcarev = Path('~/code/transcar/transcar/BT_E1E2prev.csv')

        self.excratesfn = 'emissions.dat'
        self.transcarpath = inpath
        self.transcarconfig = 'DATCAR'

        if isinstance(transcarutc,str):
            self.transcarutc = parse(transcarutc)
        else:
            self.transcarutc = transcarutc
 
        if reacreq is None:
            self.reacreq = ['metastable','atomic','n21ng','n2meinel','n22pg','n21pg']
        else:
            self.reacreq = reacreq

        if lambminmax is None:
            self.lambminmax = (1200,200)
        else:
            self.lambminmax = lambminmax

        self.reactionfn = Path('precompute/vjeinfc.h5')
        self.bg3fn = Path('precompute/BG3transmittance.h5')
        self.windowfn = Path('precompute/ixonWindowT.h5')
        self.qefn = Path('precompute/emccdQE.h5')
