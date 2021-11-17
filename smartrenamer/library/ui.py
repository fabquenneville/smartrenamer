#!/usr/bin/env python3

import tkinter.filedialog
import tkinter as tk

def build_main_window():
    window = tk.Tk()
    window.title("smartrenamer")
    w, h = window.winfo_screenwidth(), window.winfo_screenheight()
    window.geometry("%dx%d+0+0" % (w, h))
    window.grid_columnconfigure(0,weight=1)

    build_menu(window)

    dir_selector = build_directory_selector(window)
    dir_selector.grid(column=0, row=0, sticky="ew")

    # file_tree = build_directory_selector(window)
    # dir_selector.grid(column=0, row=1, sticky="ew")

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
        command=lambda: open_directory(window)
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

def build_directory_selector(window):
    frame = tk.LabelFrame(window, text="Current directory", name="directory_frame")
    # frame = tk.Frame(window, text="Current directory", highlightbackground="black", highlightthickness=1)

    # label = tk.Label(frame, text='Directory:')
    textfield = tk.Entry(frame, name="directory_entry")
    button = tk.Button(frame, text='Find directory', command=lambda: open_directory(window))

    # label.pack(side="left", fill=None, expand=False)
    textfield.pack(side="left", fill="x", expand=True)
    button.pack(side="right", fill=None, expand=False)

    textfield.focus()

    return frame



def open_directory(window):
    folder_selected = tkinter.filedialog.askdirectory()
    
    entry = window.nametowidget("directory_frame.directory_entry")
    entry.delete(0,"end")
    entry.insert(0, folder_selected)