import dask.dataframe
import numpy as np
import pandas as pd
import tsfresh
from os import walk
import datetime
import sys
import time
from tsfresh import extract_relevant_features

# EfficientFCParameters ist ein Dictionary, welches nur schnell zu berechnende Features heranzieht
from tsfresh.feature_extraction import extract_features, EfficientFCParameters, feature_calculators, \
    ComprehensiveFCParameters

from tsfresh import select_features
from tsfresh.utilities.dataframe_functions import impute

from tsfresh import extract_features
from tsfresh.feature_selection.relevance import calculate_relevance_table


# lädt daten aus txt datei und gibt diese als dataframe zurück
def read_data_from_file(path):
    data_temp = []
    with open(path, "r") as file:
        next(file)  # erste line ist header mit sample rate und aufnahmedauer, also skippen
        for line in file:
            line.replace("\n", "")
            data_temp.append(float(line))

    data_temp = data_temp  # [4500:14500]  # nur 10.000 frames zum testen

    # in dataframe umwandeln
    data_temp = pd.DataFrame(data_temp, columns=["data"])
    data_temp["id"] = 0

    return data_temp


# gibt ne liste mit allen dateien in einem ordner zurück
def give_files_in_dir(path):
    filenames = next(walk(path), (None, None, []))[2]  # [] if no file
    return filenames


def extract_features_from_file(path):
    data = read_data_from_file(path)

    settings = EfficientFCParameters()

    features = tsfresh.extract_features(data, column_id="id", default_fc_parameters=settings)

    features.to_csv("features.csv", index=False)



if __name__ == '__main__':

    # folders = ["gummi", "metall", "plastik", "stift"]
    #
    # y_list = []
    #
    # for folder in folders[0:1]:
    #     print(folder)
    #     time_1 = datetime.datetime.now().replace(microsecond=0)
    #     # dateien im ordner holen
    #     files_list = give_files_in_dir(f"Aufnahmen getrennt/{folder}")
    #     # durch jede file im ordner gehen
    #     all_features = pd.DataFrame()
    #     for element in files_list[0:1]:
    #         data = read_data_from_file(f"Aufnahmen getrennt/{folder}/{element}")
    #
    #         if files_list.index(element) % 10 == 0 and files_list.index(element) != 0:
    #             print(f"progress: {files_list.index(element)} von {len(files_list)}")
    #
    #         settings = EfficientFCParameters()
    #
    #         features = tsfresh.extract_features(data, column_id="id", default_fc_parameters=settings)
    #
    #         # features = []
    #         # data = pd.DataFrame.to_numpy(data)
    #         # print(type(tsfresh.feature_extraction.feature_calculators.autocorrelation(data, 3)))
    #
    #         if element == files_list[0]:  # beim ersten durchgang soll die variable erstellt werden
    #             all_features = features
    #         else:  # und nach ersten durchlauf nur noch erweitern der matrix
    #             all_features = pd.concat([all_features, features], axis=0)
    #         all_features["id_KI"] = folders.index(folder)  # 0: gummi, 1: metall, 2:plastik, 3: stift
    #
    #     print(all_features)
    #
    #     # speichern des feature dataframes als csv
    #     all_features.to_csv(f"{folder}.csv", index=False)
    #
    #     time_2 = datetime.datetime.now().replace(microsecond=0)
    #
    #     print(f"total time: {time_2 - time_1}")

    extract_features_from_file('Aufnahmen getrennt/gummi/gummi1_1.txt')
