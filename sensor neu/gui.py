import tkinter as tk
from tkinter import ttk
import graph
import reading_data
import recording

import matplotlib

matplotlib.use('TkAgg')

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)

from matplotlib.figure import Figure


class MainApplication(tk.Frame):
    current_path = 'D:/Benutzer/Lars/Dokumente/GitHub/sensor_projekt/sensor neu/Aufnahmen/data_10.txt'

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        parent.title("title")
        parent.geometry('1280x720')

        # styles
        style = ttk.Style(parent)
        current_theme = style.theme_use()
        #  style.theme_use('xpnative')
        # style.configure('TFrame', background='green')
        style.configure('left.TFrame', background='#F0F0F0')  # #F0F0F0
        # style.configure('right.TFrame', background='white')

        # tab control
        tab_control = ttk.Notebook(parent)
        tab_1 = ttk.Frame(tab_control)
        tab_2 = ttk.Frame(tab_control)
        tab_control.add(tab_1, text='Aufnahmen')
        tab_control.add(tab_2, text='Klassifizierung')
        tab_control.pack(expand=True, fill="both")

        # tab 1 -----------------------------------

        # left frame
        frame_left = ttk.Frame(tab_1, padding=30, style='left.TFrame')
        frame_left.pack(anchor='w', fill='y', expand=False, side='left')

        # buttons: neue aufnahme, aufnahme laden
        button_1 = ttk.Button(frame_left, text="Neue Aufnahme", width=25,
                              command=lambda: [recording.new_recording_thread(), plot_changed(selected)])
        button_1.pack(pady=10)
        button_2 = ttk.Button(frame_left, text="Aufnahme laden", width=25,
                              command=lambda: [recording.load_recording(self.current_path), plot_changed(selected)])
        button_2.pack(pady=10)

        label_current_file = ttk.Label(frame_left, text='Aktuell geladen: -')
        label_current_file.pack()

        # info part label
        label_info_1 = ttk.Label(frame_left, text="Informationen")
        label_info_1.pack(pady=10)

        # tree widget for information
        tree_information = ttk.Treeview(frame_left, show='headings', height=8)
        tree_information['columns'] = ('feature', 'value')

        tree_information.column("# 1", anchor='w', width=120)
        tree_information.heading("# 1", text="Merkmal", anchor='w')

        tree_information.column("# 2", anchor='w', width=60)
        tree_information.heading("# 2", text="Wert", anchor='w')

        tree_information.insert(parent='', index='end', iid='i1', values=('Aufnahmelänge', '0'))
        tree_information.insert(parent='', index='end', iid='i2', values=('Abtastrate', '0'))
        tree_information.insert(parent='', index='end', iid='i3', values=('max Ampl.', '0'))
        tree_information.insert(parent='', index='end', iid='i4', values=('max Ampl. Zeit', '0'))
        tree_information.insert(parent='', index='end', iid='i5', values=('RMS', '0'))
        tree_information.insert(parent='', index='end', iid='i6', values=('Signalenergie', '0'))
        tree_information.insert(parent='', index='end', iid='i7', values=('max Ampl. FFT', '0'))
        tree_information.insert(parent='', index='end', iid='i8', values=('max Ampl. Freq.', '0'))

        tree_information.pack()

        button_detect_hit = ttk.Button(frame_left, text="Schlag erkennen", width=25,
                                       command=lambda: [reading_data.detect_hit(), plot_changed(selected)])
        button_detect_hit.pack(pady=10)

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

        # tab 2 -----------------------------------

        import main_neuGUI_O

        info = tk.Label(tab_2, justify='left', font=("Helvetica", 16),
                        text="""\
                            Methoden zur Klassifizierung 

                 1) Gewünschte Methode wählen.
                 2) cross validation oder normale Wiederholung wählen
                 3) test size eingeben (eine Zahl zwischen 0 und 0.5 ).
                 4) Taste "Speichern" drücken
                 5) Taste "Durchführen" drücken.""", bg="white")

        mth_NW = "neural network"
        mth_DT = "decision tree"
        crossVali_yes = "cross validation"
        crossVali_no = "normale Wiederholung"

        methode_wahl = tk.StringVar(tab_2)
        methode_wahl.set(mth_NW)  # default value
        ifCrossVali = tk.StringVar(tab_2)
        ifCrossVali.set(crossVali_yes)  # default value

        tk.Label(tab_2, text="test size", bg="white", font=("Helvetica", 16)).grid(row=4)
        tk.Label(tab_2, text="repeat n times", bg="white", font=("Helvetica", 16)).grid(row=5)

        entry_testSize = ttk.Entry(tab_2)
        entry_repeatTimes = ttk.Entry(tab_2)

        option_methode = tk.OptionMenu(tab_2, methode_wahl, mth_NW, mth_DT)
        option_methode.configure(width=25, font=("Helvetica", 16))
        optionen_cv = tk.OptionMenu(tab_2, ifCrossVali, crossVali_yes, crossVali_no)
        optionen_cv.configure(width=25, font=("Helvetica", 16))

        label_egbs1 = tk.Label(tab_2, justify='center', font=("Helvetica", 16), text="Genauigkeit: ", bg="white")
        label_egbs2 = tk.Label(tab_2, justify='center', font=("Helvetica", 16), text="ausgewogene Genauigkeit( bac ): ",
                               bg="white")
        label_egbs3 = tk.Label(tab_2, justify='center', font=("Helvetica", 16), text="Material: ", bg="white")

        ausgabe1 = tk.Label(tab_2, justify='center', font=("Helvetica", 16), text=" ", bg="white")
        ausgabe2 = tk.Label(tab_2, justify='center', font=("Helvetica", 16), text=" ", bg="white")
        ausgabe3 = tk.Label(tab_2, justify='center', font=("Helvetica", 16), text=" ", bg="white")  # predict result

        tk.Button(tab_2, text='Speichern', command=lambda: button_action_save(), font=("Helvetica", 16)).grid(row=5, column=2,
                                                                                                   sticky='w', pady=20)

        run_button = tk.Button(tab_2, text="Durchführen", font=("Helvetica", 16), command=lambda: button_action_execute())
        load_classifier_button = tk.Button(tab_2, text="Klassifikator laden", font=("Helvetica", 16),
                                           command=lambda: button_action_load_klassifikator())
        predict_button = tk.Button(tab_2, text="Klassifizierung", font=("Helvetica", 16), command=lambda: button_action_predict())

        info.grid(row=0, column=0, columnspan=3, pady=20, padx=150)
        option_methode.grid(row=1, column=0, columnspan=1, pady=20)
        optionen_cv.grid(row=1, column=1, columnspan=1, pady=20)

        run_button.grid(row=6, column=1, pady=20)
        load_classifier_button.grid(row=1, column=3, sticky='w', pady=20)
        predict_button.grid(row=2, column=3, sticky='w', pady=20)

        label_egbs1.grid(row=7, column=0, pady=20)
        label_egbs2.grid(row=8, column=0, pady=20)
        label_egbs3.grid(row=3, column=3, pady=20)
        # optionen_cv.grid_rowconfigure(1,weight=1)
        ausgabe1.grid(row=7, column=1, columnspan=2, pady=20)
        ausgabe2.grid(row=8, column=1, columnspan=2, pady=20)
        ausgabe3.grid(row=3, column=4, columnspan=2, pady=20)

        entry_testSize.grid(row=4, column=1, pady=20)
        entry_repeatTimes.grid(row=5, column=1, pady=20)


        def button_action_save():
            testsize_str = entry_testSize.get()
            global testsize
            testsize = float(testsize_str)

            repeat_n_times_str = entry_repeatTimes.get()
            global repeat_n_times
            repeat_n_times = int(repeat_n_times_str)

            wahl1 = methode_wahl.get()
            if wahl1 == mth_NW:
                global klassi_methode
                klassi_methode = "neural_network"
            elif wahl1 == mth_DT:
                klassi_methode = "decision_tree"

            wahl2 = ifCrossVali.get()
            if wahl2 == crossVali_yes:
                global wh_methode
                wh_methode = "True"
            elif wahl2 == crossVali_no:
                wh_methode = "False"

        def button_action_execute():
            results = main_neuGUI_O.result(klassi_methode, wh_methode, repeat_n_times, testsize)
            global score
            score = results[0]
            ausgabe1.configure(text=str(score) + "%")
            global balanced_accuracy
            balanced_accuracy = results[1]
            ausgabe2.configure(text=str(balanced_accuracy) + "%")

        def button_action_load_klassifikator():
            from tkinter import filedialog as fd

            filename = fd.askopenfilename()
            global classifier
            classifier = main_neuGUI_O.load_classifier(filename)
            print(classifier)

        # todo gespeicherte Klassifikator .pickle datei auswählen

        def button_action_predict():
            # to vorhersagende Data-> test_data in
            data_list = main_neuGUI_O.get_test_data()
            # print(data_list)
            global prediction
            prediction = main_neuGUI_O.predict_single_data(classifier, data_list)
            ausgabe3.configure(text=prediction)



















        def plot_changed(value_p):
            if value_p.get() == 'timeplot':
                graph.plot_time(figure_plots, canvas_plots)
                reading_data.change_info(tree_information)
            elif value_p.get() == 'fftplot':
                graph.plot_fft(figure_plots, canvas_plots)
                reading_data.change_info(tree_information)
            elif value_p.get() == 'spectrogram':
                graph.plot_spectrogram(figure_plots, canvas_plots)
            else:
                print('radio button value error')

        def on_closing():
            exit()

        parent.protocol("WM_DELETE_WINDOW", on_closing)
        parent.mainloop()
