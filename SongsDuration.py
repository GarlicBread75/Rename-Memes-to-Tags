from mutagen.mp3 import MP3
import os


def format_time(length):
    hours = length // 3600
    length %= 3600
    mins = length // 60
    length %= 60
    seconds = length
    return f'{round(hours)}h {round(mins)}m {round(seconds)}s'

path = 'C:\\New Folder (71)\\songs\\'
min_duration = 999999
min_song = ''
max_duration = 0
max_song = ''
songs = 0
total = 0

for file in os.listdir(path):
    song = MP3(path+file)
    duration = song.info.length
    total += duration
    songs += 1
    if duration > max_duration:
        max_duration = duration
        max_song = file
    elif duration < min_duration:
        min_duration = duration
        min_song = file

print(f'Min duration: {format_time(min_duration)} - {min_song}')
print(f'Max duration: {format_time(max_duration)} - {max_song}')
print(f'Average duration: {format_time(total/songs)}')
print(f'Total duration: {format_time(total)}\n')