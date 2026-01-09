import os
import time
import numpy as np
from tqdm.auto import tqdm
from src.config import DEFAULT_PARAMS
from src.fingerprint import compute_fingerprint

def build(database_dir, output_dir):
    """
    Computes fingerprints for the files in database recordings folder path &
    stores them in fingerprints path
    """
    os.makedirs(output_dir, exist_ok=True)
    start = time.time()
    files = [e for e in os.scandir(database_dir) if e.is_file()]

    # Traverse through the database recordings and compute fingerprints for each of the files
    for entry in tqdm(
        files,
        desc="Building fingerprints",
        unit="file",
        colour="green"
    ):
        fp = compute_fingerprint(entry.path, DEFAULT_PARAMS)
        np.save(os.path.join(output_dir, entry.name[:-4]), fp)

    print(f"Fingerprinting completed in {time.time() - start:.2f}s")

if __name__ == "__main__":
    build("data/database_recordings", "data/fingerprints")
