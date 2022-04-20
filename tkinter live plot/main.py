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

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

from tkinter import messagebox

import re


matplotlib.use('TkAgg')


# gui ------------------------------------------------------------

root = tk.Tk()
root.title("Tab Widget")
root.geometry("1280x720")
root.configure(background='white')


tabControl = ttk.Notebook(root)

tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)

# Initialize style
s = ttk.Style()
# Create style used by default for all Frames
s.configure('TFrame', background='white')

tabControl.add(tab1, text='Aufnahmen')
tabControl.add(tab2, text='Plots')
tabControl.add(tab3, text='Liveplot')


# variables -----------------------------------------------------

data_filename_label = tk.StringVar()
data_filename_label.set("None")

data_filename_var = "None"

loaded_data = []

currently_recording = False


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
    global currently_recording

    with open('test.json', 'r') as f:
        data = json.load(f)

    global data_filename_var
    data_filename_var = os.path.join(os.path.dirname(__file__), data["outputPath"].replace("/", "\\"))

    # checks if recording has started
    while True:
        if not os.path.isfile(data["outputPath"]):
            continue
        else:
            print("recording...")
            tabControl.select(2)
            currently_recording = True
            break

    # checks if recording stops
    while True:
        time.sleep(0.5)
        current_file_size = os.path.getsize(data["outputPath"])

        if current_file_size != file_size:
            file_size = current_file_size
        else:
            print("stopped recording")
            currently_recording = False
            break

    load_data()

    tabControl.select(1)

    data_filename_var_short = re.sub(r".*\\", "", data_filename_var)
    data_filename_label.set(data_filename_var_short)


def new_recording():
    cpp_file = os.path.join(os.path.dirname(__file__), 'c++\\record.exe')
    subprocess.call([cpp_file])


def new_recording_thread():
    record_thread = threading.Thread(target=new_recording)
    record_thread.start()

    time.sleep(1)

    check_if_recording_thread = threading.Thread(target=check_if_recording)
    check_if_recording_thread.start()


def browse_files():
    global data_filename_var
    data_filename_var = filedialog.askopenfilename(initialdir=os.getcwd(),
                                                   title="Select a File",
                                                   filetypes=(("Text files", "*.txt"),
                                                              ("all files", "*.*")))
    if data_filename_var != "":
        data_filename_var_short = re.sub(r".*\/", "", data_filename_var)
        data_filename_label.set(data_filename_var_short)

        load_data()


# tab 1 ---------------------------------------------------------

frame = Frame(tab1, bg="white")

button_new_recording = tk.Button(frame, text="New Recording", command=new_recording_thread)
button_load_recording = tk.Button(frame, text="Load Recording", command=browse_files)

label_current_file_dings = tk.Label(frame, text="Current File: ", bg="white")
label_current_file = tk.Label(frame, textvariable=data_filename_label, bg="white")


# ----------


button_new_recording.grid(row=0, column=0, padx=30, pady=30, sticky="news")
button_load_recording.grid(row=0, column=1, padx=30, pady=30, sticky="news")
label_current_file_dings.grid(row=1, column=0, sticky="news")
label_current_file.grid(row=1, column=1, sticky="news")

frame.pack(expand=True)

# tab 2 ---------------------------------------------------------

label_2 = tk.Label(tab2, textvariable=data_filename_label, bg="white")

loaded_data2 = [1,2,3,4,5,5]


show_plot_1 = IntVar(value=1)
show_plot_2 = IntVar()


def ticked():
    fig.clear()
    if show_plot_1.get() == 0 and show_plot_2.get() == 0:
        fig.clear()
    elif show_plot_1.get() == 1 and show_plot_2.get() == 1:
        fig.add_subplot(2, 1, 1).plot(loaded_data)
        fig.add_subplot(2, 1, 2).plot(loaded_data2)
    elif show_plot_1.get() == 1 and show_plot_2.get() == 0:
        fig.add_subplot(1, 1, 1).plot(loaded_data)
    elif show_plot_1.get() == 0 and show_plot_2.get() == 1:
        fig.add_subplot(1, 1, 1).plot(loaded_data2)
    canvas.draw()


def refresh_plot():
    fig.clear()
    fig.add_subplot(1, 1, 1).plot(loaded_data)
    canvas.draw()


checkbox_frame = Frame(tab2)

plot_1_checkbutton = Checkbutton(checkbox_frame, text="plot one", variable=show_plot_1, command=ticked, bg="white")
plot_2_checkbutton = Checkbutton(checkbox_frame, text="plot two", variable=show_plot_2, command=ticked, bg="white")


fig = Figure(figsize=(5, 4), dpi=100)


canvas = FigureCanvasTkAgg(fig, master=tab2)  # A tk.DrawingArea.
canvas.draw()


toolbar = NavigationToolbar2Tk(canvas, tab2)
toolbar.update()


# ----------

# label_2.grid(row=0, column=0, padx=30, pady=30)
# figure_canvas.get_tk_widget().grid(row=1, column=0)

label_2.pack()

checkbox_frame.pack()

plot_1_checkbutton.grid(row=0, column=0)
plot_2_checkbutton.grid(row=0, column=1)

canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


# tab 3 ---------------------------------------------------------


fig2 = Figure(figsize=(5, 4), dpi=100)

fig2.add_subplot(111).plot(0)


canvas2 = FigureCanvasTkAgg(fig2, master=tab3)  # A tk.DrawingArea.
canvas2.draw()


toolbar2 = NavigationToolbar2Tk(canvas2, tab3)
toolbar2.update()


def liveplot():
    while currently_recording:
        load_data()

        fig2.clear()
        plot = fig2.add_subplot(111)

        global loaded_data

        if len(loaded_data) > 10000:
            plot.set_xlim([len(loaded_data)-10000, len(loaded_data)])
        else:
            plot.set_xlim([0, 10000])

        plot.plot(loaded_data)

        canvas2.draw()

    return


# ----------

canvas2.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


# main grid ---------------------------------------------------------

tabControl.pack(expand=1, fill='both')

# -------------------------------------------------------------------


def tab_switched(*args):
    if tabControl.index(tabControl.select()) == 0:
        return
    elif tabControl.index(tabControl.select()) == 1:
        refresh_plot()
    elif tabControl.index(tabControl.select()) == 2:
        liveplot()


def on_closing():
    # if messagebox.askokcancel("Quit", "Do you want to quit?"):
    root.quit()
    root.destroy()
    # plt.close(figure)
    # plt.close(figure_live)


tabControl.bind('<<NotebookTabChanged>>', tab_switched)

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()






