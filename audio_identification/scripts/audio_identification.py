import os
import time
from tqdm.auto import tqdm
from src.config import DEFAULT_PARAMS
from src.matching import match_query
from src.extract_song_name import extract_song_name

def run(query_dir, fingerprint_dir, output_file):
    """
    Identifies the top N matches for the file in query recordings folder path
    by comparing with fingerprints of database recordings and prints/stores 
    the output in output.txt file
    """

    start = time.time()    
    hit_count = 0
    query_count = 0

    entries = [e for e in os.scandir(query_dir) if e.is_file()]

    with open(output_file, "w") as f:
        for entry in tqdm(
            entries,
            desc="Identifying audio",
            unit="query",
            colour="blue"
        ):
            _, top = match_query(
                entry.path,
                fingerprint_dir,
                DEFAULT_PARAMS,
                DEFAULT_PARAMS["topN"]
            )
            out = entry.name
            for recording in top:
                q_out, db_out = extract_song_name(
                    entry.path,
                    recording)
                out = out + '\t' + db_out + '.wav'
                if q_out == db_out:
                    hit_count += 1
            query_count += 1
            f.write(out + '\n')

    # Accuracy score calculation
    accuracy = (hit_count / query_count) * 100

    print(f"Time taken to compute all matches and write to output file: {time.time() - start:.2f}s")
    print(f"Total number of queries: {query_count}")
    print(f"Total number of matches: {hit_count}")
    print(f"Accuracy: {accuracy:.2f}%")

    return query_count, hit_count, accuracy

if __name__ == "__main__":
    run("data/query_recordings", "data/fingerprints", "output.txt")
