"""Module for extracting audio features from audio files."""

# from memory_profiler import profile
import librosa

from pathlib import Path

import logging

import numpy as np
from numpy.typing import NDArray

from typing import Annotated, Literal, Optional

import logging

from enum import Enum


class Method(Enum):
    mfcc = 1
    contrast = 2


class Embedder():

    def __init__(self,
                 sample_rate: int = 22050,
                 max_duration_seconds: Optional[float] = None,
                 method: Method = Method.contrast):
        self.sample_rate = sample_rate
        self.max_duration_seconds = max_duration_seconds
        self.method = method

    def get_features(self, song_path: Path) -> np.ndarray:
        """Extract the mfcc features for each song in a path"""

        data, sr = librosa.load(song_path,
                                sr=self.sample_rate,
                                duration=self.max_duration_seconds)
        match self.method:
            case Method.mfcc:
                mfcc = librosa.feature.mfcc(y=data, sr=sr)
                return mfcc.flatten()
            case Method.contrast:
                spectral_features = librosa.feature.spectral_contrast(y=data,
                                                                      sr=sr)
                return spectral_features.flatten()
