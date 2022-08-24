import tkinter as tk
from tkinter import ttk
import matplotlib
import graph
import recording

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)


class MainApplication(tk.Frame):
    current_path = 'D:/Benutzer/Lars/Dokumente/GitHub/sensor_projekt/sensor neu/Aufnahmen/data_10.txt'

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        parent.title("title")
        parent.geometry('854x480')

        # styles
        style = ttk.Style(parent)
        current_theme = style.theme_use()
        style.theme_use('xpnative')
        # style.configure('TFrame', background='green')
        style.configure('left.TFrame', background='#F0F0F0')  # #F0F0F0
        # style.configure('right.TFrame', background='white')

        matplotlib.use('TkAgg')

        # tab control
        tab_control = ttk.Notebook(parent)
        tab_1 = ttk.Frame(tab_control)
        tab_2 = ttk.Frame(tab_control)
        tab_control.add(tab_1, text='Aufnahmen')
        tab_control.add(tab_2, text='Klassifizierung')
        tab_control.pack(expand=True, fill="both")

        # -----------------------------------

        # left frame
        frame_left = ttk.Frame(tab_1, padding=40, style='left.TFrame')
        frame_left.pack(anchor='w', fill='y', expand=False, side='left')

        # buttons: neue aufnahme, aufnahme laden
        button_1 = ttk.Button(frame_left, text="Neue Aufnahme", width=25,
                              command=lambda: recording.new_recording_thread())
        button_1.pack(pady=10)
        button_2 = ttk.Button(frame_left, text="Aufnahme laden", width=25,
                              )
        button_2.pack(pady=10)

        label_current_file = ttk.Label(frame_left, text='Aktuell geladen: -')
        label_current_file.pack()

        # info part label
        label_info_1 = ttk.Label(frame_left, text="Informationen")
        label_info_1.pack(pady=10)

        # tree widget for information
        tree_information = ttk.Treeview(frame_left, show='headings', height=8)
        tree_information['columns'] = ('feature', 'value')

        tree_information.column("# 1", anchor='w', width=80)
        tree_information.heading("# 1", text="Merkmal", anchor='w')

        tree_information.column("# 2", anchor='w', width=80)
        tree_information.heading("# 2", text="Wert", anchor='w')

        tree_information.insert(parent='', index='end', iid='i1', values=('info 1', '0'))
        tree_information.insert(parent='', index='end', iid='i2', values=('info 2', '0'))
        tree_information.insert(parent='', index='end', iid='i3', values=('info 3', '0'))
        tree_information.insert(parent='', index='end', iid='i4', values=('info 4', '0'))
        tree_information.insert(parent='', index='end', iid='i5', values=('info 5', '0'))
        tree_information.insert(parent='', index='end', iid='i6', values=('info 6', '0'))
        tree_information.insert(parent='', index='end', iid='i7', values=('info 7', '0'))
        tree_information.insert(parent='', index='end', iid='i8', values=('info 8', '0'))

        tree_information.pack()

        # to update tree information
        tree_information.item('i3', values=('info 3', '2'))

        # -----------------------------------

        frame_right = ttk.Frame(tab_1)
        frame_right.pack(anchor='n', fill='both', expand=True, side='left')

        # radio buttons for the plot
        frame_radiobuttons = ttk.Frame(frame_right)
        frame_radiobuttons.pack()

        selected = tk.StringVar(None, 'timeplot')
        radiobutton_1 = ttk.Radiobutton(frame_radiobuttons, text='time plot', value='timeplot', variable=selected,
                                        command=lambda: plot_changed(selected))
        radiobutton_2 = ttk.Radiobutton(frame_radiobuttons, text='fft plot', value='fftplot', variable=selected,
                                        command=lambda: plot_changed(selected))
        radiobutton_3 = ttk.Radiobutton(frame_radiobuttons, text='spectrogram', value='spectrogram', variable=selected,
                                        command=lambda: plot_changed(selected))

        radiobutton_1.grid(column=0, row=0)
        radiobutton_2.grid(column=1, row=0)
        radiobutton_3.grid(column=2, row=0)

        # plot frame
        figure_plots = Figure(dpi=100)
        figure_plots.set_facecolor('#F0F0F0')
        canvas_plots = FigureCanvasTkAgg(figure_plots, master=frame_right)
        canvas_plots.draw()

        # toolbar for matplotlib
        toolbar = NavigationToolbar2Tk(canvas_plots, frame_right)
        toolbar.update()

        canvas_plots.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # time plot as default plot
        graph.plot_time(figure_plots, canvas_plots)

        def plot_changed(value_p):
            if value_p.get() == 'timeplot':
                graph.plot_time(figure_plots, canvas_plots)
            elif value_p.get() == 'fftplot':
                graph.plot_fft(figure_plots, canvas_plots)
            elif value_p.get() == 'spectrogram':
                graph.plot_spectrogram(figure_plots, canvas_plots)
            else:
                print('radio button value error')

        def on_closing():
            exit()

        parent.protocol("WM_DELETE_WINDOW", on_closing)
        parent.mainloop()
