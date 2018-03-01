import pyaudio
import numpy as np
import matplotlib.pyplot as plt

class AudioStream:
    def __init__(self):
        #buffer size
        self.CHUNK = 4096

        #samples per second
        self.RATE = 44100

        #Number of seconds to record
        self.RECORD_SECONDS = 5

        #creates audio stream using the Pyaudio library and then calls the analyze function
        p = pyaudio.PyAudio()
        self.stream = p.open(format=pyaudio.paInt16, channels=1, rate=self.RATE, input=True,
                        frames_per_buffer=self.CHUNK)
        self.AnalyzeData()

    #Fills enough buffers corresponding to record time, changes data from binary to integer,
    #calculates Fourier Transform on data, and then print's out frequency of microphone sound
    def AnalyzeData(self):
        counter = 0

        # RATE / CHUNK corresponds to the number of buffers filled
        for i in range(int(self.RECORD_SECONDS * self. RATE / self.CHUNK)): #record for RECORD_SECONDS

            #reads in binary data
            data = self.stream.read(self.CHUNK)

            #changes binary data into integer data with amplitude on y axis and time on x axis
            int_data = np.fromstring(data, dtype = np.int16)
            processed_data = np.abs(np.fft.fft(int_data))
            frequencies = np.fft.fftfreq(len(processed_data))
            counter = counter + 1


            max_frequency_index = np.argmax(processed_data)
            frequency_in_hertz = abs(frequencies[max_frequency_index] * self.RATE)
            print counter, frequency_in_hertz
        self.PlotData()

    def PlotData(self):
        #Generates one additional data point to plot
        plot_data = self.stream.read(self.CHUNK)
        plot_int_data = np.fromstring(plot_data, dtype=np.int16)
        f, ax = plt.subplots(2)

        x = np.arange(10000)
        y = np.random.randn(10000)

        #This plot shows the integer sound wave data
        li, = ax[0].plot(x, y)
        ax[0].set_xlim(0, self.CHUNK)
        ax[0].set_ylim(-3000, 3000)
        ax[0].set_title("Sound Wave")
        ax[0].set_xlabel("Number of Samples")
        ax[0].set_ylabel("Amplitude")
        li.set_xdata(np.arange(len(plot_int_data)))
        li.set_ydata(plot_int_data)

        #This plot shows the transformed data, converted into decibels
        li2, = ax[1].plot(x, y)
        ax[1].set_xlim(0, 2000)
        ax[1].set_ylim(0, 100)
        ax[1].set_title("Fourier Transform")
        ax[1].set_xlabel("Frequency (Hz)")
        ax[1].set_ylabel("Strength (Db)")

        #converts fourier transformed data into decibels
        fourier_plot_data = 10 * np.log10(abs(np.fft.fft(plot_int_data)))
        li2.set_xdata(np.arange(len(fourier_plot_data)) * 10)
        li2.set_ydata(fourier_plot_data)

        #Makes sure plots don't overlap
        plt.tight_layout()
        plt.show()

if __name__ == '__main__':
    AudioStream()