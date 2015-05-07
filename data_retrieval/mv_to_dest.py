""" Moves a file or list of files to destination

.. moduleauthor:: Neil Swart <neil.swart@ec.gc.ca>

"""
import shutil
import os

def mv_to_dest(destination, *files):
    """
    Move files to destination.

    destination is a valid path.
    """
    if destination != '.':
        for f in files:
            df = os.path.join(destination, f)
            shutil.move(f, df)