# Used subset of coronavirus data uploaded by Irith
import pandas as pd
import utils

def service_handler(input_filename, output_filename):
    """
    Input
        data: dataframe of tweets
    Output
        dataframe of tweets with the geolocation of each tweet to index on
    """

    data = pd.read_json(input_filename)
    data['geolocation'] = '' #create empty column
    for i in range(0,data.shape[0]):
      if 'coordinates' in data.iloc[i]:
          from_coordinates = data['coordinates'].iloc[i]  # get the tweet's originating geocoordinates
      else:
          from_coordinates = None
      from_coordinates = from_coordinates['coordinates']  
      data.at[i,'geolocation']=from_coordinates  # adding coordinates to the new column (geocoordinates) created

    data.to_json(output_filename)


print('extract_geolocations.py starting...')
if __name__ == '__main__':
    input_filename = utils.get_input()
    output_filename = utils.get_output()
    service_handler(input_filename, output_filename)
