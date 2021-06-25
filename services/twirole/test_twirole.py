import twirole
import upload
import numpy as np
import pandas as pd
import json

def test_twirole():
    """
    Validate that exporting using our service maintains all fields/values.
    """

    with open('sfm-coronavirus-sample-geo.json') as f:
        data = json.load(f)

    df = pd.DataFrame(data) # Read in some sample data and modify the dataframe.
    df = df.drop('created_at', axis=1)  # We drop 'created_at' since timezones cause issues with equality.

    new_df = twirole.service_handler(df)

    assert 'twirole' in df

test_twirole()