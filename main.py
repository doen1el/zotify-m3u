import subprocess
import os
from dotenv import load_dotenv
from datetime import datetime
import schedule
import time

load_dotenv()

def download_playlist(url):
    print("Environment variables:")
    print("SONG_ARCHIVE:", os.getenv("SONG_ARCHIVE"))
    print("ROOT_PATH:", os.getenv("ROOT_PATH"))
    print("DOWNLOAD_FORMAT:", os.getenv("DOWNLOAD_FORMAT"))
    print("DOWNLOAD_QUALITY:", os.getenv("DOWNLOAD_QUALITY"))
    print("PLAYLISTS:", os.getenv("PLAYLISTS"))
    
    # zotify command (username, password, song archive path, root path, download format, download quality, print downloads, download lyrics, url)
    command = ["zotify", "--credentials-location", os.getenv("CREDENTIAL_LOCATION"), "--song-archive", os.getenv("SONG_ARCHIVE"), "--root-path", os.getenv("ROOT_PATH"), "--download-format", os.getenv("DOWNLOAD_FORMAT"), "--download-quality", os.getenv("DOWNLOAD_QUALITY"), "--print-downloads", "True", "--download-lyrics", "False", url]

    # start the subprocess
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # wait until the process is finished and fetch the output
    stdout, stderr = process.communicate()
    
    print("OUTPUT: ", stdout)
    print("ERROR: ", stderr)

    # check if the subprocess was successfull
    if process.returncode != 0:
        print(f"Error while downloading the playlist: {stderr.decode()}")
    else:
        print(f"Playlist was downloaded successfuly: {stdout.decode()}")
        
def create_playlists(root_directory):
    # check if the root directory exits
    if not os.path.exists(root_directory):
        print("The root directory doesnt exists")
        return

    # check if the root directory is a directory
    if not os.path.isdir(root_directory):
        print("The root directory isnt a valid directory")
        return

    for dirpath, dirnames, _ in os.walk(root_directory):
        for dirname in dirnames:
            # create the playlist file
            playlist_name = dirname + ".m3u"
            playlist_path = os.path.join(dirpath, dirname, playlist_name)

            # open the playlist file with write permission
            with open(playlist_path, "w") as playlist_file:
                # search for every mp3 file in the directory
                for _, _, files in os.walk(os.path.join(dirpath, dirname)):
                    for file in files:
                        if file.endswith(".mp3"):
                            # write the file path to the playlist
                            playlist_file.write(os.path.join(file) + "\n")

            print(f"playlist '{playlist_name}' was created.")
    
def download_and_create_playlists():
    print(f"Running script at {datetime.now()}")
    # loop through each playlist string and download the playlist
    for playlist in os.getenv("PLAYLISTS").split(', '):
        print(playlist)
        download_playlist(playlist)
        
    # create playlists in the music folder
    create_playlists(os.getenv("ROOT_PATH"))
    

if __name__ == "__main__":
    print("Starting the zotify script")
    download_and_create_playlists()
    
    schedule.every().day.at("01:00").do(download_and_create_playlists)

    while True:
        schedule.run_pending()
        time.sleep(60)