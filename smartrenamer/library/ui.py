#!/usr/bin/env python3

import tkinter.filedialog
import tkinter as tk

def build_main_window():
    window = tk.Tk()
    window.title("smartrenamer")
    w, h = window.winfo_screenwidth(), window.winfo_screenheight()
    window.geometry("%dx%d+0+0" % (w, h))
    # window.grid_columnconfigure(0,weight=1)
    # window.grid_rowconfigure(0,weight=1)
    # window.grid_rowconfigure(1,weight=1)

    build_menu(window)
    dir_selector_frame = build_directory_selector(window)
    comparator_frame = build_comparator(window)

    # dir_selector_frame.grid(column=0, row=0, sticky="new")
    # comparator_frame.grid(column=0, row=1, sticky="nsew")

    dir_selector_frame.pack(fill="x")
    comparator_frame.pack(expand=True, fill="both")

    print_allwidgets(window)
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
    frame = tk.LabelFrame(window, text="Current directory", name="dir_selector_frame", padx=10, pady=10)
    
    textfield = tk.Entry(frame, name="directory_entry")
    textfield.focus()
    button = tk.Button(frame, text='Find directory', command=lambda: open_directory(window))
    
    textfield.pack(side="left", fill="x", expand=True)
    button.pack(side="right", fill=None, expand=False)

    return frame


def build_comparator(window):
    main_frame = tk.Frame(window, name="comparator_frame", pady=10)
    # mainframe.columnconfigure(0, weight=1)
    # mainframe.columnconfigure(1, weight=1)
    # mainframe.rowconfigure(0, weight=1)

    before_frame = tk.LabelFrame(main_frame, text="Before", name="before_frame", pady=10)
    after_frame = tk.LabelFrame(main_frame, text="After", name="after_frame", pady=10)
    scrollbar = tk.Scrollbar(main_frame)

    # beforeframe.grid(column=0, row=0, sticky="w")
    # afterframe.grid(column=1, row=0, sticky="e")

    # beforeframe.grid(column=0, row=0)
    # afterframe.grid(column=1, row=0)

    before_frame.pack(side="left", expand=True, fill="both")
    after_frame.pack(side="left", expand=True, fill="both")
    scrollbar.pack(side="right", fill="y")

    # beforeframe.pack(side="left", expand=True)
    # afterframe.pack(side="right", expand=True)
    
    before_list = tk.Listbox(before_frame, yscrollcommand=scrollbar.set)
    after_list = tk.Listbox(after_frame, yscrollcommand=scrollbar.set)
    # for line in range(100):
    #     before_list.insert(tk.END, "This is line number " + str(line))
    #     after_list.insert(tk.END, "This is line number " + str(line))

    before_list.pack(side="left", fill="both", expand=True)
    after_list.pack(side="left", fill="both", expand=True)

    scrollbar.config(command=lambda *args: (before_list.yview(*args), after_list.yview(*args)))

    return main_frame


def open_directory(window):
    folder_selected = tkinter.filedialog.askdirectory()
    
    entry = window.nametowidget("dir_selector_frame.directory_entry")
    entry.delete(0,"end")
    entry.insert(0, folder_selected)


def print_allwidgets(window):
    for widget in window.winfo_children():
        print(widget)