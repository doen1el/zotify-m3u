## Zotify Wrapper for m3u playlists

This is a simple wrapper for the [Zotify](https://github.com/zotify-dev/zotify) package that allows you to create an m3u playlist from a [Spotify](https://spotify.com) playlist. I was inpired by [Zotifarr](https://github.com/Xoconoch/zotifarrr).

## Disclaimer:

I don't encourage you to scrape music from Spotify. If you want to support your favourite artists, please consider buying their music or merch.

## Installation and Usage:

### 1. Clone the repository:

```
git clone https://github.com/doen1el/zotify-m3u.git
cd zotify-m3u
```

### 2. Edit the `docker-compose.yml` file:

Edit the `docker-compose.yml` file and replace the environment variables with your desired values.

```
services:
  zotify-m3u:
    image: zotify-m3u
    container_name: zotify-m3u
    volumes:
      - "/your/download/path:/app/downloads" # <-- change this mapping for your music library directory
    environment:
      - CREDENTIAL_LOCATION=/app/credentials.json
      - SONG_ARCHIVE=/app/downloads/music_archive
      - ROOT_PATH=/app/downloads
      - DOWNLOAD_FORMAT=mp3
      - DOWNLOAD_QUALITY=very_high
      - PLAYLISTS=playlist_url_1, playlist_url_2, ...
```

| Environment Variable | Description                                                        |
| -------------------- | ------------------------------------------------------------------ |
| CREDENTIAL_LOCATION  | Path to the `credential.json` file                                 |
| SONG_ARCHIVE         | Path to the directory where the list of downloaded songs is stored |
| ROOT_PATH            | Path to the directory where the downloaded songs are stored        |
| DOWNLOAD_FORMAT      | Format of the downloaded songs                                     |
| DOWNLOAD_QUALITY     | Quality of the downloaded songs                                    |
| PLAYLISTS            | List of playlists to download                                      |

### 3. Build the docker container:

Make sure that you have [docker](https://www.docker.com/) installed and running!

```
docker build -t zotify-m3u .
```

### 4. Run the docker container:

```
docker-compose up -d
```

### 5. Create your `credential.json` file:

Follow [this](https://github.com/dspearson/librespot-auth?tab=readme-ov-file) repo using a PC/laptop with spotify client installed, and once it generates the credentials.json, you need to modify it as follows:

- Replace `"auth_type": 1` with `"type":"AUTHENTICATION_STORED_SPOTIFY_CREDENTIALS"`
- Rename `"auth_data"` to `"credentials"`

Create the `credential.json` file in the `/app` directory of the container and paste the contents of the modified `credentials.json` file.

```
docker exec -it zotify-m3u bash
nano credential.json
```

### 6. Run the script:

```
docker exec -it zotify-m3u bash
python3 main.py
```

## Important Notes:

As Spotify has a download limit, you may need to run the script several times to download all the songs in the playlist.

## Acknowledgements:

This project heavily relies on [Zotify](https://github.com/zotify-dev/zotify). Thanks to the developers for their hard work!
