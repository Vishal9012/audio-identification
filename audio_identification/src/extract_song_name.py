import os

def extract_song_name(q_path, db_path):
    """
    Obtain the recording names to aid for matching
    Return corresponding name depending on whether it is classical or pop file
    """
    q_name = os.path.basename(q_path)
    q_out = q_name[:15] if q_name.startswith("c") else q_name[:9]

    db_name = os.path.basename(db_path)
    db_out = db_name[:15] if db_name.startswith("c") else db_name[:9]

    return q_out, db_out
