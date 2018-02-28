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
        plot_data = self.stream.read(self.CHUNK)
        plot_int_data = np.fromstring(plot_data, dtype=np.int16)
        fig, ax = plt.subplots()
        ax.plot(plot_int_data, '-')
        plt.xlabel("Sample Number")
        plt.ylabel("Amplitude")
        plt.title("Sound Wave")
        plt.show()
        plt.close('all')

if __name__ == '__main__':
    AudioStream()