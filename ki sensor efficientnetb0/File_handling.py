from pandas import DataFrame
from datetime import datetime
from contextlib import redirect_stdout
import os
import pickle

import pandas as pd
file_name = datetime.now().strftime("%Y_%m_%d_%H_%M") + '_Trainingsdaten.txt'
diretory_name = datetime.now().strftime("%Y_%m_%d_%H_%M") + '_Model'
diretory_name2 = datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + '_Model'


def write_train_data(content):
    """
    Writes the content into a text file
    :param content: String to write
    :return: None
    """
    with open(file_name, 'a') as file:
        file.write(content + '\n')


def write_model_summary_to_file(model):
    """
    Writes the model summary into a text file
    :param model: The model to summarize
    :return: None
    """
    with open(file_name, 'a') as file:
        with redirect_stdout(file):
            model.summary()


def save_history_to_file(history):
    """
    saves the model history to a textfile

    params:
            history: model history
    """
    with open('model_history', 'wb') as file_pi:
        pickle.dump(history.history, file_pi)


def open_directories(directory_path):
    """
    opens and traverses the directories.
    """
    for subdir, dirs, files in os.walk(directory_path):
        if subdir.__contains__("Example") and files.__len__() == 0:
            file_numbers = []
            for _, _, file in os.walk(subdir):
                file_numbers.append(file.__len__())
                # The first part of the path is not needed
            subdir = subdir[60:]
            subdir = subdir.replace('\\', '/')
            # Split path by \ into substrings, which mark the class
            split_string = subdir.split('/')
            file_numbers.clear()


def change_working_directory():
    """
    Changes the current working directory
    """
    os.getcwd()
    path = '../Modelle/' + datetime.now().strftime("%Y_%m_%d_%H_%M") + '_Model' + '/'
    try:
        os.mkdir(path)
        os.chdir(path)
    except OSError:
        #path = '../Modelle/' + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + '_Model' + '/'
        os.mkdir(path)
        os.chdir(path)
        print('Creation of the directory %s failed' % path)


if __name__ == "__main__":
    open_directories("")
