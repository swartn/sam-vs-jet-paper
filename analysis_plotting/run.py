""" Call scripts to do analysis and plotting

.. moduleauthor:: Neil Swart <neil.swart@ec.gc.ca>
"""
import os
import glob
import importlib

# horrible, but works to run all the plotting scripts. Should be setup as functions
# but not enough time.

files = glob.glob('plot*.py')
for f in files:
    ff = f.replace('.py','')
    print ff
    importlib.import_module(ff)
