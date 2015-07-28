""" Call scripts to do plotting (with some minor analysis embedded).

    All output pdfs are saved at ../plots/

.. moduleauthor:: Neil Swart <neil.swart@ec.gc.ca>
"""
import os
import glob
import importlib

import plot_timeseries
import plot_seas_trends_1951_2011
import plot_theoretical_model
import plot_psl_trend_maps_hadslp2r_vs_20cr_cmip5_1951_2004
import plot_uas_trend_maps_cmip5_20CR_1951_2011
import plot_psl_and_u10m_trend_uncertainty_maps_20CR
import plot_rean_vs_marshall_slp
import plot_rean_vs_marshall_slp_trends
import plot_psl_trend_maps_hadslp2r_vs_reanalyses_1979_2004
import plot_uas_trend_maps_ccmp_vs_reanalyses_1988_2011
import plot_zonmean_trends
import plot_seas_trends_1979_2009

def run_plotting(datapath):
    """ Auto-run the plotting scripts to produce the 14 PDF figures from the paper.
        
        datapath is the location of the processed data.
    """

    # Figure 1: SAM and jet properties time-series.
    print 'plot_timeseries \n' 
    plot_timeseries.plot_timeseries(datapath=datapath)

    # Figures 2, 4 and 5: Trends in SAM indices and jet properties over 1951-2011.
    print 'plot_seas_trends_1951_2011 \n'
    plot_seas_trends_1951_2011.plot_seas_trends_1951_2011(datapath=datapath)
    
    #Figure 3: simple geostrophic model
    print 'plot_theoretical_model \n'
    plot_theoretical_model.plot_theoretical_model()
    
    # Figure 6: SLP trend maps 1951-2004
    print 'plot_psl_trend_maps_hadslp2r_vs_20cr_cmip5_1951_2004 \n'
    plot_psl_trend_maps_hadslp2r_vs_20cr_cmip5_1951_2004.plot_trend_maps(datapath=datapath)
    
    # Figure 7: u10m trend maps 1951-2011
    print 'plot_uas_trend_maps_cmip5_20CR_1951_2011 \n'
    plot_uas_trend_maps_cmip5_20CR_1951_2011.plot_trend_maps(datapath=datapath)
    
    # Figure 8: Uncertainty in 20CR slp and u10m trends.
    print 'plot_psl_and_u10m_trend_uncertainty_maps_20CR'
    plot_psl_and_u10m_trend_uncertainty_maps_20CR.plot_trend_maps(datapath=datapath)
    
    # Figure 9: Marshall SAM index timeseries
    print 'plot_rean_vs_marshall_slp \n'
    plot_rean_vs_marshall_slp.plot_rean_vs_marshall_slp(datapath=datapath)
    
    # Figure 10: Marshall SAM trends
    print 'plot_rean_vs_marshall_slp_trends \n'
    plot_rean_vs_marshall_slp_trends.plot_rean_vs_marshall_slp_trends(datapath=datapath)
    
    # Figure 11: SLP trends over 1979-2004 (HadSLP2r vs 6 Reanalyses and CMIP5)
    print 'plot_psl_trend_maps_hadslp2r_vs_reanalyses_1979_2004 \n'
    plot_psl_trend_maps_hadslp2r_vs_reanalyses_1979_2004.plot_trend_maps(datapath=datapath)
    
    # Figure 12: u10m trends over 1988-2011 (CCMP vs 6 Reanalyses and CMIP5)
    print 'plot_uas_trend_maps_ccmp_vs_reanalyses_1988_2011 \n'
    plot_uas_trend_maps_ccmp_vs_reanalyses_1988_2011.plot_trend_maps(datapath=datapath)

    #Figure 13: Zonal mean slp, u10m and tauu trends
    print 'plot_zonmean_trends \n'
    plot_zonmean_trends.plot_zonmean_trends(datapath=datapath)
    
    # Figure 14: Trends in SAM indices and jet properties over 1979-2009.
    print 'plot_seas_trends_1979_2009 \n'
    plot_seas_trends_1979_2009.plot_seas_trends_1979_2009(datapath=datapath)
    
if __name__ == '__main__':
    run_plotting(datapath='../data_retrieval/data/')    
