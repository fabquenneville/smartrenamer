#!/usr/bin/env python3

import tkinter as tk

from .tools import open_directory

def build_main_window():
    window = tk.Tk()
    window.title("smartrenamer")
    w, h = window.winfo_screenwidth(), window.winfo_screenheight()
    window.geometry("%dx%d+0+0" % (w, h))
    build_menu(window)
    return window

def build_menu(window):
    menubar = tk.Menu(window)
    window.config(menu=menubar)

    file_menu = tk.Menu(menubar, tearoff=False)
    file_menu.add_command(
        label='New'
    )
    file_menu.add_command(
        label='Open directory',
        command=open_directory
    )
    file_menu.add_command(label='Close')
    file_menu.add_separator()
    file_menu.add_command(
        label='Exit',
        command=window.destroy,
    )
    menubar.add_cascade(
        label="File",
        menu=file_menu,
        underline=0
    )

    help_menu = tk.Menu(
        menubar,
        tearoff=0
    )
    help_menu.add_command(label='Welcome')
    help_menu.add_command(label='About...')
    menubar.add_cascade(
        label="Help",
        menu=help_menu
    )