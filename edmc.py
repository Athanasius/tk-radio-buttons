#!/usr/bin/env python3
#

import tkinter as tk

appname = "edmclikeradiobuttons"
applongname = "EDMC-like Radio Buttons"

class AppWindow:

    def __init__(self, master):
        self.w = master

        self.w.title(applongname)

        self.prefsdialog = None

        self.menubar = tk.Menu()

        self.file_menu = tk.Menu(self.menubar, tearoff=tk.FALSE)
        self.file_menu.add_command(command=lambda: PreferencesDialog(self.w, self.postprefs))

    def onexit(self, event=None):
        self.w.destroy()

    def postprefs(self, event=None):
        pass


def main():
    root = tk.Tk(className=appname.lower())

    app = AppWindow(root)

    root.mainloop()


if __name__ == '__main__':
    main()