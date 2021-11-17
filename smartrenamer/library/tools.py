#!/usr/bin/env python3

import sys

import tkinter.filedialog
import tkinter as tk

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

def open_directory():
    folder_selected = tkinter.filedialog.askdirectory()
    print(folder_selected)
