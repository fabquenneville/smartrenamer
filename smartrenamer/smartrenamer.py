#!/usr/bin/env python3

# Normal import
try:
    from smartrenamer.library.tools import load_arguments, print_allwidgets
    from smartrenamer.library.mainapplication import MainApplication
# Allow local import for development purposes
except ModuleNotFoundError:
    from library.tools import load_arguments, print_allwidgets
    from library.mainapplication import MainApplication

def main():
    mainapp = MainApplication()
    mainapp.mainloop()


if __name__ == '__main__':
    main()
