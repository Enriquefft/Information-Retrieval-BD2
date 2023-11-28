from typing import Final, cast, Callable, Any
from pathlib import Path

from librosa import load
from librosa.feature import mfcc, chroma_vqt, spectral_contrast
from librosa.beat import beat_track

import numpy as np
from math import sqrt, log2, pow

max_duration_seconds: Final[float] = 50

favourite_mp3_path: Final[Path] = Path("./favourite_things.mp3")
_7_rings_mp3_path: Final[Path] = Path("./7_rings.mp3")
tumba_casa_mp3_path: Final[Path] = Path("./tumba_casa.mp3")

data_fav, sr_fav = load(favourite_mp3_path)
data_7, sr_7 = load(_7_rings_mp3_path)
data_tumba, sr_tumba = load(tumba_casa_mp3_path)

vector_dimension: Final[int] = 60_000


def mfcc_features(data: np.ndarray, sr: float) -> np.ndarray:
    """Extract the mfcc features for each song in a path"""

    features = mfcc(y=data, sr=sr)
    return features.flatten()


def rythm_spectral_features(data: np.ndarray,
                            sr: float) -> tuple[np.ndarray, np.ndarray, float]:

    # Extract spectral features
    spectral_features = spectral_contrast(y=data, sr=sr)

    # Extract rhythm features
    beat, rhythmic_features = beat_track(y=data, sr=sr)

    # Flatten the spectral features into a single dimension vector
    spectral_vector = spectral_features.flatten()

    # Concatenate the spectral and rhythmic vectors
    return spectral_vector, rhythmic_features, beat


def normalize(features: np.ndarray, limit: int) -> np.ndarray:
    # truncate or pad to limit
    if features.shape[0] > limit:
        features = features[:limit]

    if features.shape[0] < limit:
        # Repeat the last row until the dimension is the same
        features = np.pad(features, (0, limit - features.shape[0]), 'edge')
    return features


def feature_extractor(data: np.ndarray, sr: float) -> np.ndarray:
    """Extract the mfcc features for a song."""
    return np.ndarray(0)


def euclidean_distance(x: np.ndarray, y: np.ndarray) -> float:
    """Compute the euclidean distance between two vectors"""
    return sqrt(np.sum((x - y)**2))


# def cosine_distance(x: np.ndarray, y: np.ndarray) -> float:
#     """Compute the cosine distance between two vectors"""
#     return 1 - np.dot(x, y) / (np.linalg.norm(x) * np.linalg.norm(y))


def test(
    extraction_function: Callable[[np.ndarray, float], Any],
    comparison_function: Callable[[np.ndarray, np.ndarray],
                                  float] = euclidean_distance
) -> None:

    spectral_fav, rythmic_fav, beat_fav = extraction_function(data_fav, sr_fav)
    spectral_7, rythmic_7, beat_7 = extraction_function(data_7, sr_7)
    spectral_tumba, rythmic_tumba, beat_tumba = extraction_function(
        data_tumba, sr_tumba)

    # Normalize the features
    spectral_fav = normalize(spectral_fav, 50_000)
    spectral_7 = normalize(spectral_7, 50_000)
    spectral_tumba = normalize(spectral_tumba, 50_000)

    rythmic_fav = normalize(rythmic_fav, 200)
    rythmic_7 = normalize(rythmic_7, 200)
    rythmic_tumba = normalize(rythmic_tumba, 200)

    # distances
    spectral_distance_fav_7 = comparison_function(spectral_fav, spectral_7)
    spectral_distance_fav_tumba = comparison_function(spectral_fav,
                                                      spectral_tumba)
    spectral_distance_7_tumba = comparison_function(spectral_7, spectral_tumba)

    rythmic_distance_fav_7 = comparison_function(rythmic_fav, rythmic_7)
    rythmic_distance_fav_tumba = comparison_function(rythmic_fav,
                                                     rythmic_tumba)
    rythmic_distance_7_tumba = comparison_function(rythmic_7, rythmic_tumba)

    # Means
    fav_7_mean = (spectral_distance_fav_7 + rythmic_distance_fav_7) / 2
    fav_tumba_mean = (spectral_distance_fav_tumba +
                      rythmic_distance_fav_tumba) / 2
    _7_tumba_mean = (spectral_distance_7_tumba + rythmic_distance_7_tumba) / 2

    # Print results
    print("spectral distance between favourite things and 7 rings: ",
          spectral_distance_fav_7, rythmic_distance_fav_7, fav_7_mean)
    print("spectral distance between favourite things and tumba casa: ",
          spectral_distance_fav_tumba, rythmic_distance_fav_tumba,
          fav_tumba_mean)
    print("spectral distance between 7 rings and tumba casa: ",
          spectral_distance_7_tumba, rythmic_distance_7_tumba, _7_tumba_mean)

    # print("distance between features of favourite things and 7 rings: ",
    #       comparison_function(features_fav, features_7))
    # print("distance between features of favourite things and tumba casa: ",
    #       comparison_function(features_fav, features_tumba))
    # print("distance between features of 7 rings and tumba casa: ",
    #       comparison_function(features_7, features_tumba))


test(rythm_spectral_features)
