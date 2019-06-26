# -*- coding: utf-8 -*-
# Command Line Interface
# http://python-packaging.readthedocs.io/en/latest/command-line-scripts.html

from src import listids as pmidoi_listids

def listids():
    return pmidoi_listids.main()


def about():
    return '''
Utility to extract pmid - doi mapping for a given journal using EuropePMC.

Available commands:

    about: this message.
    listids: extracting the pmid-doi as tab-delimited text file.

Usage:

    listids "Your Journal Name" save_to_file.txt
'''