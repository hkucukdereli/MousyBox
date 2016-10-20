import os
from loadData import *
from licks import *

__all__ = ['loadData', 'findLicks', 'plotLicks', 'rasterLicks', 'histLicks']

## change the wd to dir containing the script
curpath = os.path.dirname(os.path.realpath(__file__))
os.chdir(curpath)
