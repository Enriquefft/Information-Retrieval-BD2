"""Module for extracting audio features from audio files."""

import librosa

from pathlib import Path

import logging

import numpy as np
from numpy.typing import NDArray

from typing import Annotated, Literal, Optional

SONGS_PATH = Path('songs')

Array1D = Annotated[NDArray[np.double], Literal["N"]]
Array2D = Annotated[NDArray[np.double], Literal["N", "N"]]

SAMPLE_RATE: int = 22050


def load_audio_file(path: Path,
                    max_duration: Optional[float]) -> tuple[np.ndarray, float]:
    return librosa.load(path, sr=SAMPLE_RATE, duration=max_duration)


def MFCC(audio: np.ndarray, sr: float) -> np.ndarray:
    """Extract MFCC features from all audio files in SONGS_PATH."""
    # Compute MFCC features
    return librosa.feature.mfcc(y=audio, sr=sr)


def flatenize(mfcc: Array2D) -> Array1D:
    """Flatenize MFCC features."""
    return mfcc.flatten()


# def mean_mfcc(mfcc: Array2D) -> Array1D:
#     """Mean of MFCC features to have a 1D array."""
#     return mfcc.mean(axis=1)


def get_sample_rate() -> int:
    return SAMPLE_RATE


def get_mfcc_features_flatenized(
        song_path: Path,
        max_duration_ms: Optional[float] = None) -> np.ndarray:
    """Extract the mfcc features for each song in a path"""

    data, sr = load_audio_file(
        song_path,
        max_duration=(max_duration_ms / 1000) if max_duration_ms else None)
    mfcc = MFCC(data, sr)
    logging.info(f'Extracted MFCC features from {song_path}')
    return flatenize(mfcc)
