import tkinter as tk
from tkinter import ttk
import matplotlib
import graph

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)


def create_gui():

    root = tk.Tk()
    root.title("title")
    root.geometry('854x480')

    style = ttk.Style(root)
    current_theme = style.theme_use()
    style.theme_use('xpnative')
    # style.configure('TFrame', background='white')
    style.configure('left.TFrame', background='#F0F0F0')
    # style.configure('right.TFrame', background='white')

    matplotlib.use('TkAgg')

    tab_control = ttk.Notebook(root)
    tab_1 = ttk.Frame(tab_control)
    tab_2 = ttk.Frame(tab_control)
    tab_control.add(tab_1, text='Aufnahmen')
    tab_control.add(tab_2, text='Klassifizierung')
    tab_control.pack(expand=1, fill="both")

    # -----------------------------------

    frame_left = ttk.Frame(tab_1, padding=40, style='left.TFrame')
    frame_left.pack(anchor='w', fill='y', expand=False, side='left')

    button_1 = ttk.Button(frame_left, text="Neue Aufnahme", width=25)
    button_1.pack(pady=10)
    button_2 = ttk.Button(frame_left, text="Aufnahme laden", width=25)
    button_2.pack(pady=10)

    label_info_1 = ttk.Label(frame_left, text="Informationen")
    label_info_1.pack(pady=10)

    # Add a Treeview widget
    tree_information = ttk.Treeview(frame_left, show='headings', height=8)
    tree_information['columns'] = ('feature', 'value')

    tree_information.column("# 1", anchor='w', width=80)
    tree_information.heading("# 1", text="Merkmal", anchor='w')

    tree_information.column("# 2", anchor='w', width=80)
    tree_information.heading("# 2", text="Wert", anchor='w')

    # Insert the data in Treeview widget
    tree_information.insert(parent='', index='end', iid='i1', values=('info 1', '0'))
    tree_information.insert(parent='', index='end', iid='i2', values=('info 2', '0'))
    tree_information.insert(parent='', index='end', iid='i3', values=('info 3', '0'))
    tree_information.insert(parent='', index='end', iid='i4', values=('info 4', '0'))
    tree_information.insert(parent='', index='end', iid='i5', values=('info 5', '0'))
    tree_information.insert(parent='', index='end', iid='i6', values=('info 6', '0'))
    tree_information.insert(parent='', index='end', iid='i7', values=('info 7', '0'))
    tree_information.insert(parent='', index='end', iid='i8', values=('info 8', '0'))

    tree_information.pack()

    tree_information.item('i3', values=('info 3', '2'))

    # -----------------------------------

    frame_right = ttk.Frame(tab_1)
    frame_right.pack(anchor='n', fill='both', expand=True, side='left')

    frame_radiobuttons = ttk.Frame(frame_right)
    frame_radiobuttons.pack()

    selected = tk.StringVar()
    radiobutton_1 = ttk.Radiobutton(frame_radiobuttons, text='time plot', value='value_1', variable=selected)
    radiobutton_2 = ttk.Radiobutton(frame_radiobuttons, text='fft plot', value='value_2', variable=selected)
    radiobutton_3 = ttk.Radiobutton(frame_radiobuttons, text='spectoram', value='value_3', variable=selected)

    selected.set('value_1')

    radiobutton_1.grid(column=0, row=0)
    radiobutton_2.grid(column=1, row=0)
    radiobutton_3.grid(column=2, row=0)

    figure = Figure(figsize=(6, 4), dpi=100)
    figure_canvas = FigureCanvasTkAgg(figure, frame_right)
    NavigationToolbar2Tk(figure_canvas, frame_right)
    axes = figure.add_subplot()
    figure.set_facecolor('#F0F0F0')
    graph.create_graph(axes)
    figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    return root

