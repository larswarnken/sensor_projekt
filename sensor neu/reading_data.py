import json
import os

loaded_sample_rate = 0
loaded_record_time = 0
loaded_data = []
current_path = ''


def get_output_path():
    with open('test.json', 'r') as f:
        output_path = json.load(f)
    output_path = os.path.join(os.path.dirname(__file__), output_path["outputPath"].replace("/", "\\"))

    global current_path
    current_path = output_path
    return output_path


def read_data(path):
    global loaded_sample_rate
    global loaded_record_time
    global loaded_data
    global current_path

    current_path = path

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
    except:
        print("reading error")


def detect_hit():
    global loaded_data
    global loaded_sample_rate

    if len(loaded_data) > 0:

        max_value = max(loaded_data)

        puffer_seconds = 1.5
        puffer_samples = round(puffer_seconds * loaded_sample_rate)

        trigger_value = max_value * 0.4

        if len(loaded_data) > puffer_samples:

            for value in loaded_data:
                if value >= trigger_value:
                    start_index = round(loaded_data.index(value) - loaded_sample_rate * 0.10)
                    end_index = start_index + puffer_samples

                    cut_data = loaded_data[start_index:end_index]

                    print('length cut data: ', len(cut_data))

                    loaded_data = cut_data

                    break
        else:
            print('data too short')
    else:
        print('no data loaded')


def get_loaded_data():
    global loaded_data
    return loaded_data


def get_loaded_sample_rate():
    global loaded_sample_rate
    return loaded_sample_rate


def get_loaded_record_time():
    global loaded_record_time
    return loaded_record_time


def get_current_path():
    global current_path
    return current_path


def set_current_path(path):
    global current_path
    current_path = path
