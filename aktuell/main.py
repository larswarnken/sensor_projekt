import detect
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
import numpy as np
from scipy import signal
from scipy.fft import fftfreq
from scipy.fft import fft, ifft, fft2, ifft2
import pywt
import matplotlib.pyplot as plt

import tensorflow as tf
from os import walk
import datetime

import liveplot_file


# gui ------------------------------------------------------------

# main window
root = tk.Tk()
root.title("Vibroakustische Signale")
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

ai_model_label = tk.StringVar()
ai_model_label.set("None")

data_filename_var = "None"

loaded_data = []
loaded_sample_rate = 0
loaded_record_time = 0

currently_recording = False

show_plot_var = IntVar(value=1)

loaded_model = None


# functions ------------------------------------------------------

def load_data():
    global loaded_sample_rate
    global loaded_record_time
    global loaded_data
    # reads data from file
    with open(data_filename_var, 'r') as file:
        details = file.read()
        x = details.split('\n')
    try:
        # saves info from first line
        loaded_sample_rate = int(x[0].split(", ")[0])
        loaded_record_time = int(x[0].split(", ")[1])
        # delete first line which is samlpe rate and time
        x.pop(0)
        # adds data to list
        global loaded_data
        loaded_data = []
        for i in x:
            if i != '':
                loaded_data.append(float(i))
    except:
        print("idk")


def check_if_recording():
    print('yooooooooooo')
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
            # tabControl.select(2)
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

    print('boop')

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

    time.sleep(0.5)

    check_if_recording_thread = threading.Thread(target=check_if_recording)
    check_if_recording_thread.start()

    time.sleep(0.1)

    record_thread2 = threading.Thread(target=liveplot_file.main())
    record_thread2.start()



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


#
def load_ai_model():
    global loaded_model
    model_name = 'efficientNetB0_2'
    loaded_model = tf.keras.models.load_model(f'ai/{model_name}')
    loaded_model = tf.keras.models.load_model(f'ai/{model_name}')
    print('model loaded')
    ai_model_label.set(model_name)





# TAB 1 ---------------------------------------------------------

frame = Frame(tab1, bg="white")

button_new_recording = tk.Button(frame, text="New Recording", command=new_recording_thread)
button_load_recording = tk.Button(frame, text="Load Recording", command=browse_files)
button_load_ai_model = tk.Button(frame, text="Load AI Model", command=load_ai_model)

label_current_file_dings = tk.Label(frame, text="Current File: ", bg="white")
label_current_file = tk.Label(frame, textvariable=data_filename_label, bg="white")
label_current_ai_model = tk.Label(frame, textvariable=ai_model_label, bg="white")


# ----------

button_new_recording.grid(row=0, column=0, padx=30, pady=30, sticky="news")
button_load_recording.grid(row=0, column=1, padx=30, pady=30, sticky="news")
button_load_ai_model.grid(row=0, column=2, padx=30, pady=30, sticky="news")

label_current_file_dings.grid(row=1, column=0, sticky="news")
label_current_file.grid(row=1, column=1, sticky="news")
label_current_ai_model.grid(row=1, column=2, sticky="news")


frame.pack(expand=True)

# TAB 2 ---------------------------------------------------------

filename_plot_label = tk.Label(tab2, textvariable=data_filename_label, bg="white")

loaded_data2 = [1, 2, 3, 4, 5]
loaded_data3 = [5, 4, 3, 2, 1]

bigframe = Frame(tab2, bg='white')

plot_frame = Frame(bigframe)
data_frame = Frame(bigframe, width=1000)

label_test = tk.Label(data_frame, text="Recording Time: ")
label_test_value = tk.Label(data_frame, text='-')
label_test2 = tk.Label(data_frame, text="Sample Rate: ")
label_test_value2 = tk.Label(data_frame, text='-')
label_test3 = tk.Label(data_frame, text="max Amplitude: ")
label_test_value3 = tk.Label(data_frame, text='-')
label_test4 = tk.Label(data_frame, text="max Amplitude Time: ")
label_test_value4 = tk.Label(data_frame, text='-')
label_test5 = tk.Label(data_frame, text="RMS: ")
label_test_value5 = tk.Label(data_frame, text='-')
label_test6 = tk.Label(data_frame, text="Signalenergie: ")
label_test_value6 = tk.Label(data_frame, text='-')
label_test7 = tk.Label(data_frame, text="max Amplitude FFT: ")
label_test_value7 = tk.Label(data_frame, text='-')
label_test8 = tk.Label(data_frame, text="max Amplitude Frequenz: ")
label_test_value8 = tk.Label(data_frame, text='-')




def refresh_facts():
    label_test_value.configure(text=f'{loaded_record_time} ms')
    label_test_value2.configure(text=f'{loaded_sample_rate}')

    time = []
    max_data = max(loaded_data)
    min_data = min(loaded_data)

    # Construct a time signal
    fs = loaded_sample_rate  # Sampling freq
    tstep = 1 / fs  # sample time interval

    for x in range(len(loaded_data)):
        time.append(x * tstep)

    # merkmale Zeitbereich 1. max. Amplitude
    max_amplitude = (max(abs(i) for i in loaded_data))
    if abs(max_data) > abs(min_data):
        m_t_idx = loaded_data.index(max_data)
    else:
        m_t_idx = loaded_data.index(min_data)

    label_test_value3.configure(text=f'{max_amplitude}')
    label_test_value4.configure(text=f'{time[m_t_idx]}')

    average = sum(loaded_data) / len(loaded_data)

    rms = np.sqrt(average ** 2)

    label_test_value5.configure(text=f'{rms}')

    # merkmale Zeitbereich 3. Signalenergie
    sig_energie = sum(abs(i) for i in loaded_data)
    label_test_value6.configure(text=f'{sig_energie}')

    label_test_value7.configure(text='-')
    label_test_value8.configure(text='-')


def plot_time():
    figure_plots.clear()
    subplot = figure_plots.add_subplot(1, 1, 1)
    subplot.plot(loaded_data)
    subplot.set_xlabel("Time")
    subplot.set_ylabel("Amplitude")
    canvas_plots.draw()


def plot_fft():
    if len(loaded_data) != 0:
        time = []

        # Construct a time signal
        fs = loaded_sample_rate  # Sampling freq
        tstep = 1 / fs  # sample time interval

        for x in range(len(loaded_data)):
            time.append(x * tstep)

        time_interval = len(time) * tstep

        # perform fft
        t = time_interval  # entire time
        n = len(loaded_data)
        t = np.linspace(0, t, n)
        dt = np.diff(t)[0]

        f = fftfreq(len(t), np.diff(t)[0])
        # fftfreq: Calculate the frequencies corresponding to
        # the FFT bins in the result returned by fft.
        y_fft = fft(loaded_data)

        figure_plots.clear()
        subplot = figure_plots.add_subplot(1, 1, 1)
        subplot.plot(f[:n // 2], np.abs(y_fft[:n // 2]))
        subplot.set_xlim(0, fs / 2)
        subplot.set_xlabel("Frequency (Hz)")
        subplot.set_ylabel("Amplitude")
        canvas_plots.draw()

        # zuerst die idx von max. Amplitude in y_FFT zu finden
        m_fft_idx = 0
        max_amplitude = 0
        for currtFFT in y_fft:
            if np.abs(currtFFT) > max_amplitude:
                m_fft_idx = np.where(y_fft == currtFFT)[0][0]
                max_amplitude = np.abs(currtFFT)

        label_test_value7.configure(text=f'{max_amplitude}')
        label_test_value8.configure(text=f'{f[:n // 2][m_fft_idx]}')
    else:
        figure_plots.clear()
        subplot = figure_plots.add_subplot(1, 1, 1)
        subplot.set_xlabel("Frequency (Hz)")
        subplot.set_ylabel("Amplitude")
        canvas_plots.draw()


def transform_to_spectrogram():
    N = int(loaded_sample_rate / 150.0)
    f = fftfreq(N, 1.0 / loaded_sample_rate)
    t = np.linspace(0, 0.1, N)
    mask = (f > 0) * (f < loaded_sample_rate / 2)

    subdata = loaded_data[:N]
    F = fft(subdata)

    n_max = int(len(loaded_data) / N)
    f_values = np.sum(mask)
    spectorgram_data = np.zeros((n_max, f_values))

    window = signal.windows.blackman(len(subdata))

    for n in range(0, n_max):
        subdata = loaded_data[(N * n):(N * (n + 1))]
        F = fft(subdata * window)
        spectorgram_data[n, :] = np.log(abs(F[mask]))

    spectorgram_data_T = spectorgram_data.T

    return spectorgram_data_T


def save_spectrogram():
    spectorgram_data_T = transform_to_spectrogram()

    figx, axes = plt.subplots(1, 1, figsize=(8, 6))
    p = axes.imshow(spectorgram_data_T, origin='lower',
                    extent=(0, len(loaded_data) / loaded_sample_rate, 0, loaded_sample_rate / 2),
                    aspect='auto',
                    cmap='RdBu_r')
    # cb = figx.colorbar(p, ax=axes)
    # cb.set_label("$\\log|F|$", fontsize=16)
    axes.set_xlabel("time (s)", fontsize=14)
    axes.set_ylabel("Frequency (Hz)", fontsize=14)
    figx.tight_layout()

    folder = "ai/input"

    # delete all files in ai input folder
    for f in os.listdir(folder):
        os.remove(os.path.join(folder, f))

    filename = data_filename_var.split("/")[-1]
    if "\\" in filename:
        filename = filename.split("\\")[-1]
    filename = filename.replace(".txt", "")
    figx.savefig(f"{folder}/{filename}.png")

    # plt.close(figx)


def plot_spectogram():
    if len(loaded_data) != 0:

        spectorgram_data_T = transform_to_spectrogram()
        # Transposed matrix

        # fig, axes = plt.subplots(1, 1, figsize=(8, 6))
        # p = axes.imshow(spectorgram_data_T, origin='lower',
        #                 extent=(0, len(loaded_data) / Fs, 0, Fs / 2),
        #                 aspect='auto',
        #                 cmap=matplotlib.cm.RdBu_r)
        # cb = fig.colorbar(p, ax=axes)
        # cb.set_label("$\log|F|$", fontsize=16)
        #
        # fig.tight_layout()
        #
        # plt.show()

        figure_plots.clear()
        subplot_one = figure_plots.add_subplot(1, 1, 1)
        # subplot_two = figure_plots.add_subplot(1, 2, 2)

        subplot_one.imshow(spectorgram_data_T, origin='lower',
                           extent=(0, len(loaded_data) / loaded_sample_rate, 0, loaded_sample_rate / 2),
                           aspect='auto',
                           cmap=matplotlib.cm.RdBu_r)

        subplot_one.set_xlabel("Time (s)")
        subplot_one.set_ylabel("Frequency (Hz)")

        # figure_plots.colorbar(subplot_one, ax=subplot_two)

        canvas_plots.draw()

    else:
        figure_plots.clear()
        subplot_one = figure_plots.add_subplot(1, 1, 1)
        subplot_one.set_xlabel("Time (s)")
        subplot_one.set_ylabel("Frequency (Hz)")
        canvas_plots.draw()

        # figure_plots.clear()
        # subplot = figure_plots.add_subplot(1, 1, 1)
        #
        # subplot.set_xlabel("Frequency (Hz)")
        # subplot.set_ylabel("Amplitude")
        # canvas_plots.draw()


def ticked():
    if show_plot_var.get() == 1:
        plot_time()
    elif show_plot_var.get() == 2:
        plot_fft()
    elif show_plot_var.get() == 3:
        plot_spectogram()


def radio_default():
    show_plot_var.set(1)





# plot checkbuttons
checkbox_frame = Frame(tab2)
plot_1_checkbutton = Radiobutton(checkbox_frame, text="Time Plot", variable=show_plot_var, value=1, command=ticked,
                                 bg="white")
plot_2_checkbutton = Radiobutton(checkbox_frame, text="FFT Plot", variable=show_plot_var, value=2, command=ticked,
                                 bg="white")
plot_3_checkbutton = Radiobutton(checkbox_frame, text="Spectrogram", variable=show_plot_var, value=3, command=ticked,
                                 bg="white")

figure_plots = Figure(dpi=100)

canvas_plots = FigureCanvasTkAgg(figure_plots, master=plot_frame)
canvas_plots.draw()

# toolbar for matplotlib
toolbar = NavigationToolbar2Tk(canvas_plots, tab2)
toolbar.update()

# ----------

filename_plot_label.pack()

checkbox_frame.pack()

bigframe.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

bigframe.columnconfigure(0, weight=1)
bigframe.rowconfigure(0, weight=1)

plot_frame.grid(row=0, column=0, sticky='news')
data_frame.grid(row=0, column=1)

plot_1_checkbutton.grid(row=0, column=0)
plot_2_checkbutton.grid(row=0, column=1)
plot_3_checkbutton.grid(row=0, column=2)

label_test.grid(row=0, column=0)
label_test_value.grid(row=0, column=1)
label_test2.grid(row=1, column=0)
label_test_value2.grid(row=1, column=1)
label_test3.grid(row=2, column=0)
label_test_value3.grid(row=2, column=1)
label_test4.grid(row=3, column=0)
label_test_value4.grid(row=3, column=1)
label_test5.grid(row=4, column=0)
label_test_value5.grid(row=4, column=1)
label_test6.grid(row=5, column=0)
label_test_value6.grid(row=5, column=1)
label_test7.grid(row=6, column=0)
label_test_value7.grid(row=6, column=1)
label_test8.grid(row=7, column=0)
label_test_value8.grid(row=7, column=1)


canvas_plots.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# TAB 3 ---------------------------------------------------------


figure_liveplot = Figure(dpi=100)

figure_liveplot.add_subplot(111).plot(0)

canvas_liveplot = FigureCanvasTkAgg(figure_liveplot, master=tab3)
canvas_liveplot.draw()

toolbar2 = NavigationToolbar2Tk(canvas_liveplot, tab3)
toolbar2.update()


# def last_n_lines(fname, n):
#     assert n >= 0
#     pos = n + 1
#     lines = []
#     with open(fname) as f:
#         while len(lines) <= n:
#             try:
#                 f.seek(-pos, 2)
#             except IOError:
#                 f.seek(0)
#                 break
#             finally:
#                 lines = list(f)
#             pos *= 2
#     return lines[-n:]
#
#
# # frequently loads data file
# def liveplot():
#
#     last_n_lines("Aufnahmen/data.txt", 2)
#
#     global loaded_data
#     while currently_recording:
#         load_data()
#
#         figure_liveplot.clear()
#         plot = figure_liveplot.add_subplot()
#
#         if len(loaded_data) > 10000:
#             plot.set_xlim([0, len(loaded_data)])
#         else:
#             plot.set_xlim([0, 10000])
#
#         plot.plot(loaded_data)
#
#         canvas_liveplot.draw()
#
#     return


def cut_data():
    global loaded_data
    global loaded_sample_rate
    new_data = detect.find_dings(loaded_data, loaded_sample_rate)
    loaded_data = new_data

    plot_time()

    refresh_facts()


def use_ai():
    save_spectrogram()
    CATEGORIES = ['gummi', 'metall', 'plastik', 'stift']

    image_name = next(walk('ai/input'), (None, None, []))[2][0]  # [] if no file
    image_path = f'ai/input/{image_name}'

    image = tf.keras.preprocessing.image.load_img(
        image_path, target_size=(450, 300)
    )
    input_arr = tf.keras.preprocessing.image.img_to_array(image)
    input_arr = np.array([input_arr])

    prediction = loaded_model.predict([input_arr])

    print(prediction)
    print(np.argmax(prediction))
    print(CATEGORIES[np.argmax(prediction)])



# ----------

canvas_liveplot.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# main grid ---------------------------------------------------------

tabControl.pack(expand=1, fill='both')


# -------------------------------------------------------------------


button_detect_hit = tk.Button(data_frame, text="Detect Hit",
                              command=cut_data)
button_detect_hit.grid(row=8, column=0)


button_predict = tk.Button(data_frame, text="Classify Hit", command=use_ai)
button_predict.grid(row=9, column=0)

# ---------------------------------------------------







def tab_switched(*args):
    if tabControl.index(tabControl.select()) == 0:
        return
    elif tabControl.index(tabControl.select()) == 1:
        radio_default()

        plot_time()

        if len(loaded_data) != 0:
            refresh_facts()

    # elif tabControl.index(tabControl.select()) == 2:
    #     liveplot()


def on_closing():
    # if messagebox.askokcancel("Quit", "Do you want to quit?"):
    root.quit()
    root.destroy()
    # plt.close(figure)
    # plt.close(figure_live)


tabControl.bind('<<NotebookTabChanged>>', tab_switched)

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
