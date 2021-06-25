import json
import pandas as pd
import numpy as np
import pyarrow.parquet as pq



def service_handler(filename, isJson):
    if isJson:
        return json_format(filename)
    else:
        return parquet_format(filename)


def json_format(filename):
    df = pd.read_json(filename)
    return df


def parquet_format(filename):
    table = pq.read_table(filename)
    df = table.to_pandas()
    return df
