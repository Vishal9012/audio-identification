import os
import numpy as np
from tqdm.auto import tqdm
from scipy.stats import mode
from .fingerprint import compute_fingerprint

def match_query(query_path, fingerprint_dir, params, top_n):
    """
    Computes matching function for query file against all files in database 
    and returns the top N results with the maximum value.
    """
    q_fp = compute_fingerprint(query_path, params)
    matches = {}

    # Traverse through the database fingerprints and compute matching function
    for entry in tqdm(
        os.scandir(fingerprint_dir),
        desc="Matching against database",
        leave=False,
        unit="track"
    ): 
    
        db_fp = np.load(entry.path, allow_pickle=True)[()]

        # Implementation of the matching function by inverted list algorithm
        delta = []
        for h, q_times in q_fp.items():
            if h not in db_fp:
                continue
            
            q_times = np.asarray(q_times).ravel()
            db_times = np.asarray(db_fp[h]).ravel()

            if q_times.size == 0 or db_times.size == 0:
                continue

            for qt in q_times:
                delta.extend(db_times - int(qt))

        if len(delta) == 0:
            continue
        
        delta = np.array(delta)
        m = mode(delta)
        count = m.count
        if hasattr(count, "__len__"):
            count = count[0]
        matches[entry.path] = count

    # Obtain top N matched results for the corresponding query recording
    top_results = []
    for n in range(top_n):
        count = 0
        res = -1
        for match in matches:
            if matches[match] > count:
                res = match
                count = matches[match]
        top_results += [res]
        del matches[res]    
    return matches, top_results
