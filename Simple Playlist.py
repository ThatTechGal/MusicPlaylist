import pygame
from tkinter import *
from tkinter import filedialog, messagebox, Listbox, ttk
from mutagen.mp3 import MP3
import time
import threading

# Initialize pygame mixer
pygame.mixer.init()

# Global variable to track if song is playing
is_playing = False
current_song_index = 0  # To track the current song in the playlist

# Function to add songs to the playlist
def add_songs():
    songs = filedialog.askopenfilenames(title="Select Songs", filetypes=(("mp3 Files", "*.mp3"),))
    for song in songs:
        playlist.insert(END, song)  # Add each song path to the playlist listbox

# Function to load and play the selected song from the playlist
def play_song():
    global is_playing, current_song_index
    is_playing = True
    song_path = playlist.get(current_song_index)  # Get the song from the listbox using current_song_index
    try:
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play()
        song_label.config(text=f"Playing: {song_path.split('/')[-1]}")
        # Get and display the song duration
        load_song_duration(song_path)
        # Start the progress bar update in a separate thread
        threading.Thread(target=update_progress_bar).start()
    except Exception as e:
        messagebox.showerror("Error", f"Could not play the song: {e}")

# Function to get song duration using mutagen
def load_song_duration(song_path):
    audio = MP3(song_path)
    song_duration = audio.info.length  # Duration in seconds
    progress_bar['maximum'] = song_duration  # Set max length of progress bar
    # Update the total duration in MM:SS format
    total_minutes, total_seconds = divmod(int(song_duration), 60)
    time_label.config(text=f"00:00 / {total_minutes:02}:{total_seconds:02}")

# Function to update the progress bar as the song plays
def update_progress_bar():
    while is_playing and pygame.mixer.music.get_busy():
        current_time = pygame.mixer.music.get_pos() / 1000  # Get current time in seconds
        progress_bar['value'] = current_time
        # Convert current time to MM:SS format
        current_minutes, current_seconds = divmod(int(current_time), 60)
        total_minutes, total_seconds = divmod(int(progress_bar['maximum']), 60)
        time_label.config(text=f"{current_minutes:02}:{current_seconds:02} / {total_minutes:02}:{total_seconds:02}")
        time.sleep(1)
    progress_bar['value'] = 0  # Reset progress bar if song stops
    time_label.config(text="")
    play_next_song()  # Play the next song when the current one finishes

# Function to pause the song
def pause_song():
    global is_playing
    pygame.mixer.music.pause()
    is_playing = False

# Function to resume the song
def resume_song():
    global is_playing
    pygame.mixer.music.unpause()
    is_playing = True
    threading.Thread(target=update_progress_bar).start()

# Function to stop the song
def stop_song():
    global is_playing
    pygame.mixer.music.stop()
    is_playing = False
    song_label.config(text="Music Stopped")
    progress_bar['value'] = 0  # Reset progress bar
    time_label.config(text="")

# Function to play the next song in the playlist
def play_next_song():
    global current_song_index
    if current_song_index + 1 < playlist.size():
        current_song_index += 1
        play_song()

# Function to play the previous song in the playlist
def play_previous_song():
    global current_song_index
    if current_song_index - 1 >= 0:
        current_song_index -= 1
        play_song()

# Create the Tkinter window
root = Tk()
root.title("Music Player with Playlist and Progress Bar")
root.geometry("550x550")

# Song Label
song_label = Label(root, text="No song playing", font=("Helvetica", 12))
song_label.pack(pady=10)

# Playlist Listbox
playlist = Listbox(root, selectmode=SINGLE, bg="black", fg="white", width=60, height=10)
playlist.pack(pady=10)

# Progress bar
progress_bar = ttk.Progressbar(root, orient=HORIZONTAL, length=300, mode='determinate')
progress_bar.pack(pady=5)

# Time label to show current time and duration in MM:SS format
time_label = Label(root, text="", font=("Helvetica", 10))
time_label.pack(pady=5)

# Control Buttons
controls_frame = Frame(root)
controls_frame.pack(pady=10)

play_button = Button(controls_frame, text="Play", width=10, command=play_song)
play_button.grid(row=0, column=0, padx=5)

pause_button = Button(controls_frame, text="Pause", width=10, command=pause_song)
pause_button.grid(row=0, column=1, padx=5)

resume_button = Button(controls_frame, text="Resume", width=10, command=resume_song)
resume_button.grid(row=0, column=2, padx=5)

stop_button = Button(controls_frame, text="Stop", width=10, command=stop_song)
stop_button.grid(row=0, column=3, padx=5)

next_button = Button(controls_frame, text="Next", width=10, command=play_next_song)  # Next button
next_button.grid(row=0, column=4, padx=5)

prev_button = Button(controls_frame, text="Previous", width=10, command=play_previous_song)  # Previous button
prev_button.grid(row=0, column=5, padx=5)

# Add Songs Button
add_button = Button(root, text="Add Songs", command=add_songs)
add_button.pack(pady=10)

# Run the Tkinter main loop
root.mainloop()

