import json
import os
import sys
import pandas as pd
import numpy as np
import pyarrow.parquet as pq

class upload():
    def __init__(self,filename, isJson):
        self.filename = filename
        if isJson:
            json_format()
        else:
            parquet_format()


    def json_format(self):
        df = pd.read_json("ytk_eom_sample_data_z1.json")


    def parquet_format(self):
        table = pq.read_table('example.parquet')
        df = table.to_pandas()


class export():
    def __init__(self, filename, to_json):
        self.filename = filename
        self.to_json = to_json

    def from_df(self, df):
        """
        Take a dataframe, write to a file, then give it back to the
        client.
        """

        if self.to_json:
            # Export to json format.
            df.to_json(self.filename)
        else:
            # Export to parquet format.
            df.to_parquet(self.filename)

        # Expose the newly exported data.
        self.from_file()


    def from_file(self):
        """
        Expose a file for client download.
        """

        # Copy file to client-facing server to access outside ELS?
        # Redirect FE to copied file.
        pass
