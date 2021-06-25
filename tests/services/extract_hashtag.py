import numpy as np
import pandas as pd
import re
import utils

def service_handler(input_filename, output_filename):
    """
    Input
        df: dataframe of tweets
    Output
        dataframe of tweets with hashtag column/field to index on
    """

    df = pd.read_json(input_filename)

    # Add another field to the dataframe.
    df['hashtags'] = [str(i) for i in range(len(df))]

    # Check in the entities field for Hashtag data.
    if "entities" in df:
        for index, tweet in df.iterrows():
            # Check for blank row
            ht_data = []
            if len(tweet['entities']['hashtags']) > 0:
                for j in tweet['entities']['hashtags']:
                    ht_data.append(j)
                df.at[index, 'hashtags'] = ht_data
                
            else:
                df.at[index, 'hashtags'] = ht_data
                
    else:
        for index, tweet in df.iterrows():
            ht_data = []
            if len(tweet['full_text']) == 0:
                df.at[index, 'hashtags'] = ht_data
                continue
            # For each, grab all the relevant hashtags.
            df.at[index, 'hashtags'] = re.findall(r"#(\w+)", tweet['full_text'])

    # Return the dataframe with tweets + hashtags field
    df.to_json(output_filename)


print('extract_hashtag.py starting...')
if __name__ == '__main__':
    input_filename = utils.get_input()
    output_filename = utils.get_output()
    service_handler(input_filename, output_filename)
