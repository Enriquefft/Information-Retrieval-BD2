"""Module for extracting audio features from audio files."""

import librosa

from pathlib import Path

import logging

import numpy as np

SONGS_PATH = Path('songs')


def load_audio_file(path: Path) -> tuple[np.ndarray, float]:
    return librosa.load(path)


def MFCC(audio: np.ndarray, sr: float) -> np.ndarray:
    """Extract MFCC features from all audio files in SONGS_PATH."""
    # Compute MFCC features
    return librosa.feature.mfcc(y=audio, sr=sr)


def flatenize(mfcc: np.ndarray) -> np.ndarray:
    """Flatenize MFCC features."""
    return mfcc.flatten()


def get_mfcc_features(song_path: Path) -> np.ndarray:
    """Extract the mfcc features for each song in a path"""

    data, sr = load_audio_file(song_path)
    mfcc = MFCC(data, sr)
    logging.info(f'Extracted MFCC features from {song_path}')
    return flatenize(mfcc)
