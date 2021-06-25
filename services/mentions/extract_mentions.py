import numpy as np
import pandas as pd
import re
import utils

def service_handler(input_filename, output_filename):
    """
    Input
        df: dataframe of tweets
    Output
        dataframe of tweets with mentions column/field to index on
    """

    df = pd.read_json(input_filename)

    # Add another field to the dataframe.
    df['mentions'] = [str(i) for i in range(len(df))]

    # Check in the entities field for mentions data.
    if "entities" in df:
        for index, tweet in df.iterrows():
            m_data = []
            if len(tweet['entities']['user_mentions']) > 0:
                for j in tweet['entities']['user_mentions']:
                    m_data.append(j['screen_name'])
                df.at[index, 'mentions'] = m_data
                
            else:
                df.at[index, 'mentions'] = m_data
                
    elif "full_text" in df:
        for index, tweet in df.iterrows():
            # For each, grab all the relevant mentions.
            df.at[index, 'mentions'] = re.findall(r"@(\w+)", tweet['full_text'])

    elif "text" in df:
        for index, tweet in df.iterrows():
            # For each, grab all the relevant hashtags.
            df.at[index, 'mentions'] = re.findall(r"@(\w+)", tweet['text'])

    # Return the dataframe with tweets + mentions field
    df.to_json(output_filename)


print('extract_mentions.py starting...')
if __name__ == '__main__':
    input_filename = utils.get_input('HASHTAGS_FILENAME')
    output_filename = utils.get_output('MENTIONS_FILENAME')
    service_handler(input_filename, output_filename)

