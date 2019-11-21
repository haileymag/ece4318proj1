import os

import threading
import time
import tkinter.messagebox
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter import *
from tkinter.ttk import *
from ttkthemes import themed_tk as tk
from PIL import ImageTk
import platform
from CollapsablePane import CollapsiblePane as clp
from mutagen.mp3 import MP3
from pygame import mixer
import wave
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt


root = tk.ThemedTk()
root.get_themes()  # Returns a list of all themes that can be set
if platform.system() == "Darwin":
    root.set_theme("aqua")
else:
    root.set_theme("black")  # Sets an available theme

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
    add_to_playlist(filename_path)

    mixer.music.queue(filename_path)


def add_to_playlist(filename):
    filename = os.path.basename(filename)
    index = 0
    playlistBox.insert(index, filename)
    playlist.insert(index, filename_path)
    index += 1


menuBar.add_cascade(label="File", menu=subMenu)
subMenu.add_command(label="Open", command=browse_file)
subMenu.add_command(label="Exit", command=root.destroy)


def about_us():
    tkinter.messagebox.showinfo('Music Player 1.0', 'For ECE 4318')


subMenu = Menu(menuBar, tearoff=0)
menuBar.add_cascade(label="Help", menu=subMenu)
subMenu.add_command(label="About Us", command=about_us)

mixer.init()  # initializing the mixer

root.title("Music Player")
root.iconbitmap(r"images/music.ico")

# Root Window - StatusBar, LeftFrame, RightFrame
# LeftFrame - The listbox (playlist)
# RightFrame - TopFrame,MiddleFrame and the BottomFrame

leftFrame = Frame(root)
leftFrame.pack(side=LEFT, padx=30, pady=30)


playlistBox = Listbox(leftFrame)
playlistBox.pack()

addBtn = ttk.Button(leftFrame, text="+ Add", command=browse_file)
addBtn.pack(side=LEFT)

cPane = clp(root, 'item', ['1'])
cPane.pack(side="top", fill="x")


def del_song():
    selected_song = playlistBox.curselection()
    selected_song = int(selected_song[0])
    playlistBox.delete(selected_song)
    playlist.pop(selected_song)


delBtn = ttk.Button(leftFrame, text="- Del", command=del_song)
delBtn.pack(side=LEFT)

rightFrame = Frame(root)
rightFrame.pack(pady=30)

topFrame = Frame(rightFrame)
topFrame.pack()
currentTimeLabel = ttk.Label(topFrame, text='')
currentTimeLabel.pack(side=LEFT, pady = 5)
lengthLabel = ttk.Label(topFrame, text='--:--')
lengthLabel.pack(side=LEFT, pady = 5)




def show_details(play_song):
    file_data = os.path.splitext(play_song)

    if file_data[1] == '.mp3':
        audio = MP3(play_song)
        total_length = audio.info.length
    else:
        a = mixer.Sound(play_song)
        total_length = a.get_length()
        if file_data[1] == '.wav':
            signal_wave = wave.open(play_song, "r")
            sample_frequency = 16000
            data = np.fromstring(signal_wave.readframes(sample_frequency), dtype=np.int16)
            sig = signal_wave.readframes(-1)
            sig = np.fromstring(sig, 'Int16')
            sig = sig[:]
            plt.figure(1)
            a = plt.subplot(211)
            plt.plot(sig)
            c = plt.subplot(212)
            Pxx, freqs, bins, im = c.specgram(sig, NFFT=1024, Fs=16000, noverlap=900)
            plt.show()

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
            statusBar['text'] = "Playing music" + ' - ' + os.path.basename(play_it)
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


def mute_music():
    global muted
    if muted:  # Unmute the music
        mixer.music.set_volume(0.7)
        volumeBtn.configure(image=volumePhoto)
        scale.set(70)
        muted = FALSE
    else:  # mute the music
        mixer.music.set_volume(0)
        volumeBtn.configure(image=mutePhoto)
        scale.set(0)
        muted = TRUE


middleFrame = Frame(rightFrame)
middleFrame.pack(pady=30, padx=30)

playPhoto = ImageTk.PhotoImage(file=r"images/play.png")
playBtn = ttk.Button(middleFrame, image=playPhoto, command=play_music)
playBtn.grid(row=0, column=0, padx=10)

stopPhoto = ImageTk.PhotoImage(file=r"images/stop.png")
stopBtn = ttk.Button(middleFrame, image=stopPhoto, command=stop_music)
stopBtn.grid(row=0, column=1, padx=10)

pausePhoto = ImageTk.PhotoImage(file=r"images/pause.png")
pauseBtn = ttk.Button(middleFrame, image=pausePhoto, command=pause_music)
pauseBtn.grid(row=0, column=2, padx=10)

# Bottom Frame for volume, rewind, mute etc.

bottomFrame = Frame(rightFrame)
bottomFrame.pack()

rewindPhoto = ImageTk.PhotoImage(file=r"images/rewind.png")
rewindBtn = ttk.Button(bottomFrame, image=rewindPhoto, command=rewind_music)
rewindBtn.grid(row=0, column=0)

mutePhoto = ImageTk.PhotoImage(file=r"images/mute.png")
volumePhoto = ImageTk.PhotoImage(file=r"images/unmute.png")
volumeBtn = ttk.Button(bottomFrame, image=volumePhoto, command=mute_music)
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
# <div>Icons made by <a href="https://www.flaticon.com/authors/smashicons" title="Smashicons">Smashicons</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>
# <div>Icons made by <a href="https://www.flaticon.com/authors/smashicons" title="Smashicons">Smashicons</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>

