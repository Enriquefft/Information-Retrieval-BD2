"""Module for downloading a Spotify playlist using the Spotify API or a csv."""

from pytube import YouTube, Search, Stream  # type: ignore
from pytube.exceptions import AgeRestrictedError, LiveStreamError  # type: ignore

import youtube_dl  # type: ignore

from spotipy import Spotify  # type: ignore
from spotipy.oauth2 import SpotifyClientCredentials  # type: ignore

from typing import Final, Optional, Generator, Iterable, cast

from pathlib import Path

from csv import reader

import logging

from psycopg2.extensions import connection, cursor

from os import getenv

# Set up credentials
client_id: Final[str] = '5b0ac652d91f4d2a89f62f99d568cd34'
client_secret: Final[str] = 'b450d640d4f44a13928f7725475a270b'

client_credentials_manager = SpotifyClientCredentials(
    client_id=client_id, client_secret=client_secret)
sp: Spotify = Spotify(client_credentials_manager=client_credentials_manager)

BASE_OUTPUT_PATH: Final[Path] = Path("songs/")

from enum import Enum


class DownloadMethod(Enum):
    """Enum for the download method."""
    YOUTUBE_DL = 1
    PYTUBE = 2


class Downloader():
    """Class for downloading a Spotify playlist."""

    def __init__(self, dl_method: DownloadMethod, csv_path: Optional[Path],
                 playlist_id: Optional[str], userFavourites: bool,
                 db: connection):
        """Initialize a Downloader object."""

        # Only one of csv_path and playlist_id should be set
        if sum([csv_path is not None, playlist_id is not None,
                userFavourites]) != 1:
            raise ValueError(
                "Only one of csv_path, playlist_id, and userFavourites should be set"
            )

        self.output_path: Path
        if csv_path is not None:
            self.get_method = self.get_songs_by_csv
            self.output_path = BASE_OUTPUT_PATH
        elif playlist_id is not None:
            self.get_method = self.get_songs_by_playlist
            self.output_path = BASE_OUTPUT_PATH / playlist_id
        elif userFavourites:
            self.get_method = self.get_songs_by_favourites
            self.output_path = BASE_OUTPUT_PATH / 'favourites'

        if dl_method == DownloadMethod.YOUTUBE_DL:
            self.download_method = self.download_song_youtube_dl
        elif dl_method == DownloadMethod.PYTUBE:
            self.download_method = self.download_song_pytube

        self.playlist_id: str | None = playlist_id
        self.userFavourites: bool = userFavourites
        self.csv_path: Optional[Path] = csv_path

        self.db: connection = db

    def exists_in_db(self, track_id: str) -> bool:
        """Check if a song exists in the database."""
        cur: cursor
        with self.db.cursor() as cur:
            cur.execute(
                f"SELECT EXISTS(SELECT 1 FROM {getenv('TABLE_NAME')} WHERE track_id=%s)",
                (track_id, ))
            exists = cur.fetchone()
            if exists is None:
                raise ValueError("exists is None")
            return cast(bool, exists[0])

    def get_songs_by_csv(self) -> Generator[tuple[str, str, str], None, None]:
        """Get a list of [trackid, songname, artist] from a Spotify playlist."""

        if self.csv_path is None:
            raise ValueError("csv_path is None")

        with open(self.csv_path, 'r') as file:

            csv_reader = reader(file)
            headers = next(csv_reader)  # Skip the header row

            track_id_index = headers.index('track_id')
            track_name_index = headers.index('track_name')
            track_artist_index = headers.index('track_artist')

            # Advance to the first row whose track_id is not in the database
            # logging.info("Searching the first row not inserted yet.")
            while True:
                row = next(csv_reader)
                if not self.exists_in_db(row[track_id_index]):
                    # logging.info(f"Found first row: {row[track_name_index]}")
                    yield (row[track_id_index], row[track_name_index],
                           row[track_artist_index])
                    break

            for row in csv_reader:
                yield (row[track_id_index], row[track_name_index],
                       row[track_artist_index])

    def get_songs_by_playlist(
            self) -> Generator[tuple[str, str, str], None, None]:
        """Get a list of [trackid, songname, artist_name] from a Spotify playlist."""

        return ((item['track']['id'], item['track']['name'],
                 item['track']['artists'][0]['name'])
                for item in sp.playlist_tracks(self.playlist_id)['items'])

    def get_songs_by_favourites(
            self) -> Generator[tuple[str, str, str], None, None]:
        """Get a list of [trackid, songname, artist_name] from a Spotify playlist."""
        return ((item['track']['id'], item['track']['name'],
                 item['track']['artists'][0]['name'])
                for item in sp.playlist(self.playlist_id)['tracks']['items'])

    def download_song_youtube_dl(self, song: tuple[str, str,
                                                   str]) -> Path | None:
        """Download a song audio by searching its name on yt.

        @param song: A tuple of [track_id, song_name, artist_name]
        @return: The path to the downloaded song
        """
        try:
            ydl_opts = {
                'default_search': 'ytsearch',
                'format': 'bestaudio/best',
                'outtmpl': f'{self.output_path}/{song[0]}.%(ext)s',
                'quiet': True,
                'no_warnings': True,
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(f"ytsearch:{song[1]}",
                                             download=False)
                audio_url = info_dict['entries'][0]['webpage_url']
                pprint(info_dict['entries'])
                if audio_url is None:
                    logging.warning(
                        f"Could not find an audio URL for {song[1]}")
                    return None
                ydl.download([audio_url])
                return Path(f'{self.output_path}/{song[0]}.{info_dict["ext"]}')
        except youtube_dl.utils.DownloadError as e:
            return None

    def download_song_pytube(self, song: tuple[str, str, str]) -> Path | None:
        """Download a song audio by searching its name on yt.

        @param song: A tuple of [track_id, song_name, artist_name]
        @return: The path to the downloaded song
        """
        try:
            search_query = f""""{song[1]}" {song[2]}"""
            yt_results: YouTube = Search(search_query).results

            if len(yt_results) == 0:
                logging.warning(
                    f"Could not find a video for search query: {search_query}")
                return None
            stream = yt_results[0].streams.get_audio_only()
            if stream is None:
                logging.warning(
                    f"Could not find an mp4 audio stream for {song[1]}")
                return None

            return Path(
                stream.download(output_path=self.output_path,
                                filename=song[0]))
        except (AgeRestrictedError, LiveStreamError) as e:
            return None

    def download_songs(self) -> Generator[Path, None, None]:
        """Download a song b its name."""

        for song in self.get_method():
            song_path = self.download_method(song)
            if song_path is not None:
                yield song_path
