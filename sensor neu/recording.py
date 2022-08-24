import threading
import os
import subprocess
import json
import time
import graph
import reading_data
from tkinter import filedialog


def check_if_recording():
    file_size = -1
    recording_path = reading_data.get_output_path()

    # checks if recording has started by checking if new file has been created yet
    while True:
        if not os.path.isfile(recording_path):
            continue
        else:
            print("recording...")
            print(recording_path)
            break

    # checks if recording stops by comparing file sizes
    while True:
        time.sleep(0.5)
        current_file_size = os.path.getsize(recording_path)

        if current_file_size != file_size:
            file_size = current_file_size
        else:
            print("stopped recording")
            break


def new_recording():
    cpp_file = os.path.join(os.path.dirname(__file__), 'c++\\record.exe')
    subprocess.call([cpp_file])


def new_recording_thread():
    record_thread = threading.Thread(target=new_recording, daemon=True)
    record_thread.start()

    time.sleep(0.5)

    check_if_recording_thread = threading.Thread(target=check_if_recording, daemon=True)
    check_if_recording_thread.start()


def load_recording(path):
    loaded_path = filedialog.askopenfilename(initialdir=f'{os.getcwd()}/Aufnahmen',
                                             title="Select a File",
                                             filetypes=(("Text files", "*.txt"),
                                                        ("all files", "*.*")))
    print(loaded_path)
    reading_data.read_data(loaded_path)
