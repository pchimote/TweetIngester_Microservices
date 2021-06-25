import elasticsearch
import pandas as pd
import utils

def service_handler(input_filename):
    """
    Input
        df: dataframe of (meta)data to index
    """

    df = pd.read_json(input_filename)

    # Get an ELS client.
    es = elasticsearch.Elasticsearch([{'host': 'elasticsearch.cs.vt.edu', 'port': 9200}])

    # Create a new index for tweets if does not exist.
    if not es.indices.exists('twt'):
        es.indices.create(index='twt')

    # For each tweet, add to the index to be searchable based on all
    # given columns.
    for _, tweet in df.iterrows():
        es.index(index='twt', body=tweet.to_json(), id=tweet['id'])

print('index.py starting...')
if __name__ == '__main__':
    input_filename = utils.get_input()
    service_handler(input_filename)
