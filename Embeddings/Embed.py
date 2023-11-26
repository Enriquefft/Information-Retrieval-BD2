"""Module for extracting audio features from audio files."""

# from memory_profiler import profile
import librosa

from pathlib import Path

import logging

import numpy as np
from numpy.typing import NDArray

from typing import Annotated, Literal, Optional

import logging


class Embedder():

    def __init__(self,
                 sample_rate: int = 22050,
                 max_duration_seconds: Optional[float] = None):
        self.sample_rate = sample_rate
        self.max_duration_seconds = max_duration_seconds

    def get_mfcc_features_flatenized(self, song_path: Path) -> np.ndarray:
        """Extract the mfcc features for each song in a path"""

        data, sr = librosa.load(song_path,
                                sr=self.sample_rate,
                                duration=self.max_duration_seconds)
        mfcc = librosa.feature.mfcc(y=data, sr=sr)
        chroma_cqt = librosa.feature.chroma_vqt(y=data, sr=sr)
        return mfcc.flatten()
