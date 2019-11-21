import tkinter as tk
from tkinter import ttk



class CollapsiblePane(ttk.Frame):

    def __init__(self, parent, label, items):
        tk.Frame.__init__(self, parent)
        header = tk.Frame(self)
        self.sub_frame = tk.Frame(self, relief="sunken",
                                  width=400, height=22, borderwidth=1)
        header.pack(side="top", fill="x")
        self.sub_frame.pack(side="top", fill="both", expand=True)

        self.var = tk.IntVar(value=0)
        self.label = tk.Label(header, text=label)
        self.toggle_btn = ttk.Checkbutton(header, width=2, text="+",
                                          variable=self.var, style='Toolbutton',
                                          command=self.toggle)
        self.entry = tk.Entry(header, width=11)

        self.label.pack(side="left")
        self.toggle_btn.pack(side="left")
        self.entry.pack(side="right", pady=2, anchor="e")
        self.sub_frame.pack(side="top", fill="both", expand=True)

        for item in items:
            tk.Label(self.sub_frame, text=item).pack(side="top")

        # this sets the initial state
        self.toggle(False)

    def toggle(self, show=None):
        show = self.var.get() if show is None else show
        if show:
            self.sub_frame.pack(side="top", fill="x", expand=True)
            self.toggle_btn.configure(text='-')
        else:
            self.sub_frame.forget()
            self.toggle_btn.configure(text='+')
