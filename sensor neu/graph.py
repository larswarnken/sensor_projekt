import gui

loaded_sample_rate = 0
loaded_record_time = 0
loaded_data = []

def get_current_path():
    return ''

def read_data():
    global loaded_sample_rate
    global loaded_record_time
    global loaded_data

    path = get_current_path()


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


def plot_time(figure_plots, canvas_plots, path):
    print('plotted time')

    read_data(path)

    figure_plots.clear()
    subplot = figure_plots.add_subplot(1, 1, 1)
    subplot.plot(loaded_data)
    subplot.set_xlabel("Time")
    subplot.set_ylabel("Amplitude")
    canvas_plots.draw()


def plot_fft(figure_plots, canvas_plots):
    print('plotted fft')
    figure_plots.clear()


def plot_spectrogram(figure_plots, canvas_plots):
    print('plotted spectrogram')
    figure_plots.clear()
