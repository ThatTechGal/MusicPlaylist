# MusicPlaylist

Add songs function - The add_songs() function utilizes the filedialog.askopenfilenames() method to open a file dialog window where the user can select multiple files. The title parameter sets the title of the dialog window to "Select Songs", and the filetypes parameter restricts the selectable files to those with an .mp3 extension. The filedialog.askopenfilenames() method returns a list of file paths that the user has selected.

Once the user has selected the songs, the function iterates over each file path in the songs list. For each song, it calls the playlist.insert(END, song) method to add the song to the playlist. Here, playlist is presumably a listbox widget from a GUI library like Tkinter, and END is a constant that indicates the new item should be added at the end of the listbox.


Play songs function - This function uses the pygame library to handle the music playback and the threading library to manage concurrent operations. The function begins by setting a global variable is_playing to True and retrieves the path of the current song from the playlist using the current_song_index. The playlist.get method is used to fetch the song path from a listbox widget.

The function then attempts to load and play the song using pygame.mixer.music.load and pygame.mixer.music.play methods. If successful, it updates a label widget (song_label) to display the name of the currently playing song by extracting the file name from the song path. Additionally, the function calls load_song_duration to retrieve and display the duration of the song. This function uses the MP3 class from the mutagen library to get the length of the audio file and updates a progress bar widget to reflect the song's duration. The total duration is formatted in minutes and seconds and displayed on a label widget (time_label).

To ensure the progress bar updates in real-time, the function starts a new thread that runs the update_progress_bar function. This is done using the threading.Thread class, which allows the progress bar to be updated concurrently with the music playback without blocking the main thread. If any exception occurs during the loading or playing of the song, an error message is displayed using the messagebox.showerror function from the tkinter library.

The relevant function implementations provided include methods for retrieving values from variables, loading audio files, playing audio, and handling threading operations. The get method retrieves the value of a variable, while the load and play methods from the pygame.mixer.music module handle loading and playing audio files, respectively. The load_song_duration function calculates the duration of the song and updates the progress bar and time label accordingly. The start method from the threading.Thread class initiates a new thread, ensuring that it runs only once per thread object. Finally, the showerror function from the tkinter.messagebox module displays an error message dialog.


Load song duration function - The function takes a single argument, song_path, which is the file path to the MP3 file. Inside the function, an instance of the MP3 class is created by passing the song_path to it. This instance, audio, contains metadata about the MP3 file, including its duration.

The duration of the song is accessed through the audio.info.length attribute, which returns the length of the song in seconds. This duration is then used to set the maximum value of a progress bar, presumably part of a graphical user interface (GUI), to the song's duration. This allows the progress bar to accurately reflect the playback progress of the song.

Next, the function converts the total duration from seconds into minutes and seconds using the divmod function. The divmod function takes two arguments and returns a tuple containing the quotient and the remainder. In this case, it divides the total duration by 60 to get the number of minutes and the remaining seconds. The minutes and seconds are then formatted into a string in the "MM:SS" format.

Finally, the function updates a label in the GUI, time_label, to display the formatted duration string. The label shows the current playback time (initialized to "00:00") and the total duration of the song. This provides a clear and user-friendly way to display the song's duration and playback progress.

The MP3 class, as described in the relevant class declarations, is part of the mutagen library and is used to handle MPEG audio files. It provides various attributes and methods to access and manipulate the metadata of MP3 files. The divmod function, which is a built-in Python function, is used here to perform integer division and modulus operations simultaneously, making it convenient for converting seconds into a more readable minutes and seconds format.


Update progress bar function - The function runs in a loop as long as a song is playing (is_playing is True) and the music mixer is busy (pygame.mixer.music.get_busy() returns True). Within the loop, it retrieves the current playback position in milliseconds using pygame.mixer.music.get_pos() and converts it to seconds by dividing by 1000. This value is then assigned to the progress bar's value attribute.

The function also converts the current playback time and the total duration of the song (assumed to be the maximum value of the progress bar) into a MM:SS format using the divmod function, which divides the time in seconds by 60 to get minutes and seconds. These formatted times are then displayed on a time_label widget using the config method. The loop pauses for one second between updates using time.sleep(1) to avoid excessive CPU usage.

When the song stops playing, the progress bar is reset to zero, and the time label is cleared. The function then calls play_next_song to start playing the next song in the playlist. The play_next_song function increments the current_song_index and calls play_song to play the next song if there are more songs in the playlist.

The relevant function implementations provided include get_busy, which checks if the music mixer is busy, and get_pos, which retrieves the current playback position. The divmod function is used to calculate minutes and seconds from the total seconds. The sleep function pauses the execution for a specified number of seconds. The play_next_song function handles transitioning to the next song in the playlist.

The class declarations for int show the various methods and properties available for integer objects in Python, including arithmetic operations, bitwise operations, and conversions. These details are not directly related to the update_progress_bar function but provide context for the divmod function and integer manipulations used in the code.


