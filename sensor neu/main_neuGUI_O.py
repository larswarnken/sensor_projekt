import numpy as np
import pandas as pd
import tsfresh
import tsfresh as ts
from sklearn.neural_network import MLPClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import sys
import datetime
from tkinter import *
import tkinter as tk
from tkinter import *
from tkinter import ttk
from sklearn.model_selection import KFold
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as pyplot
import pickle
from matplotlib import style
from sklearn.preprocessing import StandardScaler


# ---------------------------------------------
classes = [0, 1, 2, 3]  # gummi, metall, plastik, stift
material_class = ["gummi", "metall", "plastik", "stift"]
methodes = [0, 1]  # neural_network, decision_tree
classes_np = np.asarray(classes)
# testsize = 0
# repeat_n_times = 0
selected_features = tsfresh.select_features
#test_data = [[],[]]



# --------------------------------------------
'''def button_action():
    # repeat_n_time()

    wahl = variable.get()
    if wahl == u1:
        message = str(result("neural_network",crossvalidation)) + "%"
    elif wahl == u2:
        message = str(result("decision_tree",crossvalidation)) + "%"

    ausgabe.configure(text=message)'''

#
# def find_features(features_list, df):
#     df.drop(columns= features_list)
#     return df


def result(methode, crossvalidation, repeat_n_times, testsize):
    X2 = pd.read_csv("combined_10_features.csv")  # pandas dataframe
    data = X2.dropna(axis=1)
    data.drop('id_KI',axis=1, inplace=True)


    # classes
    y2 = X2.iloc[:, -1:]
    y2 = y2.values.tolist()
    y3 = []
    for element in y2:
        y3.append(element[0])
    y3 = np.array(y3)

    print("Merkmale:")
    print(data.columns.values)

    relevant_features = list(data.columns)


    print("crossvalidation:", crossvalidation)
    results = []
    bac_list = []

    global pp

    if (crossvalidation == "True"):
        print("repeat n times:", repeat_n_times)
        print("split in n folds:", (int)(1 / testsize))
        for i in range(repeat_n_times):
            data = np.array(data)
            X, y = data, y3
            kf = KFold(n_splits=(int)(1 / testsize), shuffle=True)
            kf.get_n_splits(X)
            print(kf)
            pp = PdfPages("decision_trees_crossvalidation.pdf")
            num_x = 1
            for train_index, test_index in kf.split(X):
                X_train, X_test = X[train_index], X[test_index]
                y_train, y_test = y[train_index], y[test_index]
                if (methode == "neural_network"):
                    X_train, X_test = scale_data(X_train, X_test)
                    score = neural_network(X_train, X_test, y_train, y_test, bac_list)
                if (methode == "decision_tree"):
                    score = decision_tree(X_train, X_test, y_train, y_test, num_x, bac_list)
                    num_x += 1
                results.append(score)


    else:
        pp = PdfPages("decision_trees.pdf")
        print("repeat n times:", repeat_n_times)
        print("test size:", testsize)
        for i in range(repeat_n_times):
            # training

            X_train, X_test, y_train, y_test = train_test_split(data, y3, test_size=testsize, shuffle=True)


            if (methode == "neural_network"):
                X_train, X_test = scale_data(X_train, X_test)
                score = neural_network(X_train, X_test, y_train, y_test, bac_list)
            if (methode == "decision_tree"):
                # save multiple decision trees plots in one file
                score = decision_tree(X_train, X_test, y_train, y_test, i+1, bac_list)
            results.append(score)

    pp.close()
    result = sum(results) / len(results)  # durchschnitt von results
    bac =  sum(bac_list) / len(bac_list)
    return result * 100, bac*100

# def get_test_data():
#     return test_data

# kombiniert alle cvs files zu einer, brauchen wir eigentlich nicht mehr
# def get_x_data():
#     gummi_dataframe = pd.read_csv("gummi.csv")
#     metall_dataframe = pd.read_csv("metall.csv")
#     plastik_dataframe = pd.read_csv("plastik.csv")
#     stift_dataframe = pd.read_csv("stift.csv")
#
#     combined_data = gummi_dataframe.append(metall_dataframe, ignore_index=True)
#     combined_data = combined_data.append(plastik_dataframe, ignore_index=True)
#     combined_data = combined_data.append(stift_dataframe, ignore_index=True)
#
#     combined_data.to_csv(f"combined.csv", index=False)
#
#     return combined_data

# ---------------------------------------------
def neural_network(X_train, X_test, y_train, y_test, bac_list):
    clf = MLPClassifier(max_iter=1000, hidden_layer_sizes=10, learning_rate="adaptive", batch_size=5).fit(X_train,
                                                                                                          y_train)
    y_pred = clf.predict(X_test)  # predict material from test dataset   1 = hammer - plastic ...
    score1 = clf.score(X_test, y_test)  # Accuracy - How many times did he get it right in real use case
    # score2 = get_score(y_pred, y_test)
    bac = balanced_accuracy(y_pred, y_test)

    if( (score1>=0.95) and (bac>=0.95)):
        with open("neural_network_model.pickle", "wb") as f:
            pickle.dump(clf, f)


    print("Genauigkeit des neural network(FKT):", score1)
    # print("Genauigkeit des neural network:", score2)
    bac_list.append(bac)
    print("balanced accuracy des neural network:", bac)

    return score1


def decision_tree(X_train, X_test, y_train, y_test, num_x, bac_list):
    from sklearn import tree


    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    score1 = clf.score(X_test, y_test)

    fig = plt.figure()
    _ = tree.plot_tree(clf,
                       filled=True)
    plt.title("Decision tree Nr." + str(num_x))
    pp.savefig(fig)
    plt.close()


    # score2 = get_score(y_pred, y_test)
    bac = balanced_accuracy(y_pred, y_test)

    # das Model als pickle datei speichern, wenn das score und bac sind >= 95%
    if ((score1 >= 0.95) and (bac >= 0.95)):
        with open("decision_tree_model.pickle", "wb") as f:
            pickle.dump(clf, f)


    bac_list.append(bac)
    print("Genaurigkeit des decision tree(FKT):", score1)
    # print("Genaurigkeit des decision tree:", score2)
    print("balanced accuracy des decision tree:", bac)

    return score1


def balanced_accuracy(y_pred, y_test):
    score_classes = np.zeros(len(classes))  # zeros is a null vektor
    class_no = np.zeros(len(classes))
    for i in range(len(y_pred)):  # Samples durchgehen
        for j in range(len(classes)):  # schauen welche Klasse vorliegt
            if y_test[i] == classes[j]:
                if y_pred[i] == y_test[i]:
                    score_classes[j] += 1  # wenn Klasse richtig vorhergesagt, Klassencounter hochsetzen
                class_no[j] += 1  # zählen welche Klasse wie oft in ytest vorliegt
    for j in range(len(classes)):
        score_classes[j] = score_classes[j] / class_no[j]  # accuracy für jede Klasse separat berechnen
        print("Klass-",j,":",score_classes[j])
    bac = np.mean(score_classes)  # balanced accuracy

    return bac

# gespeicherte Klassifikator aufrufen
def load_classifier(modul_name):
    global is_neural_network
    if modul_name == 'C:/Users/shenj/Desktop/SystemProjekt/aktuell/10 Features Version/neural_network_model.pickle':
        is_neural_network  = True
    else:
        is_neural_network = False
    pickle_in = open(modul_name, "rb") # z.B. pickle_in = open("decision_tree_model.pickle", "rb")
    print(pickle_in)
    clf = pickle.load(pickle_in)
    print("is_neural_network:", is_neural_network)
    return clf

# todo für MLP Skalieren
# einzeln Aufnahme vorhersagen, data_list-> eindemensionaler Vektor: Merkmale list für die zu vorhersagende Aufnahme
def predict_single_data(modul):
    clf = modul
    data_list = get_data_list_one_recording()
    if is_neural_network == True:
        data_list = scale_data_predict(data_list)
        print("data_list_scale:", data_list)
    prediction_index = clf.predict(data_list)[0]
    #print(clf.predict(data_list))
    print(prediction_index)
    print(material_class[prediction_index])
    return material_class[prediction_index]

# data skalieren
def scale_data(X_train, X_test):

    global scaler
    scaler = StandardScaler()
    scaler.fit(X_train)
    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)
    return X_train, X_test

def scale_data_predict(X):

    X = scaler.transform(X)
    return X


def get_data_list_one_recording():
    X2 = pd.read_csv("features.csv")  # pandas dataframe
    data = X2.dropna(axis=1)
    print(data.columns.values)
    data = np.array(data)
    return data

