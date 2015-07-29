""" Call scripts to processes data and make plots. 

    Assumes data has been downloaded to data_retrieval/data

.. moduleauthor:: Neil Swart <neil.swart@ec.gc.ca>
"""
import os
import sys
import subprocess
from analysis_plotting import run_plotting
from data_processing import run_processing

def run(datapath):
    os.chdir('data_processing/') #have to change for rel paths to work!?!
    run_processing.run_processing(datapath=datapath)
    os.chdir('../')
    os.chdir('analysis_plotting/')
    run_plotting.run_plotting(datapath=datapath)
    os.chdir('../')

if __name__ == '__main__':
    run(datapath='../data_retrieval/data/')
    
