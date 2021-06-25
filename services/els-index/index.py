import elasticsearch
import pandas as pd
import utils

def service_handler(input_filename, output_filename):
    """
    Input
        df: dataframe of (meta)data to index
    Output
        Logged info about the indexing results
    """

    df = pd.read_json(input_filename)

    # Get an ELS client.
    es = elasticsearch.Elasticsearch(
        [{'host': 'elasticsearch.cs.vt.edu', 'port': 9200}],
        http_auth=('elastic', 'P9O5qfUOMF8AmHZFKJnS'),
        use_ssl=True,
        verify_certs=False,
        ssl_show_warn=False,
    )

    # Create a new index for tweets if does not exist.
    if not es.indices.exists('twt'):
        es.indices.create(index='twt')

    # For each tweet, add to the index to be searchable based on all
    # given columns.
    created = 0
    updated = 0
    for i, tweet in df.iterrows():
        resp = es.index(index='twt', body=tweet.to_json(), id=tweet['id'])
        if resp['result'] == 'created':
            created += 1
        elif resp['result'] == 'updated':
            updated += 1

    total = len(df)
    with open(output_filename, 'w') as f:
        f.write('{} tweets indexed\n\n'.format(total))
        f.write('{} tweets created in index\n'.format(created))
        f.write('{} tweets updated in index\n'.format(updated))
        f.write('{} tweets remaining\n\n'.format(total - created - updated))
        f.write('Fields: {}\n'.format(df.columns.values.tolist()))

print('index.py starting...')
if __name__ == '__main__':
    input_filename = utils.get_input('FILTERED_FILENAME')
    output_filename = utils.get_input('ELS_FILENAME')
    service_handler(input_filename, output_filename)
