import os
import threading
import time
import tkinter.messagebox
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from ttkthemes import themed_tk
from PIL import ImageTk
import tkinter as tk
from mutagen.mp3 import MP3
from pygame import mixer
import wave
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

root = themed_tk.ThemedTk()
root.get_themes()  # Returns a list of all themes that can be set
root.set_theme("radiance")  # Sets an available theme

signal_wave = wave.open('Lanquidity.wav', 'r')
sample_frequency = 16000
data = np.frombuffer(signal_wave.readframes(sample_frequency), dtype=np.int16)
sig = signal_wave.readframes(-1)
sig = np.frombuffer(sig, dtype='int16')
sig = sig[:]
figure = plt.Figure(figsize=(6, 5), dpi=100)
c = figure.add_subplot(212)
Pxx, freqs, bins, im = c.specgram(sig, NFFT=1024, Fs=16000, noverlap=900)
plt.axis('off')
chart_type = FigureCanvasTkAgg(figure, root)
chart_type.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
# plt.show()

root.mainloop()