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
    if "full_text" in df:
        for index, tweet in df.iterrows():
            # For each, grab all the relevant keywords.
            df.at[index, 'keywords'] = keywords(tweet['full_text'])

    elif "text" in df:
        for index, tweet in df.iterrows():
            # For each, grab all the relevant keywords.
            df.at[index, 'keywords'] = keywords(tweet['text'])

    # Return the dataframe with tweets + keyword field
    df.to_json(output_filename)


print('extract_keywords.py starting...')
if __name__ == '__main__':
    input_filename = utils.get_input('GEOLOCATION_FILENAME')
    output_filename = utils.get_output('KEYWORDS_FILENAME')
    service_handler(input_filename, output_filename)
