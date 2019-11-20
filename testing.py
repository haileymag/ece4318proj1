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

root = themed_tk.ThemedTk()
root.get_themes()  # Returns a list of all themes that can be set
root.set_theme("radiance")  # Sets an available theme

# root = Tk()

statusBar = ttk.Label(root, text="Music Player 1.0", relief=SUNKEN, anchor=W, font='Helvetia 10 italic')
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
    tkinter.messagebox.showinfo('About Music Player', 'For ECE 4318')


subMenu = Menu(menuBar, tearoff=0)
menuBar.add_cascade(label="Help", menu=subMenu)
subMenu.add_command(label="About Us", command=about_us)

mixer.init()  # initializing the mixer

root.geometry('300x380')
root.title("Music Player 1.0")
root.iconbitmap(r"images/music.ico")
photo = ImageTk.PhotoImage( file = r"images/play.png")
Button(root, text="play", image = photo).pack( side = TOP)
# theres a

root.mainloop()