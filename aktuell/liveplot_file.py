import threading

from PyQt5 import QtWidgets, QtCore
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import os
from random import randint
import json
import time
import subprocess

from PyQt5.QtCore import QCoreApplication


class MainWindow(QtWidgets.QMainWindow):
    data_filename_var = ''
    loaded_sample_rate = None
    loaded_record_time = None
    loaded_data = None
    currently_recording = False

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)

        self.x = []
        self.y = []

        self.graphWidget.setBackground('w')

        pen = pg.mkPen(color=(100, 100, 255))
        self.data_line = self.graphWidget.plot(self.x, self.y, pen=pen)

        self.graphWidget.setYRange(-1, 1)

        # self.show()

        # # ... init continued ...
        # self.timer = QtCore.QTimer()
        # self.timer.setInterval(50)
        # self.timer.timeout.connect(self.update_plot_data)
        # self.timer.start()

        self.new_recording_thread()

        print(type(self.graphWidget))

        # self.load_data()
        #
        # print('bla')
        #
        # self.plot()

    def update_plot_data(self):
        self.x = self.x[1:]  # Remove the first y element.
        self.x.append(self.x[-1] + 1)  # Add a new value 1 higher than the last.

        self.y = self.y[1:]  # Remove the first
        self.y.append(randint(0, 100))  # Add a new random value.

        self.data_line.setData(self.x, self.y)  # Update the data.

    def check_if_recording(self):
        file_size = -1

        # gets recently created file
        with open('test.json', 'r') as f:
            output_path = json.load(f)
        data_filename_var = os.path.join(os.path.dirname(__file__), output_path["outputPath"].replace("/", "\\"))

        print(output_path["outputPath"])

        # checks if recording has started
        while True:
            if not os.path.isfile(f'{output_path["outputPath"]}'):
                continue
            else:
                print("recording...")
                self.currently_recording = True

                liveplot_thread = threading.Thread(target=self.plot)
                liveplot_thread.start()

                break

        # checks if recording stops
        while True:
            time.sleep(0.5)
            current_file_size = os.path.getsize(f'{output_path["outputPath"]}')

            if current_file_size != file_size:
                file_size = current_file_size
            else:
                print("stopped recording yo")
                self.currently_recording = False

                break
        # self.close()
        # sys.exit()
        QCoreApplication.quit()
        self.close()

    def new_recording_thread(self):
        check_if_recording_thread = threading.Thread(target=self.check_if_recording)
        check_if_recording_thread.start()

    def load_data(self):

        with open('test.json', 'r') as f:
            output_path = json.load(f)
        # reads data from file
        with open(f'{output_path["outputPath"]}', 'r') as file:
            details = file.read()
            x = details.split('\n')
        try:
            # saves info from first line
            self.loaded_sample_rate = int(x[0].split(", ")[0])
            self.loaded_record_time = int(x[0].split(", ")[1])
            # delete first line which is samlpe rate and time
            x.pop(0)
            # adds data to list
            self.loaded_data = []
            for i in x:
                if i != '':
                    self.loaded_data.append(float(i))
        except:
            print("idk")

    def plot(self):
        while self.currently_recording:
            self.load_data()
            if self.loaded_data is not None:
                if len(self.loaded_data) <= 20000:
                    self.x = list(range(len(self.loaded_data)))
                    self.y = self.loaded_data

                    # self.x = self.x[1:]  # Remove the first y element.
                    # self.x.append(self.x[-1] + 1)  # Add a new value 1 higher than the last.
                    #
                    # self.y = self.y[1:]  # Remove the first
                    # self.y.append(randint(0, 1))  # Add a new random value.
                    #
                    # self.data_line.setData(self.x, self.y)  # Update the data.
                else:
                    self.x = list(range(len(self.loaded_data) - 20000, len(self.loaded_data)))
                    self.y = self.loaded_data[len(self.loaded_data) - 20000:len(self.loaded_data)]

                time.sleep(0.1)
            else:
                self.x = list(range(100))
                self.y = []

            self.data_line.setData(self.x, self.y)  # Update the data.


def main():
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
