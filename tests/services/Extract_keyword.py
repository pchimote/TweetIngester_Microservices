from gensim.summarization import keywords
# Need proper installation of gensim
import pandas as pd
import re
import utils

def service_handler(input_filename, output_filename):
    """
    Input
        df: dataframe of tweets
    Output
        dataframe of tweets with keywords column/field to index on
    """

    df = pd.read_json(input_filename)

    # Add another field to the dataframe.
    df['keywords'] = [str(i) for i in range(len(df))]

    # Iterate through the tweets.
    for index, tweet in df.iterrows():
        # Check for blank row
        kw_data = []
        if len(tweet['full_text']) == 0:
            df.at[index, 'keywords'] = kw_data
            continue
        # For each, grab all the relevant keywords.
        df.at[index, 'keywords'] = keywords(tweet['full_text'])

    # Return the dataframe with tweets + keyword field
    df.to_json(output_filename)


print('extract_keyword.py starting...')
if __name__ == '__main__':
    input_filename = utils.get_input()
    output_filename = utils.get_output()
    service_handler(input_filename, output_filename)
