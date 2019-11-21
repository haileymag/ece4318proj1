import os
import math
import random
import threading
import time
import codecs
import tkinter.messagebox
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter import *
from tkinter.ttk import *
from ttkthemes import themed_tk as tk
import platform
from mutagen.mp3 import MP3
from pygame import mixer
import wave
import numpy as np
import time
import matplotlib.pyplot as plt

root = tk.ThemedTk()
root.get_themes()  # Returns a list of all themes that can be set
if platform.system() == "Darwin":
    root.set_theme("aqua")
else:
    root.set_theme("black")  # Sets an available theme
    root.iconbitmap(r'icon.ico')

statusBar = ttk.Label(root, text="Welcome to Music Player 1.0", relief=SUNKEN, anchor=W, font='Arial 10')
statusBar.pack(side=BOTTOM, fill=X)

# Create the menubar
menuBar = Menu(root)
root.config(menu=menuBar)
# Create the submenu

subMenu = Menu(menuBar, tearoff=0)

playlist = []


# playlist - contains the full path + filename
# playlistbox - contains just the filename
# Fullpath + filename is required to play the music inside play_music load function


def browse_file():
    global filename_path
    filename_path = filedialog.askopenfilename()
    file_ext = os.path.splitext(filename_path)[1]
    if (file_ext == ".m3u8"):
        m3u8 = codecs.open(filename_path, "r", "utf-8")
        for line in m3u:
            if (os.path.isfile(line.rstrip())):
                add_to_playlist(line.rstrip())
        m3u8.close()
    else:
        print(filename_path)
        add_to_playlist(filename_path)
        mixer.music.queue(filename_path)


def add_to_playlist(filename):
    # filename = os.path.basename(filename)
    index = 0
    playlistBox.insert(index, os.path.basename(filename))
    playlist.insert(index, filename)
    index += 1


def shuffle_playlist():
    playlistBox.delete(0, END)
    for idx in range(len(playlist)):
        r = math.floor(random.random() * (idx + 1))
        swap = playlist[r]
        playlist[r] = playlist[idx]
        playlist[idx] = swap

    for idx, song in enumerate(playlist):
        playlistBox.insert(idx, os.path.basename(song))


def save_playlist():
    filename_save_path = filedialog.asksaveasfilename(title="Save playlist as",
                                                      filetypes=(("M3U8 Playlist", "*.m3u8"), ("all files", "*.*")))
    m3u8 = codecs.open(os.path.splitext(filename_save_path)[0] + ".m3u8", "w",
                       "utf-8")  # can save files with utf-8 characters
    for song in playlist:
        m3u.write(song.replace("/", "\\") + "\n")
    m3u8.close()


menuBar.add_cascade(label="File", menu=subMenu)
subMenu.add_command(label="Open", command=browse_file)
subMenu.add_command(label="Save Playlist", command=save_playlist)
subMenu.add_command(label="Exit", command=root.destroy)


def about_us():
    tkinter.messagebox.showinfo('Music Player 1.0', 'For ECE 4318')


subMenu = Menu(menuBar, tearoff=0)
menuBar.add_cascade(label="Help", menu=subMenu)
subMenu.add_command(label="About Us", command=about_us)

mixer.init()  # initializing the mixer

root.title("Music Player")
root.resizable(False, False)

# Root Window - StatusBar, LeftFrame, RightFrame
# LeftFrame - The listbox (playlist)
# RightFrame - TopFrame,MiddleFrame and the BottomFrame

leftFrame = Frame(root)
leftFrame.pack(side=LEFT, padx=30, pady=30)

playlistBox = Listbox(leftFrame)
playlistBox.pack()

addBtn = ttk.Button(leftFrame, text=u"\u256C", command=browse_file)
addBtn.pack(side=LEFT)


def del_song():
    selected_song = playlistBox.curselection()
    selected_song = int(selected_song[0])
    playlistBox.delete(selected_song)
    playlist.pop(selected_song)


delBtn = ttk.Button(leftFrame, text=u"\u2550", command=del_song)
delBtn.pack(side=LEFT)

shufBtn = ttk.Button(leftFrame, text="Shuffle", command=shuffle_playlist)
shufBtn.pack(side=LEFT)

rightFrame = Frame(root)
rightFrame.pack(pady=30, padx= 30)

topFrame = Frame(rightFrame)
topFrame.pack()
currentTimeLabel = ttk.Label(topFrame, text='')
currentTimeLabel.pack(side=LEFT, pady=5)
lengthLabel = ttk.Label(topFrame, text='--:--')
lengthLabel.pack(side=LEFT, pady=5)


def show_details(play_song):
    file_data = os.path.splitext(play_song)

    if file_data[1] == '.mp3':
        audio = MP3(play_song)
        total_length = audio.info.length
    elif file_data[1] == '.wav':
        a = mixer.Sound(play_song)
        total_length = a.get_length()
        signal_wave = wave.open(play_song, 'r')
        sample_frequency = 16000
        data = np.frombuffer(signal_wave.readframes(sample_frequency), dtype=np.int16)
        sig = signal_wave.readframes(-1)
        sig = np.frombuffer(sig, dtype='int16')
        sig = sig[:]
        c = plt.subplot(212)
        Pxx, freqs, bins, im = c.specgram(sig, NFFT=1024, Fs=16000, noverlap=900)
        plt.axis('off')
        plt.show()
        time.sleep(10)
        plt.close()

    else:
        a = mixer.Sound(play_song)
        total_length = a.get_length()
    # div - total_length/60, mod - total_length % 60
    mins, secs = divmod(total_length, 60)
    mins = round(mins)
    secs = round(secs)
    timeFormat = '{:02d}:{:02d}'.format(mins, secs)
    lengthLabel['text'] = timeFormat

    t1 = threading.Thread(target=start_count, args=(total_length,))
    t1.start()


def start_count(t):
    global paused
    # mixer.music.get_busy(): - Returns FALSE when we press the stop button (music stop playing)
    # Continue - Ignores all of the statements below it. We check if music is paused or not.
    current_time = 0
    while current_time <= t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, secs = divmod(current_time, 60)
            mins = round(mins)
            secs = round(secs)
            timeFormat = '{:02d}:{:02d}'.format(mins, secs)
            currentTimeLabel['text'] = timeFormat + '/'
            time.sleep(1)
            current_time += 1


def play_music():
    global paused

    if paused:
        mixer.music.unpause()
        statusBar['text'] = "Music Resumed"
        paused = FALSE
    else:
        try:
            stop_music()

            time.sleep(1)
            selected_song = playlistBox.curselection()
            selected_song = int(selected_song[0])
            play_it = playlist[selected_song]
            mixer.music.load(play_it)
            mixer.music.play()
            statusBar['text'] = "Playing " + ' - ' + os.path.basename(play_it)
            show_details(play_it)
        except:
            tkinter.messagebox.showerror('File not found', 'Music Player could not find the file. Please check again.')


def stop_music():
    mixer.music.stop()
    statusBar['text'] = "Music Stopped"


paused = FALSE


def pause_music():
    global paused
    paused = TRUE
    mixer.music.pause()
    statusBar['text'] = "Music Paused"


def rewind_music():
    play_music()
    statusBar['text'] = "Rewinding..."


def set_vol(val):
    volume = float(val) / 100
    mixer.music.set_volume(volume)
    # set_volume of mixer takes value only from 0 to 1. Example - 0, 0.1,0.55,0.54.0.99,1


muted = FALSE
prevVolume = 0.7


def mute_music():
    global muted, prevVolume
    if muted:  # Unmute the music
        mixer.music.set_volume(prevVolume)
        scale.set(prevVolume * 100)
        muted = FALSE
    else:  # mute the music
        prevVolume = mixer.music.get_volume()
        mixer.music.set_volume(0)
        scale.set(0)
        muted = TRUE


middleFrame = Frame(rightFrame)
middleFrame.pack(pady=30, padx=30)

stopBtn = ttk.Button(middleFrame, text=u"\u25A2", command=stop_music)
stopBtn.grid(row=0, column=0, padx=10)

playBtn = ttk.Button(middleFrame, text=u"\u25B7", command=play_music)
playBtn.grid(row=0, column=1, padx=10)

pauseBtn = ttk.Button(middleFrame, text=u"\u259A", command=pause_music)
pauseBtn.grid(row=0, column=2, padx=10)

# Bottom Frame for volume, rewind, mute etc.

bottomFrame = Frame(rightFrame)
bottomFrame.pack()

rewindBtn = ttk.Button(bottomFrame, text=u"\u25C1", command=rewind_music)
rewindBtn.grid(row=0, column=0)

volumeBtn = ttk.Button(bottomFrame, text=u"\u259F", command=mute_music)
volumeBtn.grid(row=0, column=1)

scale = ttk.Scale(bottomFrame, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
scale.set(70)  # implement the default value of scale when music player starts
mixer.music.set_volume(0.7)
scale.grid(row=0, column=2, pady=15, padx=30)


def on_closing():
    stop_music()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()

