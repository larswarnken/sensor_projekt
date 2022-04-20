import tkinter as tk
from tkinter import *
from tkinter import ttk
import os
import subprocess
import threading
from tkinter import filedialog
import json
import time

import matplotlib
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

from tkinter import messagebox

matplotlib.use('TkAgg')


# gui ------------------------------------------------------------

root = tk.Tk()
root.title("Tab Widget")
root.geometry("1280x720")

tabControl = ttk.Notebook(root)

tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)

tabControl.add(tab1, text='Aufnahmen')
tabControl.add(tab2, text='Plots')
tabControl.add(tab3, text='Liveplot')


# variables -----------------------------------------------------

data_filename = tk.StringVar()
data_filename.set("None")

data_filename_var = "None"

loaded_data = []


# functions ------------------------------------------------------

def load_data():
    with open(data_filename_var, 'r') as file:
        details = file.read()
        x = details.split('\n')

    global loaded_data
    loaded_data = []
    for i in x:
        if i != '':
            loaded_data.append(float(i))


def check_if_recording():
    file_size = -1

    with open('test.json', 'r') as f:
        data = json.load(f)

    while True:
        if not os.path.isfile(data["outputPath"]):
            continue
        else:
            print("recording...")
            tabControl.select(2)
            break

    while True:
        time.sleep(0.5)
        current_file_size = os.path.getsize(data["outputPath"])

        if current_file_size != file_size:
            file_size = current_file_size
        else:
            print("stopped recording")
            break

    global data_filename_var
    data_filename_var = os.path.join(os.path.dirname(__file__), data["outputPath"].replace("/", "\\"))
    data_filename.set(data_filename_var)

    load_data()

    tabControl.select(1)


def new_recording():
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'c++\\record.exe')
    subprocess.call([filename])


def new_recording_thread():
    record_thread = threading.Thread(target=new_recording)
    record_thread.start()

    time.sleep(1)

    check_if_recording_thread = threading.Thread(target=check_if_recording)
    check_if_recording_thread.start()





def browse_files():
    global data_filename_var
    old_data_filename = data_filename_var
    data_filename_var = filedialog.askopenfilename(initialdir=os.getcwd(),
                                                   title="Select a File",
                                                   filetypes=(("Text files", "*.txt"),
                                                              ("all files", "*.*")))
    if data_filename_var != "":
        data_filename.set(data_filename_var.replace("/", "\\"))

        load_data()


# tab 1 ---------------------------------------------------------

frame = Frame(tab1)

button_new_recording = tk.Button(frame, text="New Recording", command=new_recording_thread)
button_load_recording = tk.Button(frame, text="Load Recording", command=browse_files)

label_current_file_dings = tk.Label(frame, text="Current File: ")
label_current_file = tk.Label(frame, textvariable=data_filename)


# ----------

# grid.columnconfigure(tuple(range(60)), weight=1)
# grid.rowconfigure(tuple(range(30)), weight=1)

button_new_recording.grid(row=0, column=0, padx=30, pady=30, sticky="news")
button_load_recording.grid(row=0, column=1, padx=30, pady=30, sticky="news")
label_current_file_dings.grid(row=1, column=0, sticky="news")
label_current_file.grid(row=1, column=1, sticky="news")

frame.pack(expand=True)

# tab 2 ---------------------------------------------------------

label_2 = ttk.Label(tab2, text="bla bla")

# create a figure
figure = plt.figure(1) # , figsize=(6, 4), dpi=100

# create FigureCanvasTkAgg object
figure_canvas = FigureCanvasTkAgg(figure, tab2)

# create the toolbar
NavigationToolbar2Tk(figure_canvas, tab2)


def refresh_plot(*args):
    if tabControl.index(tabControl.select()) == 1:
        figure.clear()
        plt.plot(loaded_data)
        plt.draw()


tabControl.bind('<<NotebookTabChanged>>', refresh_plot)


# ----------

# label_2.grid(row=0, column=0, padx=30, pady=30)
# figure_canvas.get_tk_widget().grid(row=1, column=0)

label_2.pack()
figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


# tab 3 ---------------------------------------------------------

label_3 = ttk.Label(tab3, text="bla bla bla")

# # create a figure
# figure_live = plt.figure(2) # , figsize=(6, 4), dpi=100
#
# # create FigureCanvasTkAgg object
# figure_canvas_live = FigureCanvasTkAgg(figure_live, tab3)
#
# # create the toolbar
# NavigationToolbar2Tk(figure_canvas_live, tab3)



# ----------

# label_2.grid(row=0, column=0, padx=30, pady=30)
# figure_canvas.get_tk_widget().grid(row=1, column=0)

label_3.pack()
# figure_canvas_live.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


# main grid ---------------------------------------------------------

tabControl.pack(expand=1, fill='both')


def on_closing():
    # if messagebox.askokcancel("Quit", "Do you want to quit?"):
    root.destroy()
    plt.close(figure)
    # plt.close(figure_live)


root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()






