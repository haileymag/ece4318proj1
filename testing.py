from ttkthemes import themed_tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
import wave


root = themed_tk.ThemedTk()
root.get_themes()  # Returns a list of all themes that can be set
root.set_theme("radiance")  # Sets an available theme


signal_wave = wave.open('Lanquidity.wav', 'r')
sample_frequency = 16000


data = np.frombuffer(signal_wave.readframes(sample_frequency), dtype=np.int16)
sig = signal_wave.readframes(-1)
sig = np.frombuffer(sig, dtype='int16')
sig = sig[:]
c = plt.subplot(212)

Pxx, freqs, bins, im = c.specgram(sig, NFFT=1024, Fs=16000, noverlap=900)
plt.axis('off')
plt.show()

root.mainloop()