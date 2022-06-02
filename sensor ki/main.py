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


classes = [0, 1, 2, 3]  # gummi, metall, plastik, stift
classes_np = np.asarray(classes)


# kombiniert alle cvs files zu einer, brauchen wir eigentlich nicht mehr
def get_x_data():
    gummi_dataframe = pd.read_csv("gummi.csv")
    metall_dataframe = pd.read_csv("metall.csv")
    plastik_dataframe = pd.read_csv("plastik.csv")
    stift_dataframe = pd.read_csv("stift.csv")

    combined_data = gummi_dataframe.append(metall_dataframe, ignore_index=True)
    combined_data = combined_data.append(plastik_dataframe, ignore_index=True)
    combined_data = combined_data.append(stift_dataframe, ignore_index=True)

    combined_data.to_csv(f"combined.csv", index=False)

    return combined_data


if __name__ == '__main__':

    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=50, shuffle=True)    # split dataset to train model and test it
    # clf = MLPClassifier(max_iter=300, hidden_layer_sizes=30, learning_rate="adaptive").fit(X_train, y_train)   # train MLPClassifier
    # predict = clf.predict(X_test[:20, :]) # predict material from test dataset   1 = hammer - plastic ...
    # score = clf.score(X_test, y_test)   # Accuracy - How many times did he get it right in real use case
    #
    # print("predict", predict)
    #
    # print("Accuracy: ", score)

    # csv to panda dataframe, select features
    X2 = pd.read_csv("combined.csv")  # pandas dataframe
    data = X2.dropna(axis=1)
    selected_features = tsfresh.select_features(data, data["id_KI"])

    data_features = selected_features.iloc[:, 3:10]  # feature spalten 3 bis 10
    data_target = data["id_KI"].to_numpy()

    pd.plotting.scatter_matrix(data_features,
                               c=data_target,
                               figsize=(8, 8)
                               )

    # plt.show()

    # classes
    y2 = X2.iloc[:, -1:]
    y2 = y2.values.tolist()
    y3 = []
    for element in y2:
        y3.append(element[0])
    y3 = np.array(y3)

    ki_id_column = len(X2.columns) - 1
    data = X2.iloc[:, :]  # X2.iloc[:, [1, 2, 3, ki_id_column]]

    results = []

    time_1 = datetime.datetime.now().replace(microsecond=0)

    # trains and tests ai n times, calculates average accuracy
    repeat_n_times = 10
    for i in range(repeat_n_times):
        # training
        selected_features = selected_features.iloc[:, :20]  # Nicht alle Merkmale benutzen
        X_train, X_test, y_train, y_test = train_test_split(selected_features, y3, test_size=0.1, shuffle=True)
        clf = MLPClassifier(max_iter=1000, hidden_layer_sizes=10, learning_rate="adaptive", batch_size=5).fit(X_train,
                                                                                                              y_train)
        predict = clf.predict(X_test)  # predict material from test dataset   1 = hammer - plastic ...
        score = clf.score(X_test, y_test)  # Accuracy - How many times did he get it right in real use case

        # print("predict", predict)
        #
        # print("Accuracy: ", score)

        # print(X_test[0])

        results.append(score)

        progress_value = round(i / repeat_n_times * 10)
        sys.stdout.write("\rprogress |{0}{1}|".format("=" * progress_value, " " * (10 - progress_value)))
        sys.stdout.flush()

    time_2 = datetime.datetime.now().replace(microsecond=0)

    print(time_2-time_1)

    # print(results)

    print(sum(results)/len(results))






















