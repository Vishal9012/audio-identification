import math
import numpy as np
import librosa
import skimage.feature

def compute_fingerprint(path, params):
    """
    Compute fingerprint for an audio file.
    Returns a dictionary mapping frequency bins to time indices.
    """
    y, sr = librosa.load(path)
    length = math.floor(len(y) / sr)

    S = np.abs(
        librosa.stft(
            y,
            n_fft=params["nFFT"],
            hop_length=params["hopLength"]
        )
    )

    peaks = skimage.feature.peak_local_max(
        S,
        min_distance=params["peakMinDistance"],
        num_peaks=params["maxPeaks"] * length
    )

    peaks = peaks[np.argsort(peaks[:, 1])]

    hashes = {}
    for freq_bin in range(params["nFFT"]):
        times = peaks[np.nonzero(peaks[:, 0] == freq_bin), 1]
        if len(times) > 0:
            hashes[freq_bin] = np.asarray(times, dtype=int)

    return hashes
