from services import export

import numpy as np
import pandas as pd

def test_json_export():
    """
    Validate that exporting using our service maintains all fields/values.
    """

    # Read in some sample data and modify the dataframe.
    df = pd.read_json('sfm-coronavirus-sample-geo.json')
    df = df.drop('created_at', axis=1)  # We drop 'created_at' since timezones cause issues with equality.
    df['test_col'] = 1;

    # Write back to another file.
    export.service_handler(df, 'test.json', to_json=True)

    # Validate by reading in and comparing.
    df_copy = pd.read_json('test.json')
    assert df.equals(df_copy)
