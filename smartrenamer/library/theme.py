#!/usr/bin/env python3

import tkinter as tk
import darkdetect

class Theme():
    def __init__(self):
        self.load_colors()

    def load_colors(self):
        self.colors = self.get_colors()

    @staticmethod
    def get_colors():
        colors = {
            # Background color for the widget when the widget is active.
            "activebackground":     None,
            # Foreground color for the widget when the widget is active.
            "activeforeground":     None,
            # Background color for the widget. This can also be represented as bg.
            "background":           None,
            # Foreground color for the widget when the widget is disabled.
            "disabledforeground":   None,
            # Foreground color for the widget. This can also be represented as fg.
            "foreground":           None,
            # Background color of the highlight region when the widget has focus.
            "highlightbackground":  None,
            # Foreground color of the highlight region when the widget has focus.
            "highlightcolor":       None,
            # Background color for the selected items of the widget.
            "selectbackground":     None,
            # Foreground color for the selected items of the widget.
            "selectforeground":     None,
        }
        if darkdetect.isDark():
            colors = {
                "activebackground":     None,
                "activeforeground":     None,
                "background":           "#30362F",
                "disabledforeground":   None,
                "foreground":           "#a5abaf",
                "highlightbackground":  None,
                "highlightcolor":       None,
                "selectbackground":     None,
                "selectforeground":     None,
            }
        return colors

    @staticmethod
    def set_colors(component):
        colors = Theme.get_colors()

        if colors["background"]:
            component["bg"] = colors["background"]
            component["background"] = colors["background"]

        if colors["foreground"] and hasattr(component, 'fg'):
            component["fg"] = colors["foreground"]

        if colors["foreground"] and hasattr(component, 'foreground'):
            component["foreground"] = colors["foreground"]
