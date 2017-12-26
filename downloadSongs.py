import os
import subprocess

def youtubeDlSongs(songIds):
    os.chdir("/mnt/c/dev/song-uploader/songs")
    for id in songIds:
        os.system("youtube-dl -f 140 https://www.youtube.com/watch?v="+ id)

