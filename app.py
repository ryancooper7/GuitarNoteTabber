import math
import xlwt
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
from flask import Flask, render_template, request

rms_list = []
note_list = []

#list of the frequencies of notes
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
    1479.98,
    1567.98,
    1661.22,
    1760.00,
    1864.66,
    1975.53,
    2093.00,
    2217.46,
    2349.32,
    2489.02,
    2637.02,
    2793.83,
    2959.96,
    3135.96,
    3322.44,
    3520.00,
    3729.31,
    3951.07,
    4186.01,
    4434.92,
    4698.63,
    4978.03,
    5274.04,
    5587.65
]

#list of the note names corresponding to the frequencies above
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
    "F#6",
    "G6",
    "G#6",
    "A6",
    "A#6",
    "B6",
    "C7",
    "C#7",
    "D7",
    "D#7",
    "E7",
    "F7",
    "F#7",
    "G7",
    "G#7",
    "A7",
    "A#7",
    "B7",
    "C8",
    "C#8",
    "D8",
    "D#8",
    "E8",
    "F8"
]

#writes volume data to excel, used for algorithm testing
def write_vol_to_excel(data, ws):
    for i in range (0, len(data)):
        ws.write(i, 0, data[i])

#writes note data to excel
def write_notes_to_excel(data, ws):
    for i in range (0, len(data)):
        ws.write(i, 1, data[i])

#calculates RMS with standard algorithm
def calculate_rms(data):
    sum = 0
    for i in range (0, len(data)):
        sum += data[i] * data[i]
    rms = 100* (math.sqrt(sum / len(data)))
    print rms
    return rms

#Correlates note frequency to note name using binary search algorithm
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

#Changes raw sound data to integer, performs FFT, changes frequencies to Hz, and then adds
#RMS (Volume of sound) and calculated notes to lists
def AnalyzeData(data):
    int_data = np.fromstring(data, dtype = np.float32)
    rms=calculate_rms(int_data)
    processed_data = np.abs(np.fft.fft(int_data))
    frequencies = np.fft.fftfreq(len(processed_data))
    max_frequency_index = np.argmax(processed_data)
    frequency_in_hertz = abs(frequencies[max_frequency_index] * 44100)
    note = NoteFromFrequency(notes, frequency_in_hertz, start=0, end=None)
    rms_list.append(rms)
    note_list.append(note)
    return note

#takes lists of RMS and note names and determines which notes to output to user
def find_notes():
    notes = ""
    if rms_list[0] > rms_list[1] and rms_list[0] > 8:
        note_ops = rms_list[0:5]
        print note_ops
        c = Counter(note_ops)
        common_note = c.most_common(1)[0][0]
        print common_note
        if notes == "":
            notes = common_note
        else:
            notes += "  " + common_note
    for i in range(1, len(rms_list) - 1):
        if rms_list[i-1] < rms_list[i] and rms_list[i] > rms_list[i+1] and rms_list[i] > 8:
            note_ops = note_list[i:i+5]
            print note_ops
            c = Counter(note_ops)
            common_note = c.most_common(1)[0][0]
            print common_note
            if notes == "":
                notes = common_note
            else:
                notes += "  " + common_note
    if rms_list[len(rms_list)-1] > rms_list[len(rms_list)-2] and rms_list[len(rms_list) - 1] > 8:
            if notes == "":
                notes = note_list[len(rms_list) - 1]
            else:
                notes += "  " + note_list[len(rms_list) - 1]
    return notes

app = Flask(__name__)

@app.route('/<string:index>/', methods=['GET','POST'])
def my_form_post(index):
    post = 0
    if request.method == 'POST':
        if request.data == "stop":
            #notes_to_return = find_notes()
            #wb = xlwt.Workbook()
            #ws = wb.add_sheet("A Test Sheet")
            #write_vol_to_excel(rms_list, ws)
            #write_notes_to_excel(note_list, ws)
            #ws. write(0, 5, notes_to_return)
            #wb.save("writing.xls")

            notes_to_return = find_notes()
            del note_list[:]
            del rms_list[:]
            return notes_to_return
        else:
            data = request.data
            note = AnalyzeData(data)
            if post == 0:
                post = 1
                return note
            elif post == 1:
                post = 0
    else:
        return render_template('%s.html' % index)

if __name__ == "__main__":
    app.run(debug=True)
