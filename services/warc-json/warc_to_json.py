import pandas as pd
import pyarrow
from warcio.archiveiterator import ArchiveIterator

import json
import os
from pathlib import Path
import utils
import sys


URI_LIST = ('https://api.twitter.com/1.1/statuses/user_timeline.json',
    'https://api.twitter.com/1.1/search/tweets.json',
    'https://stream.twitter.com/1.1/statuses/filter.json')
DLRL_PREFIX = '/mnt/camelot-dlrl/'
BACKUP_PREFIX = '/mnt/camelot-cs5604/twt/'
WARC_SUFFIX = '.warc.gz'
PARQUET_SUFFIX = '.parquet'

def service_handler(input_filename, output_filename, backup_filename):
    # Compile tweets from provided warc.
    tweets_list = []
    with open(input_filename, 'rb') as stream:
        for record in ArchiveIterator(stream):
            target_URI = record.rec_headers.get_header('WARC-Target-URI')
            if record.rec_type == 'response' and target_URI.startswith(URI_LIST):
                content = record.content_stream().read()
                content_json = json.loads(content)
                tweets_list += content_json

    # Write out json file containing tweets.
    with open(output_filename, 'w') as output_file:
        output_file.write(json.dumps(tweets_list))

    # Attempt to auto-generate the backup location if expected format.
    if backup_filename is None:
        backup_filename = gen_backup_loc(input_filename)

    # Create backup parquet file.
    if backup_filename is not None:
        backup_df = pd.DataFrame(tweets_list)
        backup_df = backup_df.drop(columns=['retweeted_status', 'quoted_status'], errors='ignore')  # Complicated meta-structures.
        backup_dir = '/'.join(backup_filename.split('/')[:-1])
        Path(backup_dir).mkdir(parents=True, exist_ok=True)
        backup_df.to_parquet(backup_filename)


def gen_backup_loc(backup_filename):
    """
    Attempts to auto-generate the backup location if expected format.
    """

    # Check prefix.
    if input_filename.startswith(DLRL_PREFIX):
        # Replace prefix and check extension.
        input_filename = BACKUP_PREFIX + input_filename[len(DLRL_PREFIX):]
        if input_filename.endswith(WARC_SUFFIX):
            # Replace extension and return.
            input_filename = input_filename[:-1 * len(WARC_SUFFIX)] + PARQUET_SUFFIX
            return input_filename

    # Not expected format.
    return None


print('warc_to_json.py starting...')
if __name__ == '__main__':
    input_filename = utils.get_input('WARC_FILENAME')
    output_filename = utils.get_output('JSON_FILENAME')
    backup_filename = utils.get_output('BACKUP_FILENAME')
    service_handler(input_filename, output_filename)
