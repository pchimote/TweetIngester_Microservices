import warc_to_json

import pandas as pd

import json
import os


SFM_INPUT = 'user_timeline.warc.gz'
OUTPUT_FILENAME = 'output-test-warc.json'
BACKUP_FILENAME = 'output-test-warc.parquet'
EXPECTED_COLS = ['created_at', 'id', 'id_str', 'full_text', 'truncated', 'display_text_range', 'entities', 'source', 'in_reply_to_status_id', 'in_reply_to_status_id_str', 'in_reply_to_user_id', 'in_reply_to_user_id_str', 'in_reply_to_screen_name', 'user', 'geo', 'coordinates', 'place', 'contributors', 'is_quote_status', 'retweet_count', 'favorite_count', 'favorited', 'retweeted', 'lang', 'quoted_status_id', 'quoted_status_id_str', 'quoted_status_permalink', 'extended_entities', 'possibly_sensitive']


def test_user_timeline():
    # Clean up from previous runs.
    if os.path.exists(OUTPUT_FILENAME):
        os.remove(OUTPUT_FILENAME)

    if os.path.exists(BACKUP_FILENAME):
        os.remove(BACKUP_FILENAME)

    # Run the service.
    warc_to_json.service_handler(SFM_INPUT, OUTPUT_FILENAME, BACKUP_FILENAME)

    # Make sure the files exist.
    assert os.path.exists(OUTPUT_FILENAME)
    assert os.path.exists(BACKUP_FILENAME)

    # Validate file contents.
    with open(OUTPUT_FILENAME, 'r') as f:
        new_json = json.loads(f.read())

    df = pd.DataFrame(new_json)
    assert len(df) == 3123
    assert len(df.columns.values) == 31
    for col in EXPECTED_COLS:
        assert col in df.columns.values

    df = pd.read_parquet(BACKUP_FILENAME)
    assert len(df) == 3123
    assert len(df.columns.values) == 29
    for col in EXPECTED_COLS:
        assert col in df.columns.values
