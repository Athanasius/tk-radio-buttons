#!/usr/bin/env python3
#

import tkinter as tk

appname = "edmclikeradiobuttons"
applongname = "EDMC-like Radio Buttons"

class AppWindow:

    def __init__(self, master):
        self.w = master

        self.w.title(applongname)
        self.w.rowconfigure(0, weight=1)
        self.w.columnconfigure(0, weight=1)

        self.prefsdialog = None

        frame = tk.Frame(self.w, name=appname.lower())
        frame.grid(sticky=tk.NSEW)
        frame.columnconfigure(1, weight=1)

        self.thing_label = tk.Label(frame)
        self.thing_label.grid(row=1, column=0, sticky=tk.W)
        self.thing_label['text'] = 'Thing'
        self.thing = tk.Label(frame, compound=tk.RIGHT, anchor=tk.W, name='thing')
        self.thing['text'] = 'Thingy'
        self.thing.grid(row=1, column=2, sticky=tk.EW)

        self.menubar = tk.Menu(self.w)

        self.file_menu = tk.Menu(self.menubar, tearoff=tk.FALSE, title='File')
        self.file_menu.add_command(label='Prefs', command=lambda: PreferencesDialog(self.w, self.postprefs))
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Exit', command=self.onexit)
        self.menubar.add_cascade(label='File', menu=self.file_menu)

        self.w.protocol("WM_DELETE_WINDOW", self.onexit)

        self.w.config(menu=self.menubar)

    def onexit(self, event=None):
        self.w.destroy()

    def postprefs(self, event=None):
        pass


class PreferencesDialog:

    def __init__(self, parent, callback):
        tk.Toplevel.__init__(self, parent)

        self.parent = parent
        self.callback = callback
        self.title('Settings')

        if parent.winfo_viewable():
            self.transient(parent)

        self.attributes('-toolwindow', tk.TRUE)

        self.resizable(tk.FALSE, tk.FALSE)

        # appearances_frame = nb.Frame(notebook)



def main():
    root = tk.Tk(className=appname.lower())

    app = AppWindow(root)

    root.mainloop()


if __name__ == '__main__':
    main()