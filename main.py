import string
import os
from sclib import SoundcloudAPI, Track, Playlist

def main(url):

    def clear_string(data):
        valid_chars = "-_.() abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        ret = ""
        for i in data:
            if i in valid_chars:
                ret += i
        return ret.replace("/", "")

    api = SoundcloudAPI()  
    dwn = api.resolve(url)

    def download(track: Track, folder_name = None):
        filename = f'{track.artist} - {track.title}.mp3'

        name = clear_string(filename)
        path  = "./songs/" 
        if folder_name is not None:
            path  = path + folder_name + "/"
        if not os.path.exists(path):
            os.mkdir(path=path)

        path = path + name
        if os.path.exists(path):
            return
        with open(path, 'wb+') as file:
            try:
                track.write_mp3_to(file)
            except Exception as e:
                return

    if not os.path.exists("./songs"):
        os.mkdir("./songs")

    if type(dwn) == Playlist:
        playlist: Playlist= dwn
        folder_name = clear_string(playlist.title)
        j = 0
        length = len(playlist)
        for i in playlist:
            print("Downloading " + str(j) + "/" + str(length) +":   " +   i.title)
            download(i, folder_name=folder_name)
            j += 1

    elif type(dwn) == Track:
        if not os.path.exists("./songs/solo-tracks"):
            os.mkdir(path="./songs/solo-tracks")

        download(dwn, folder_name="solo-tracks")
    else:
        exit(1)

if __name__ == "__main__":
    working = True
    
    while working:
        tmp = input("Past the Song / Playlist here or press enter to exit:\n")
        if len(tmp) <= 10:
            working = False
            continue
        main(tmp)