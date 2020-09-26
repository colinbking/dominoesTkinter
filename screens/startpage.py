
import tkinter as tk
from tkinter import font as tkfont # python 3
from tkinter import ttk

# Class representing our start page!
class StartPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # START MAKING YOUR LABELS, BUTTONS, ETC. FOR THE WELCOME PAGE HERE
        label = tk.Label(self, text="Hello World")
        label.pack()

        # self.close_button.pack(pady="5")
