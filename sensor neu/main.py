import tkinter as tk
from tkinter import ttk
import matplotlib
import second

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)

root = tk.Tk()
root.title("title")
root.geometry('854x480')

style = ttk.Style(root)
current_theme = style.theme_use()
style.theme_use('xpnative')
style.configure('TFrame', background='lightblue')
style.configure('Frame1.TFrame', background='green')
style.configure('Frame2.TFrame', background='orange')

matplotlib.use('TkAgg')

tab_control = ttk.Notebook(root)
tab_1 = ttk.Frame(tab_control)
tab_2 = ttk.Frame(tab_control)
tab_control.add(tab_1, text='Aufnahmen')
tab_control.add(tab_2, text='Klassifizierung')
tab_control.pack(expand=1, fill="both")

# -----------------------------------

frame_left = ttk.Frame(tab_1, style='Frame1.TFrame', padding=40)
frame_left.pack(anchor='w', fill='y', expand=False, side='left')


button_1 = ttk.Button(frame_left, text="Neue Aufnahme", width=20)
button_1.pack(pady=10)
button_2 = ttk.Button(frame_left, text="Aufnahme laden", width=20)
button_2.pack(pady=10)

label_info_1 = ttk.Label(frame_left, text="info: info")
label_info_1.pack()

# -----------------------------------

frame_right = ttk.Frame(tab_1, style='Frame2.TFrame')
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
axes.set_title('Top 5 Programming Languages')
axes.set_ylabel('Popularity')
figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


root.mainloop()



