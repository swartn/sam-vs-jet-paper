Analysis and plotting
=====================

The scripts here do the final analysis and plotting. 
[`run_plotting.py`](run_plotting.py) automates running of all the individual scripts.

The prefix `plot_` means that the script produces a plot(s) used in publication, and 
`discover_` means that the script is used to do some basic exploration of the data. 
All modules have docstrings that explain their basic function.   

The plotting will fail unless all of the expected, processed data is available
in [../../data_retrieval/data/](../data_retrieval/data/). You must first
[download](../data_retrieval/README.md) and [process](../data_processing/README.md)
the data before attempting the plotting.
