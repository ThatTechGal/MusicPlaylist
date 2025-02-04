# MusicPlaylist

pygame: This library is used to handle music playback.
tkinter: This is Python's standard library for building GUIs.
filedialog: Allows the user to open a file dialog to select songs.
messagebox: Used for showing error messages (e.g., when a song can't be played).
Listbox, ttk: Used for creating a listbox and progress bar in the GUI.
mutagen.mp3: This is used to extract metadata (like the duration) from MP3 files.
time: Provides functionality for time-related operations (like updating the song's progress).
threading: Used to run the progress bar updates in a separate thread.

Functions:

def add_songs():
    songs = filedialog.askopenfilenames(title="Select Songs", filetypes=(("mp3 Files", "*.mp3"),))
    for song in songs:
        playlist.insert(END, song)
This function opens a file dialog where users can select one or more MP3 files. The selected songs' paths are added to the playlist (which is a Listbox widget).

def play_song():
    global is_playing
    is_playing = True
    song_path = playlist.get(ACTIVE)
    try:
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play()
        song_label.config(text=f"Playing: {song_path.split('/')[-1]}")
        load_song_duration(song_path)
        threading.Thread(target=update_progress_bar).start()
    except Exception as e:
        messagebox.showerror("Error", f"Could not play the song: {e}")
play_song() is triggered when the user clicks the play button.
It loads the song selected from the playlist (playlist.get(ACTIVE)) using pygame.mixer and starts playing.
The song title is displayed in the song_label.
The song's duration is loaded using the load_song_duration() function, and a new thread is started to update the progress bar.

def load_song_duration(song_path):
    audio = MP3(song_path)
    song_duration = audio.info.length
    progress_bar['maximum'] = song_duration
    total_minutes, total_seconds = divmod(int(song_duration), 60)
    time_label.config(text=f"00:00 / {total_minutes:02}:{total_seconds:02}")
load_song_duration() uses the mutagen library to get the song's duration in seconds.
It sets the maximum value of the progress bar to match the song duration and updates the time_label with the song's total duration.

def update_progress_bar():
    while is_playing and pygame.mixer.music.get_busy():
        current_time = pygame.mixer.music.get_pos() / 1000
        progress_bar['value'] = current_time
        current_minutes, current_seconds = divmod(int(current_time), 60)
        total_minutes, total_seconds = divmod(int(progress_bar['maximum']), 60)
        time_label.config(text=f"{current_minutes:02}:{current_seconds:02} / {total_minutes:02}:{total_seconds:02}")
        time.sleep(1)
    progress_bar['value'] = 0
    time_label.config(text="")
update_progress_bar() continuously updates the progress bar and the time_label while the song is playing.
It checks if the song is still playing using pygame.mixer.music.get_busy().
The song's current position is retrieved using pygame.mixer.music.get_pos().
The progress bar value is updated and the current time in MM:SS format is shown in time_label.

def pause_song():
    global is_playing
    pygame.mixer.music.pause()
    is_playing = False
Pauses the song when the pause button is clicked and updates the is_playing flag.

def resume_song():
    global is_playing
    pygame.mixer.music.unpause()
    is_playing = True
    threading.Thread(target=update_progress_bar).start()
Resumes playback when the resume button is clicked and restarts the progress bar updates in a separate thread.

def stop_song():
    global is_playing
    pygame.mixer.music.stop()
    is_playing = False
    song_label.config(text="Music Stopped")
    progress_bar['value'] = 0
    time_label.config(text="")
Stops the song when the stop button is clicked and resets the progress bar and the time_label.

Creating the GUI

Window Initialization:
root = Tk()
root.title("Music Player with Playlist and Progress Bar")
root.geometry("500x450")

Creates the main window using Tkinter with the title and a fixed size.
Widgets:
song_label: Displays the current song playing or a message like "No song playing".
playlist: A Listbox widget used to show the list of songs.
progress_bar: A Progressbar widget to show the progress of the song.
time_label: A label that shows the current and total song time in MM:SS format.
controls_frame: A frame that contains the control buttons: Play, Pause, Resume, and Stop.
add_button: A button to add songs to the playlist.

