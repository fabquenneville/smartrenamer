#!/usr/bin/env python3

import os
import sys

from pathlib import Path

def load_arguments():
    '''Get/load command parameters 

    Args:

    Returns:
        arguments: A dictionary of lists of the options passed by the user
    '''
    arguments = {
        "option": False,
    }

    for arg in sys.argv:
        # Confirm with the user that he selected to delete found files
        if "-option:" in arg:
            arguments["option"] = True

    return arguments


def print_allwidgets(window):
    for widget in window.winfo_children():
        print(widget)


def get_content(path, directories = False, absolute = True):
    ''' get the list of the content in a filepath

    Args:
        path: the parent path to work on
        directories = False: If true only directories will be returned

    Returns:
        folderlist: Operations success
    '''
    
    if not path[-1] == os.sep:
        path += os.sep
    
    pathobj = Path(path)
    items = None

    if directories:
        items = [str(name) for name in pathobj.rglob("*")]
    else:
        items = [str(name) for name in pathobj.rglob("*") if name.is_file()]
    
    if not absolute:
        for i in range(len(items)):
            items[i] = items[i].replace(path, "." + os.sep)
    
    return items