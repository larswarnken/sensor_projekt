import gui
import reading_data
import numpy as np
from scipy import signal
from scipy.fft import fftfreq
from scipy.fft import fft
import matplotlib
import matplotlib.pyplot as plt


def plot_time(figure_plots, canvas_plots, data=None):
    if data is None:
        data = []

    data = reading_data.get_loaded_data()

    figure_plots.clear()
    subplot = figure_plots.add_subplot(1, 1, 1)
    subplot.plot(data)
    subplot.set_xlabel("Time")
    subplot.set_ylabel("Amplitude")

    canvas_plots.draw()

    if not data:
        subplot.set_xlim(0, 10)
        subplot.set_ylim(-1, 1)
    else:
        # sample_rate = reading_data.get_loaded_sample_rate()
        # time = reading_data.get_loaded_record_time()
        #
        # labels = [item.get_text() for item in subplot.get_xticklabels()]
        #
        # print(labels)
        # for i in range(len(labels)):
        #     if '−' not in labels[i]:
        #         print(labels[i])
        #         new_label = round(int(labels[i])/sample_rate)
        #         labels[i] = new_label
        #
        # subplot.set_xticklabels(labels)

        plt.show()

        canvas_plots.draw()


def plot_fft(figure_plots, canvas_plots, data=None):
    if data is None:
        data = []
    figure_plots.clear()

    loaded_data = reading_data.get_loaded_data()
    loaded_sample_rate = reading_data.get_loaded_sample_rate()

    if len(loaded_data) != 0:
        time = []

        # Construct a time signal
        fs = loaded_sample_rate  # Sampling freq
        tstep = 1 / fs  # sample time interval

        for x in range(len(loaded_data)):
            time.append(x * tstep)

        time_interval = len(time) * tstep

        # perform fft
        t = time_interval  # entire time
        n = len(loaded_data)
        t = np.linspace(0, t, n)
        dt = np.diff(t)[0]

        f = fftfreq(len(t), np.diff(t)[0])
        # fftfreq: Calculate the frequencies corresponding to
        # the FFT bins in the result returned by fft.
        y_fft = fft(loaded_data)

        figure_plots.clear()
        subplot = figure_plots.add_subplot(1, 1, 1)
        subplot.plot(f[:n // 2], np.abs(y_fft[:n // 2]))
        subplot.set_xlim(0, fs / 2)
        subplot.set_xlabel("Frequency (Hz)")
        subplot.set_ylabel("Amplitude")
        canvas_plots.draw()

        # zuerst die idx von max. Amplitude in y_FFT zu finden
        m_fft_idx = 0
        max_amplitude = 0
        for currtFFT in y_fft:
            if np.abs(currtFFT) > max_amplitude:
                m_fft_idx = np.where(y_fft == currtFFT)[0][0]
                max_amplitude = np.abs(currtFFT)

        # label_test_value7.configure(text=f'{max_amplitude}')
        # label_test_value8.configure(text=f'{f[:n // 2][m_fft_idx]}')
    else:
        figure_plots.clear()
        subplot = figure_plots.add_subplot(1, 1, 1)
        subplot.set_xlabel("Frequency (Hz)")
        subplot.set_ylabel("Amplitude")
        canvas_plots.draw()


def plot_spectrogram(figure_plots, canvas_plots, data=None):
    if data is None:
        data = []
    figure_plots.clear()

    loaded_data = reading_data.get_loaded_data()
    loaded_sample_rate = reading_data.get_loaded_sample_rate()

    if len(loaded_data) != 0:

        spectorgram_data_T = transform_to_spectrogram()
        # Transposed matrix

        # fig, axes = plt.subplots(1, 1, figsize=(8, 6))
        # p = axes.imshow(spectorgram_data_T, origin='lower',
        #                 extent=(0, len(loaded_data) / Fs, 0, Fs / 2),
        #                 aspect='auto',
        #                 cmap=matplotlib.cm.RdBu_r)
        # cb = fig.colorbar(p, ax=axes)
        # cb.set_label("$\log|F|$", fontsize=16)
        #
        # fig.tight_layout()
        #
        # plt.show()

        figure_plots.clear()
        subplot_one = figure_plots.add_subplot(1, 1, 1)
        # subplot_two = figure_plots.add_subplot(1, 2, 2)

        subplot_one.imshow(spectorgram_data_T, origin='lower',
                           extent=(0, len(loaded_data) / loaded_sample_rate, 0, loaded_sample_rate / 2),
                           aspect='auto',
                           cmap=matplotlib.cm.RdBu_r)

        subplot_one.set_xlabel("Time (s)")
        subplot_one.set_ylabel("Frequency (Hz)")

        # figure_plots.colorbar(subplot_one, ax=subplot_two)

        canvas_plots.draw()

    else:
        figure_plots.clear()
        subplot_one = figure_plots.add_subplot(1, 1, 1)
        subplot_one.set_xlabel("Time (s)")
        subplot_one.set_ylabel("Frequency (Hz)")
        canvas_plots.draw()


def transform_to_spectrogram():
    loaded_data = reading_data.get_loaded_data()
    loaded_sample_rate = reading_data.get_loaded_sample_rate()

    N = int(loaded_sample_rate / 150.0)
    f = fftfreq(N, 1.0 / loaded_sample_rate)
    t = np.linspace(0, 0.1, N)
    mask = (f > 0) * (f < loaded_sample_rate / 2)

    subdata = loaded_data[:N]
    F = fft(subdata)

    n_max = int(len(loaded_data) / N)
    f_values = np.sum(mask)
    spectorgram_data = np.zeros((n_max, f_values))

    window = signal.windows.blackman(len(subdata))

    for n in range(0, n_max):
        subdata = loaded_data[(N * n):(N * (n + 1))]
        F = fft(subdata * window)
        spectorgram_data[n, :] = np.log(abs(F[mask]))

    spectorgram_data_T = spectorgram_data.T

    return spectorgram_data_T
