import pandas as pd
import os.path
import utils

def service_handler(input_filename, output_filename):
    """
    Input
        data: dataframe of tweets
    Output
        dataframe of tweets with the respective tweet's originating username column/field to index on
    """

    # Read the collection of tweets being passed through the pipeline.
    data = pd.read_json(input_filename)
    data = data[['username']]

    # Grab unique usernames/categorization database if exists.
    if os.path.isfile(output_filename):
        df1 = pd.read_json(output_filename)
        data = df1.append(data)

    data = data.drop_duplicates(subset=["username"], ignore_index=True)
    data.to_json(output_filename)


print('unique_users.py starting...')
if __name__ == '__main__':
    input_filename = utils.get_input('KEYWORDS_FILENAME')
    output_filename = utils.get_output('UNIQUE_FILENAME')
    service_handler(input_filename, output_filename)
