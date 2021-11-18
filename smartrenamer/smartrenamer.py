#!/usr/bin/env python3

# Normal import
try:
    from smartrenamer.library.tools import load_arguments, print_allwidgets
    from smartrenamer.library.mainwindow import MainWindow
# Allow local import for development purposes
except ModuleNotFoundError:
    from library.tools import load_arguments, print_allwidgets
    from library.mainwindow import MainWindow

def main():
    window = MainWindow()
    window.mainloop()


if __name__ == '__main__':
    main()
