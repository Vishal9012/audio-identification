## Audio Identification using Spectral Fingerprinting

This project implements an audio identification system inspired by
constellation-map-based fingerprinting techniques.

### Features
- STFT-based peak extraction
- Hash-based fingerprinting
- Inverted index matching
- Accuracy evaluation on query datasets

### How to Run
```bash
pip install -r requirements.txt
python3 -m scripts/build_fingerprints.py
python3 -m scripts/run_identification.py