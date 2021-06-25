import re
import sys, os
import Extract_username
import pandas
import user_classifier
import utils

def service_handler(input_filename, output_filename):
    """
    TODO: Mostly pseudocode, convert/validate actual syntax

    Input
        df: dataframe of tweets

    Output
        dataframe of tweets with twirole column/field to index on
    """

    df = pandas.read_json(input_filename)

    # Add another field to the dataframe.
    df['twirole'] = [str(i) for i in range(len(df))]

    df_username = Extract_username.service_handler(df)
    values = list(x for x in df_username['username'])
    data = pandas.DataFrame(data={"col1": values})
    data.to_csv("output.csv", sep=',',index=False, header=False)
    classification = user_classifier.main("output.csv")

    # Iterate over data.
    for index, tweet in df.iterrows():
        # For each, grab the classification for each username.

        df.at[index, 'twirole'] = classification[df_username.at[index, 'username']]

    #Return the dataframe with tweets + twirole classification field
    df.to_json(output_filename)


print('twirole.py starting...')
if __name__ == '__main__':
    input_filename = utils.get_input()
    output_filename = utils.get_output()
    service_handler(input_filename, output_filename)
