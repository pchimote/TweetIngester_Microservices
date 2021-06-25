import re
import sys, os
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

    #Unique Username
    df_distinct_users = pandas.read_json("/mnt/camelot-cs5604/twt/distinct_users.json")
    values = list()
    for i in range(0, df.shape[0]):
        if 'from_user' in df:
            from_username = df['from_user'].iloc[i]  # get the tweet's originating username
        elif 'user' in df and 'screen_name' in df['user'].iloc[i]:
            from_username = df['user'].iloc[i]['screen_name']
        
        values.append(from_username)
        input_file_usernames = {'username': from_username, 'twirole': ""}
        df_distinct_users = df_distinct_users.append(input_file_usernames, ignore_index=True)# adding username to the new column created
    
    df_distinct_users = df_distinct_users.drop_duplicates(subset=['username']) # get only unique usernames for twirole    

    #usernames in current input file
    data = pandas.DataFrame(data={"col1": values})
    data.to_csv("output.csv", sep=',',index=False, header=False)
    classification = user_classifier.main("output.csv", df_distinct_users)

    # Iterate over data.
    for tweet, username in zip(df.iterrows(), values):
        # For each, grab the classification for each username.
        found = classification.index[classification['username'] == username].tolist()
        df.at[tweet[0], 'twirole'] = classification['twirole'].iloc[found[0]]

    #Return the dataframe with tweets + twirole classification field
    classification.to_json("/mnt/camelot-cs5604/twt/distinct_users.json")
    df.to_json(output_filename)



print('twirole.py starting...')
if __name__ == '__main__':
    input_filename = utils.get_input('KEYWORDS_FILENAME')
    output_filename = utils.get_output('TWIROLE_FILENAME')
    service_handler(input_filename, output_filename)
