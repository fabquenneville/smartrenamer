#!/usr/bin/env python3

import sys
import tkinter.filedialog

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


def open_directory(window):
    folder_selected = tkinter.filedialog.askdirectory()
    entry = window.nametowidget("dir_selector_frame.directory_entry")
    entry.delete(0,"end")
    entry.insert(0, folder_selected)

def print_allwidgets(window):
    for widget in window.winfo_children():
        print(widget)