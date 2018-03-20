import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import audioop

class AudioStream:
    notes = [
        65.41,
        69.30,
        73.42,
        77.78,
        82.41,
        87.31,
        92.50,
        98.00,
        103.83,
        110.00,
        116.54,
        123.47,
        130.81,
        138.59,
        146.83,
        155.56,
        164.81,
        174.61,
        185.00,
        196.00,
        207.65,
        220.00,
        233.08,
        246.94,
        261.63,
        277.18,
        293.66,
        311.13,
        329.63,
        349.23,
        369.99,
        392.00,
        415.30,
        440.00,
        466.16,
        493.88,
        523.25,
        554.37,
        587.33,
        622.25,
        659.25,
        698.46,
        739.99,
        783.99,
        830.61,
        880.00,
        932.33,
        987.77,
        1046.50,
        1108.73,
        1174.66,
        1244.51,
        1318.51,
        1396.91,
        1479.98
    ]

    note_names = [
        "C2",
        "C#2",
        "D2",
        "D#2",
        "E2",
        "F2",
        "F#2",
        "G2",
        "G#2",
        "A2",
        "A#2",
        "B2",
        "C3",
        "C#3",
        "D3",
        "D#3",
        "E3",
        "F3",
        "F#3",
        "G3",
        "G#3",
        "A3",
        "A#3",
        "B3",
        "C4",
        "C#4",
        "D4",
        "D#4",
        "E4",
        "F4",
        "F#4",
        "G4",
        "G#4",
        "A4",
        "A#4",
        "B4",
        "C5",
        "C#5",
        "D5",
        "D#5",
        "E5",
        "F5",
        "F#5",
        "G5",
        "G#5",
        "A5",
        "A#5",
        "B5",
        "C6",
        "C#6",
        "D6",
        "D#6",
        "E6",
        "F6",
        "F#6"
    ]

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

            rms = audioop.rms(data, 2)

            #changes binary data into integer data with amplitude on y axis and time on x axis
            int_data = np.fromstring(data, dtype = np.int16)
            processed_data = np.abs(np.fft.fft(int_data))
            frequencies = np.fft.fftfreq(len(processed_data))
            counter = counter + 1


            max_frequency_index = np.argmax(processed_data)
            frequency_in_hertz = abs(frequencies[max_frequency_index] * self.RATE)
            note = self.NoteFromFrequency(self.notes, frequency_in_hertz,start = 0, end=None)
            print counter, frequency_in_hertz, note, rms
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
        #plt.show()

    def NoteFromFrequency(self, arr, frequency, start=0, end=None):
        if end is None:
            end = len(arr) - 1

        lowermid = (start + end) / 2
        highermid = lowermid + 1

        if lowermid == len(arr)-1:
            return self.note_names[lowermid]
        if frequency >= arr[lowermid] and frequency <= arr[highermid]:
            if abs(frequency - arr[lowermid]) <= abs(frequency-arr[highermid]):
                return self.note_names[lowermid]
            else:
                return self.note_names[highermid]
        if frequency < arr[lowermid]:
            return self.NoteFromFrequency(arr, frequency, start, lowermid - 1)
        return self.NoteFromFrequency(arr, frequency, highermid+1, end)

if __name__ == '__main__':
    s = AudioStream()