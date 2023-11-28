import numpy as np
import matplotlib.pyplot as plt
import librosa

from pathlib import Path

song1 = Path('./7_rings.mp3')
song2 = Path('./favourite_things.mp3')
song3 = Path('./tumba_casa.mp3')


def show_spectrogram(path: Path, title: str) -> None:

    plt.clf()

    y, sr = librosa.load(path)
    D = librosa.stft(y)

    S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)

    plt.figure()
    librosa.display.specshow(S_db, x_axis='time', y_axis='log')
    plt.colorbar()
    plt.title(title)
    plt.savefig(f'{title}.png')


show_spectrogram(song1, '7 Rings')
show_spectrogram(song2, 'My Favourite Things')
show_spectrogram(song3, 'Tumba la casa mami')
