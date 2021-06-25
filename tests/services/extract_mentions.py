import pandas as pd
import re
import utils

def service_handler(input_filename, output_filename):
    """
    Input
        df: dataframe of tweets
    Output
        dataframe of tweets with Username mentions column/field to index on
    """

    df = pd.read_json(input_filename)

    # Add another field to the dataframe.
    df['mentions'] = [str(i) for i in range(len(df))]

    # Iterate through the tweets.
    for index, tweet in df.iterrows():
        # For each, grab all the relevant username.
        df.at[index, 'mentions'] = re.findall(r"@(\w+)", tweet['full_text'])

    # Return the dataframe with tweets + username field
    df.to_json(output_filename)


print('extract_mentions.py starting...')
if __name__ == '__main__':
    input_filename = utils.get_input()
    output_filename = utils.get_output()
    service_handler(input_filename, output_filename)
