import math
import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt
import skimage.feature

from src.config import DEFAULT_PARAMS


def plot_constellation(audio_path, params=DEFAULT_PARAMS):
    y, sr = librosa.load(audio_path)
    length = math.floor(len(y) / sr)

    S = np.abs(
        librosa.stft(
            y,
            n_fft=params["nFFT"],
            hop_length=params["hopLength"]
        )
    )

    n_freq = S.shape[0]   
    S = S[:n_freq, :]
    n_freq, n_time = S.shape

    peaks = skimage.feature.peak_local_max(
        S,
        min_distance=params["peakMinDistance"],
        num_peaks=params["maxPeaks"] * length
    )

    peaks = peaks[np.argsort(peaks[:, 1])]
    freqs = peaks[:, 0]
    times = peaks[:, 1]

    fig, (ax1, ax2) = plt.subplots(
        2, 1, figsize=(8, 6), sharex=True
    )

    img1 = librosa.display.specshow(
        librosa.amplitude_to_db(S, ref=np.max),
        sr=sr,
        hop_length=params["hopLength"],
        y_axis="log",
        x_axis="time",
        ax=ax1
    )
    ax1.set_title("Power spectrogram")
    fig.colorbar(img1, ax=ax1, format='%+2.0f dB')

    img2 = ax2.imshow(
    np.log1p(S),
    origin="lower",
    aspect="auto",
    cmap="Greys",
    extent=[0, len(y) / sr, 0, sr / 2]
    )
    ax2.scatter(
        times * params["hopLength"] / sr,
        freqs * sr / params["nFFT"],
        color="r",
        s=12
    )
    ax2.set_title("Constellation map")
    ax2.set_ylabel("frequency (Hz)")
    ax2.set_xlabel("time (s)")

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    plot_constellation("data/sample.wav")