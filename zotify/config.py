from argparse import Namespace
from json import dump, load
from os import environ
from pathlib import Path
from sys import platform as PLATFORM
from typing import Any

from zotify.utils import AudioFormat, ImageSize, Quality

ALBUM_LIBRARY = "album_library"
ALL_ARTISTS = "all_artists"
ARTWORK_SIZE = "artwork_size"
AUDIO_FORMAT = "audio_format"
CREATE_PLAYLIST_FILE = "create_playlist_file"
CREDENTIALS_PATH = "credentials_path"
DOWNLOAD_QUALITY = "download_quality"
FFMPEG_ARGS = "ffmpeg_args"
FFMPEG_PATH = "ffmpeg_path"
LANGUAGE = "language"
LYRICS_FILE = "lyrics_file"
LYRICS_ONLY = "lyrics_only"
OUTPUT = "output"
OUTPUT_ALBUM = "output_album"
OUTPUT_PLAYLIST_TRACK = "output_playlist_track"
OUTPUT_PLAYLIST_EPISODE = "output_playlist_episode"
OUTPUT_PODCAST = "output_podcast"
OUTPUT_SINGLE = "output_single"
PATH_ARCHIVE = "path_archive"
PLAYLIST_LIBRARY = "playlist_library"
PODCAST_LIBRARY = "podcast_library"
PRINT_DOWNLOADS = "print_downloads"
PRINT_ERRORS = "print_errors"
PRINT_PROGRESS = "print_progress"
PRINT_SKIPS = "print_skips"
PRINT_WARNINGS = "print_warnings"
REPLACE_EXISTING = "replace_existing"
SAVE_METADATA = "save_metadata"
SAVE_SUBTITLES = "save_subtitles"
SKIP_DUPLICATES = "skip_duplicates"
SKIP_PREVIOUS = "skip_previous"
TRANSCODE_BITRATE = "transcode_bitrate"

SYSTEM_PATHS = {
    "win32": Path.home().joinpath("AppData/Roaming/Zotify"),
    "darwin": Path.home().joinpath("Library/Application Support/Zotify"),
    "linux": Path(environ.get("XDG_CONFIG_HOME") or "~/.config")
    .expanduser()
    .joinpath("zotify"),
}

LIBRARY_PATHS = {
    "album": Path.home().joinpath("Music/Zotify Albums"),
    "podcast": Path.home().joinpath("Music/Zotify Podcasts"),
    "playlist": Path.home().joinpath("Music/Zotify Playlists"),
}

CONFIG_PATHS = {
    "conf": SYSTEM_PATHS[PLATFORM].joinpath("config.json"),
    "creds": SYSTEM_PATHS[PLATFORM].joinpath("credentials.json"),
    "archive": SYSTEM_PATHS[PLATFORM].joinpath("track_archive"),
}

OUTPUT_PATHS = {
    "album": "{album_artist}/{album}/{track_number}. {artists} - {title}",
    "podcast": "{podcast}/{episode_number} - {title}",
    "playlist_track": "{playlist}/{artists} - {title}",
    "playlist_episode": "{playlist}/{episode_number} - {title}",
}

CONFIG_VALUES = {
    CREDENTIALS_PATH: {
        "default": CONFIG_PATHS["creds"],
        "type": Path,
        "args": ["--credentials"],
        "help": "Path to credentials file",
    },
    PATH_ARCHIVE: {
        "default": CONFIG_PATHS["archive"],
        "type": Path,
        "args": ["--archive"],
        "help": "Path to track archive file",
    },
    ALBUM_LIBRARY: {
        "default": LIBRARY_PATHS["album"],
        "type": Path,
        "args": ["--album-library"],
        "help": "Path to root of album library",
    },
    PODCAST_LIBRARY: {
        "default": LIBRARY_PATHS["podcast"],
        "type": Path,
        "args": ["--podcast-library"],
        "help": "Path to root of podcast library",
    },
    PLAYLIST_LIBRARY: {
        "default": LIBRARY_PATHS["playlist"],
        "type": Path,
        "args": ["--playlist-library"],
        "help": "Path to root of playlist library",
    },
    OUTPUT_ALBUM: {
        "default": OUTPUT_PATHS["album"],
        "type": str,
        "args": ["--output-album", "-oa"],
        "help": "File layout for saved albums",
    },
    OUTPUT_PLAYLIST_TRACK: {
        "default": OUTPUT_PATHS["playlist_track"],
        "type": str,
        "args": ["--output-playlist-track", "-opt"],
        "help": "File layout for tracks in a playlist",
    },
    OUTPUT_PLAYLIST_EPISODE: {
        "default": OUTPUT_PATHS["playlist_episode"],
        "type": str,
        "args": ["--output-playlist-episode", "-ope"],
        "help": "File layout for episodes in a playlist",
    },
    OUTPUT_PODCAST: {
        "default": OUTPUT_PATHS["podcast"],
        "type": str,
        "args": ["--output-podcast", "-op"],
        "help": "File layout for saved podcasts",
    },
    DOWNLOAD_QUALITY: {
        "default": "auto",
        "type": Quality.from_string,
        "choices": list(Quality),
        "args": ["--download-quality"],
        "help": "Audio download quality (auto for highest available)",
    },
    ARTWORK_SIZE: {
        "default": "large",
        "type": ImageSize.from_string,
        "choices": list(ImageSize),
        "args": ["--artwork-size"],
        "help": "Image size of track's cover art",
    },
    AUDIO_FORMAT: {
        "default": "vorbis",
        "type": AudioFormat.from_string,
        "choices": list(AudioFormat),
        "args": ["--audio-format"],
        "help": "Audio format of final track output",
    },
    TRANSCODE_BITRATE: {
        "default": -1,
        "type": int,
        "args": ["--bitrate"],
        "help": "Transcoding bitrate (-1 to use download rate)",
    },
    FFMPEG_PATH: {
        "default": "",
        "type": str,
        "args": ["--ffmpeg-path"],
        "help": "Path to ffmpeg binary",
    },
    FFMPEG_ARGS: {
        "default": "",
        "type": str,
        "args": ["--ffmpeg-args"],
        "help": "Additional ffmpeg arguments when transcoding",
    },
    SAVE_SUBTITLES: {
        "default": False,
        "type": bool,
        "args": ["--save-subtitles"],
        "help": "Save subtitles from podcasts to a .srt file",
    },
    LANGUAGE: {
        "default": "en",
        "type": str,
        "args": ["--language"],
        "help": "Language for metadata",
    },
    LYRICS_FILE: {
        "default": False,
        "type": bool,
        "args": ["--lyrics-file"],
        "help": "Save lyrics to a file",
    },
    LYRICS_ONLY: {
        "default": False,
        "type": bool,
        "args": ["--lyrics-only"],
        "help": "Only download lyrics and not actual audio",
    },
    CREATE_PLAYLIST_FILE: {
        "default": True,
        "type": bool,
        "args": ["--playlist-file"],
        "help": "Save playlist information to an m3u8 file",
    },
    SAVE_METADATA: {
        "default": True,
        "type": bool,
        "args": ["--save-metadata"],
        "help": "Save metadata, required for other metadata options",
    },
    ALL_ARTISTS: {
        "default": True,
        "type": bool,
        "args": ["--all-artists"],
        "help": "Add all track artists to artist tag in metadata",
    },
    REPLACE_EXISTING: {
        "default": False,
        "type": bool,
        "args": ["--replace-existing"],
        "help": "Overwrite existing files with the same name",
    },
    SKIP_PREVIOUS: {
        "default": True,
        "type": bool,
        "args": ["--skip-previous"],
        "help": "Skip previously downloaded songs",
    },
    SKIP_DUPLICATES: {
        "default": True,
        "type": bool,
        "args": ["--skip-duplicates"],
        "help": "Skip downloading existing track to different album",
    },
    PRINT_DOWNLOADS: {
        "default": False,
        "type": bool,
        "args": ["--print-downloads"],
        "help": "Print messages when a song is finished downloading",
    },
    PRINT_PROGRESS: {
        "default": True,
        "type": bool,
        "args": ["--print-progress"],
        "help": "Show progress bars",
    },
    PRINT_SKIPS: {
        "default": False,
        "type": bool,
        "args": ["--print-skips"],
        "help": "Show messages if a song is being skipped",
    },
    PRINT_WARNINGS: {
        "default": True,
        "type": bool,
        "args": ["--print-warnings"],
        "help": "Show warnings",
    },
    PRINT_ERRORS: {
        "default": True,
        "type": bool,
        "args": ["--print-errors"],
        "help": "Show errors",
    },
}


class Config:
    __config_file: Path | None
    album_library: Path
    artwork_size: ImageSize
    audio_format: AudioFormat
    credentials_path: Path
    download_quality: Quality
    ffmpeg_args: str
    ffmpeg_path: str
    language: str
    lyrics_file: bool
    output_album: str
    output_podcast: str
    output_playlist_track: str
    output_playlist_episode: str
    playlist_library: Path
    podcast_library: Path
    print_progress: bool
    replace_existing: bool
    save_metadata: bool
    transcode_bitrate: int

    def __init__(self, args: Namespace | None = None):
        jsonvalues = {}
        if args is not None and args.config:
            self.__config_file = Path(args.config)
            # Valid config file found
            if self.__config_file.exists():
                with open(self.__config_file, "r", encoding="utf-8") as conf:
                    jsonvalues = load(conf)
            # Remove config file and make a new one
            else:
                self.__config_file.parent.mkdir(parents=True, exist_ok=True)
                jsonvalues = {}
                for key in CONFIG_VALUES:
                    if CONFIG_VALUES[key]["type"] in [str, int, bool]:
                        jsonvalues[key] = CONFIG_VALUES[key]["default"]
                    else:
                        jsonvalues[key] = str(CONFIG_VALUES[key]["default"])
                with open(self.__config_file, "w+", encoding="utf-8") as conf:
                    dump(jsonvalues, conf, indent=4)
        else:
            self.__config_file = None

        for key in CONFIG_VALUES:
            # Override config with commandline arguments
            if args is not None and key in vars(args) and vars(args)[key] is not None:
                setattr(self, key, self.__parse_arg_value(key, vars(args)[key]))
            # If no command option specified use config
            elif key in jsonvalues:
                setattr(self, key, self.__parse_arg_value(key, jsonvalues[key]))
            # Use default values for missing keys
            else:
                setattr(
                    self,
                    key,
                    self.__parse_arg_value(key, CONFIG_VALUES[key]["default"]),
                )

        # "library" arg overrides all *_library options
        if args is not None and args.library:
            self.album_library = Path(args.library).expanduser().resolve()
            self.playlist_library = Path(args.library).expanduser().resolve()
            self.podcast_library = Path(args.library).expanduser().resolve()

        # "output" arg overrides all output_* options
        if args is not None and args.output:
            self.output_album = args.output
            self.output_podcast = args.output
            self.output_playlist_track = args.output
            self.output_playlist_episode = args.output

    @staticmethod
    def __parse_arg_value(key: str, value: Any) -> Any:
        config_type = CONFIG_VALUES[key]["type"]
        if type(value) is config_type:
            return value
        elif config_type == Path:
            return Path(value).expanduser().resolve()
        elif config_type == AudioFormat.from_string:
            return AudioFormat.from_string(value)
        elif config_type == ImageSize.from_string:
            return ImageSize.from_string(value)
        elif config_type == Quality.from_string:
            return Quality.from_string(value)
        else:
            raise TypeError("Invalid Type: " + value)

    def get(self, key: str) -> Any:
        """
        Gets a value from config
        Args:
            key: config attribute to return value of
        Returns:
            Value of key
        """
        return getattr(self, key)
