import gui
import reading_data


def plot_time(figure_plots, canvas_plots, data=None):
    if data is None:
        data = []
    print('plotted time')

    data = reading_data.get_loaded_data()

    figure_plots.clear()
    subplot = figure_plots.add_subplot(1, 1, 1)
    subplot.plot(data)
    subplot.set_xlabel("Time")
    subplot.set_ylabel("Amplitude")
    canvas_plots.draw()


def plot_fft(figure_plots, canvas_plots, data=None):
    if data is None:
        data = []
    print('plotted fft')
    figure_plots.clear()


def plot_spectrogram(figure_plots, canvas_plots, data=None):
    if data is None:
        data = []
    print('plotted spectrogram')
    figure_plots.clear()
