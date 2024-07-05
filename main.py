import string
import os
import csv
from sclib import SoundcloudAPI, Track, Playlist


def clear_string(data):
    valid_chars = "-_.() abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    ret = ""
    for i in data:
        if i in valid_chars:
            ret += i
    return ret.replace("/", "")


def download(track: Track, folder_name=None):
    filename = f'{track.artist} - {track.title}.mp3'

    name = clear_string(filename)
    path = "./songs/"
    if folder_name is not None:
        path = path + folder_name + "/"
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

    # Add entry to the database
    add_to_db("Song", path, track.permalink_url)


def add_to_db(type, path, url):
    with open('./songs/db.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow([type, path, url])


def create_db():
    if not os.path.exists('./songs/db.csv'):
        with open('./songs/db.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            writer.writerow(["Type", "Path", "URL"])


def main(url):
    api = SoundcloudAPI()
    dwn = api.resolve(url)

    if not os.path.exists("./songs"):
        os.mkdir("./songs")

    if isinstance(dwn, Playlist):
        playlist: Playlist = dwn
        folder_name = clear_string(playlist.title)
        add_to_db("Playlist", f"./songs/{folder_name}", url)
        j = 0
        length = len(playlist)
        for i in playlist:
            print("Downloading " + str(j) + "/" + str(length) + ":   " + i.title)
            download(i, folder_name=folder_name)
            j += 1

    elif isinstance(dwn, Track):
        if not os.path.exists("./songs/solo-tracks"):
            os.mkdir(path="./songs/solo-tracks")

        download(dwn, folder_name="solo-tracks")
    else:
        exit(1)


def restore():
    api = SoundcloudAPI()
    with open('./songs/db.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            if row['Type'] == 'Playlist':
                dwn = api.resolve(row['URL'])
                if isinstance(dwn, Playlist):
                    playlist: Playlist = dwn
                    folder_name = clear_string(playlist.title)
                    j = 0
                    length = len(playlist)
                    for i in playlist:
                        print("Downloading " + str(j) + "/" + str(length) + ":   " + i.title)
                        download(i, folder_name=folder_name)
                        j += 1
            elif row['Type'] == 'Song':
                dwn = api.resolve(row['URL'])
                if isinstance(dwn, Track):
                    download(dwn, folder_name="solo-tracks")


if __name__ == "__main__":
    create_db()
    working = True

    while working:
        mode = input("Select mode (1: Download, 2: Restore) or press enter to exit:\n")
        if mode == '1':
            tmp = input("Paste the Song / Playlist URL here or press enter to exit:\n")
            if len(tmp) <= 10:
                working = False
                continue
            main(tmp)
        elif mode == '2':
            restore()
        else:
            working = False