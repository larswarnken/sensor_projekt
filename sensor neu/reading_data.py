import json
import os

loaded_sample_rate = 0
loaded_record_time = 0
loaded_data = []


def get_output_path():
    with open('test.json', 'r') as f:
        output_path = json.load(f)
    output_path = os.path.join(os.path.dirname(__file__), output_path["outputPath"].replace("/", "\\"))
    return output_path


def read_data(path):
    global loaded_sample_rate
    global loaded_record_time
    global loaded_data

    # reads data from file
    with open(path, 'r') as file:
        details = file.read()
        x = details.split('\n')
    try:
        # saves info from first line
        loaded_sample_rate = int(x[0].split(", ")[0])
        loaded_record_time = int(x[0].split(", ")[1])
        # delete first line which is samlpe rate and time
        x.pop(0)
        # adds data to list
        loaded_data = []
        for i in x:
            if i != '':
                loaded_data.append(float(i))

        print(len(loaded_data))


    except:
        print("reading error")


def get_loaded_data():
    global loaded_data
    return loaded_data


def get_loaded_sample_rate():
    global loaded_sample_rate
    return loaded_sample_rate


def get_loaded_record_time():
    global loaded_record_time
    return loaded_record_time






