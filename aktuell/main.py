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
import re


# gui ------------------------------------------------------------

# main window
root = tk.Tk()
root.title("Tab Widget")
root.geometry("1280x720")
root.configure(background='white')

# Create style used by default for all Frames
style = ttk.Style()
style.configure('TFrame', background='white')

# tabs
tabControl = ttk.Notebook(root)

tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)

tabControl.add(tab1, text='Aufnahmen')
tabControl.add(tab2, text='Plots')
tabControl.add(tab3, text='Liveplot')

# for the plots
matplotlib.use('TkAgg')


# variables -----------------------------------------------------

data_filename_label = tk.StringVar()
data_filename_label.set("None")

data_filename_var = "None"

loaded_data = []

currently_recording = False


# functions ------------------------------------------------------

def load_data():
    # reads data from file
    with open(data_filename_var, 'r') as file:
        details = file.read()
        x = details.split('\n')

    # adds data to list
    global loaded_data
    loaded_data = []
    for i in x:
        if i != '':
            loaded_data.append(float(i))


def check_if_recording():
    file_size = -1
    global currently_recording
    global data_filename_var

    # gets recently created file
    with open('test.json', 'r') as f:
        output_path = json.load(f)

    data_filename_var = os.path.join(os.path.dirname(__file__), output_path["outputPath"].replace("/", "\\"))

    # checks if recording has started
    while True:
        if not os.path.isfile(output_path["outputPath"]):
            continue
        else:
            print("recording...")
            tabControl.select(2)
            currently_recording = True
            break

    # checks if recording stops
    while True:
        time.sleep(0.5)
        current_file_size = os.path.getsize(output_path["outputPath"])

        if current_file_size != file_size:
            file_size = current_file_size
        else:
            print("stopped recording")
            currently_recording = False
            break

    # loads just recorded data
    load_data()

    # switches to plot tab
    tabControl.select(1)

    # changes filename to be displayed
    data_filename_var_short = re.sub(r".*\\", "", data_filename_var)
    data_filename_label.set(data_filename_var_short)


# starts c++ file
def new_recording():
    cpp_file = os.path.join(os.path.dirname(__file__), 'c++\\record.exe')
    subprocess.call([cpp_file])


# starts recording thread, then thread that checks if it records
def new_recording_thread():
    record_thread = threading.Thread(target=new_recording)
    record_thread.start()

    time.sleep(1)

    check_if_recording_thread = threading.Thread(target=check_if_recording)
    check_if_recording_thread.start()


# opens file browser, sets new data file name and loads its content
def browse_files():
    global data_filename_var
    data_filename_var = filedialog.askopenfilename(initialdir=f'{os.getcwd()}/Aufnahmen',
                                                   title="Select a File",
                                                   filetypes=(("Text files", "*.txt"),
                                                              ("all files", "*.*")))
    # if a file has been selected
    if data_filename_var != "":
        data_filename_var_short = re.sub(r".*\/", "", data_filename_var)
        data_filename_label.set(data_filename_var_short)

        load_data()


# TAB 1 ---------------------------------------------------------

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


# TAB 2 ---------------------------------------------------------

filename_plot_label = tk.Label(tab2, textvariable=data_filename_label, bg="white")

loaded_data2 = [1,2,3,4,5]
loaded_data3 = [5,4,3,2,1]


show_plot_var = IntVar(value=1)


def ticked():
    print(show_plot_var.get())

    figure_plots.clear()
    subplot = figure_plots.add_subplot(1, 1, 1)

    if show_plot_var.get() == 1:
        subplot.plot(loaded_data)
        subplot.set_xlabel("time")
    elif show_plot_var.get() == 2:
        subplot.plot(loaded_data2)
        subplot.set_xlabel("time")
    elif show_plot_var.get() == 3:
        subplot.plot(loaded_data3)
        subplot.set_xlabel("time")

    canvas_plots.draw()


# shows only time plot when plot tab is opened
def refresh_plot():
    figure_plots.clear()
    subplot = figure_plots.add_subplot(1, 1, 1)
    subplot.plot(loaded_data)
    subplot.set_xlabel("time")
    canvas_plots.draw()


# plot checkbuttons
checkbox_frame = Frame(tab2)
plot_1_checkbutton = Radiobutton(checkbox_frame, text="plot one", variable=show_plot_var, value=1,  command=ticked, bg="white")
plot_2_checkbutton = Radiobutton(checkbox_frame, text="plot two", variable=show_plot_var, value=2, command=ticked, bg="white")
plot_3_checkbutton = Radiobutton(checkbox_frame, text="plot two", variable=show_plot_var, value=3, command=ticked, bg="white")


figure_plots = Figure(dpi=100)

canvas_plots = FigureCanvasTkAgg(figure_plots, master=tab2)
canvas_plots.draw()

# toolbar for matplotlib
toolbar = NavigationToolbar2Tk(canvas_plots, tab2)
toolbar.update()

# ----------

filename_plot_label.pack()

checkbox_frame.pack()

plot_1_checkbutton.grid(row=0, column=0)
plot_2_checkbutton.grid(row=0, column=1)
plot_3_checkbutton.grid(row=0, column=2)

canvas_plots.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


# TAB 3 ---------------------------------------------------------


figure_liveplot = Figure(dpi=100)

figure_liveplot.add_subplot(111).plot(0)

canvas_liveplot = FigureCanvasTkAgg(figure_liveplot, master=tab3)
canvas_liveplot.draw()

toolbar2 = NavigationToolbar2Tk(canvas_liveplot, tab3)
toolbar2.update()


# frequently loads data file
def liveplot():
    global loaded_data
    while currently_recording:
        load_data()

        figure_liveplot.clear()
        plot = figure_liveplot.add_subplot()

        if len(loaded_data) > 10000:
            plot.set_xlim([len(loaded_data)-10000, len(loaded_data)])
        else:
            plot.set_xlim([0, 10000])

        plot.plot(loaded_data)

        canvas_liveplot.draw()

    return


# ----------

canvas_liveplot.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


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






