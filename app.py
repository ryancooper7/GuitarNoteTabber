import math
import audioop
import numpy as np
from flask import Flask, render_template, request

rms_list = []
note_list = []

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

def NoteFromFrequency(arr, frequency, start=0, end=None):
    if end is None:
        end = len(arr) - 1

    lowermid = (start + end) / 2
    highermid = lowermid + 1

    if lowermid == len(arr) - 1:
        return note_names[lowermid]
    if frequency >= arr[lowermid] and frequency <= arr[highermid]:
        if abs(frequency - arr[lowermid]) <= abs(frequency - arr[highermid]):
            return note_names[lowermid]
        else:
            return note_names[highermid]
    if frequency < arr[lowermid]:
        return NoteFromFrequency(arr, frequency, start, lowermid - 1)
    return NoteFromFrequency(arr, frequency, highermid + 1, end)

def AnalyzeData(data):
    rms = audioop.rms(data,2)
    print rms

    int_data = np.fromstring(data, dtype = np.float32)
    processed_data = np.abs(np.fft.fft(int_data))
    frequencies = np.fft.fftfreq(len(processed_data))
    max_frequency_index = np.argmax(processed_data)
    frequency_in_hertz = abs(frequencies[max_frequency_index] * 44100)
    note = NoteFromFrequency(notes, frequency_in_hertz, start=0, end=None)
    return note



app = Flask(__name__)

@app.route('/<string:index>/', methods=['GET','POST'])
def my_form_post(index):
    if request.method == 'POST':
        data = request.data
        note = AnalyzeData(data)
        return note
    else:
        return render_template('%s.html' % index)

if __name__ == "__main__":
    app.run(debug=True)
