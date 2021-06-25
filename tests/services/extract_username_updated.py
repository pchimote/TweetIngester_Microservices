import pandas as pd
import utils

def service_handler(input_filename, output_filename,param='user'): # For twirole use param = 'twirole'
    """
    Input
        data: dataframe of tweets
    Output
        dataframe of tweets with the respective tweet's originating username column/field to index on
    """

    data = pd.read_json(input_filename)
    data['username'] = '' #create empty column
    for i in range(0,data.shape[0]):
        if 'from_user' in data:
            from_username = data['from_user'].iloc[i]  # get the tweet's originating username
        elif 'user' in data and 'screen_name' in data['user'].iloc[i]:
            from_username = data['user'].iloc[i]['screen_name']
        data.at[i,'username'] = from_username  # adding username to the new column created
    if param=='user':
      data.to_json(output_filename)
    else:
      data = data.drop_duplicates(subset=["username"]) # get only unique usernames for twirole
      data.to_json(output_filename)
      
print('extract_username.py starting...')
if __name__ == '__main__':
    input_filename = utils.get_input()
    output_filename = utils.get_output()
    service_handler(input_filename, output_filename)
