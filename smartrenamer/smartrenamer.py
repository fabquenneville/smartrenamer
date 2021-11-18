#!/usr/bin/env python3

# Normal import
try:
    from smartrenamer.library.tools import load_arguments
    from smartrenamer.library.ui import build_main_window
# Allow local import for development purposes
except ModuleNotFoundError:
    from library.tools import load_arguments
    from library.ui import build_main_window

def main():
    window = build_main_window()
    window.mainloop()


if __name__ == '__main__':
    main()
