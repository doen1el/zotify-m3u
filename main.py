import subprocess
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

class SpotifyDownloader:
    def __init__(self):
        self.credential_location = os.getenv("CREDENTIAL_LOCATION")
        self.song_archive = os.getenv("SONG_ARCHIVE")
        self.root_path = os.getenv("ROOT_PATH")
        self.download_format = os.getenv("DOWNLOAD_FORMAT")
        self.download_quality = os.getenv("DOWNLOAD_QUALITY")
        self.playlists = os.getenv("PLAYLISTS")

    def download_playlist(self, playlist_url):
        """
        Downloads a playlist from the given URL using the zotify command.
        Args:
            playlist_url (str): The URL of the playlist to download.
        Prints:
            The status of the download process, including any output or errors from the zotify command.
        Raises:
            RuntimeError: If the download process fails.
        """
        print(f"Downloading playlist: {playlist_url}")
        
        # zotify command (username, password, song archive path, root path, download format, download quality, print downloads, download lyrics, url)
        command = ["zotify", "--credentials-locatio", self.credential_location,  "--song-archive", self.song_archive, "--root-path", self.root_path, "--download-format", self.download_format, "--download-quality", self.download_quality, "--skip-existing", "True", "--skip-previously-downloaded", "True", playlist_url]

        # start the subprocess
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # wait until the process is finished and fetch the output
        stdout, stderr = process.communicate()

        # check if the subprocess was successfull
        if process.returncode != 0:
            print(f"Error while downloading the playlist: {stderr.decode()}")
        else:
            print(f"Playlist was downloaded successfuly: {stdout.decode()}")
        
    def create_playlists(self):
        """
        Creates playlists for each subdirectory in the root directory.
        This method checks if the root directory exists and is a valid directory.
        For each subdirectory, it creates a playlist file with the same name as the
        subdirectory and a .m3u extension. The playlist file contains the paths of
        all .mp3 files in the subdirectory.
        Returns:
            None
        """
        # check if the root directory exits
        if not os.path.exists(self.root_path):
            print("The root directory doesnt exists")
            return

        # check if the root directory is a directory
        if not os.path.isdir(self.root_path):
            print("The root directory isnt a valid directory")
            return

        for dirpath, dirnames, _ in os.walk(self.root_path):
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
    
    def download_and_create_playlists(self):
        """
        Downloads playlists from URLs specified in the environment variable "PLAYLISTS" 
        and creates playlists in the music folder.
        This method performs the following steps:
        1. Prints the current date and time.
        2. Loops through each playlist URL specified in the "PLAYLISTS" environment variable,
           downloading each playlist.
        3. Creates playlists in the music folder.
        Environment Variables:
        - PLAYLISTS: A comma-separated string of playlist URLs to be downloaded.
        Returns:
        None
        """
        print(f"Running script at {datetime.now()}")
        # loop through each playlist string and download the playlist
        for playlist_url in os.getenv("PLAYLISTS").split(', '):
            self.download_playlist(playlist_url)
            
        # create playlists in the music folder
        self.create_playlists()
        
    def print_environment_variables(self):
        """
        Prints the current environment variables and checks for the existence of the credential file.
        This method prints the following environment variables:
        - SONG_ARCHIVE
        - ROOT_PATH
        - DOWNLOAD_FORMAT
        - DOWNLOAD_QUALITY
        - PLAYLISTS
        It also checks if the credential file exists at the specified location. If the file does not exist,
        it returns a FileNotFoundError with the appropriate message.
        Returns:
            FileNotFoundError: If the credential file is not found at the specified location.
        """
        print("Environment variables:")
        print("SONG_ARCHIVE:", self.song_archive)
        print("ROOT_PATH:", self.root_path)
        print("DOWNLOAD_FORMAT:", self.download_format)
        print("DOWNLOAD_QUALITY:", self.download_quality)
        print("PLAYLISTS:", self.playlists)
        credential_location = self.credential_location
        if not credential_location or not os.path.exists(credential_location):
            return FileNotFoundError(f"Credential file not found: {credential_location}")
        else:
            print(f"Credential file found: {credential_location}")

if __name__ == "__main__":
    downloader = SpotifyDownloader()
    downloader.print_environment_variables()
    print("------------------------------------")
    print("Starting the zotify script")
    downloader.download_and_create_playlists()