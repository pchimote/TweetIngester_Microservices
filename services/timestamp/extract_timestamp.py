from datetime import datetime
import pandas as pd
import utils

def service_handler(input_filename, output_filename):
    """
    Input
        df: dataframe of tweets
    Output
        dataframe of tweets with timestamp column/field to index on
    """

    df = pd.read_json(input_filename)

    # Convert existing columns.
    if 'time' in df:
        # yTK format.
        df['timestamp'] = pd.to_datetime(df['time'], unit='s')
    elif 'timestamp_ms' in df:
        # SFM format.
        df['timestamp'] = df['timestamp_ms']
    elif 'created_at' in df:
        df['timestamp'] = df['created_at']
    else:
        # An unimplemented format.
        assert False

    df.to_json(output_filename)


print('extract_timestamp.py starting...')
if __name__ == '__main__':
    input_filename = utils.get_input('USERNAME_FILENAME')
    output_filename = utils.get_output('TIMESTAMP_FILENAME')
    service_handler(input_filename, output_filename)
