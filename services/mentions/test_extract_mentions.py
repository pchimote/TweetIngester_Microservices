import extract_mentions
import random
import numpy as np
import pandas as pd
import json
import pytest

@pytest.fixture(scope="session")
def ip_data():
    # read data (.json)
    input_filename = 'sfm-coronavirus-sample-geo.json'
    with open(input_filename) as f:
        ip_data = json.load(f)

    ip_data = pd.DataFrame(ip_data)
    # Hand off variable to test functions.
    yield ip_data

@pytest.fixture(scope='module')
def data():

    # Set up.
    input_filename = 'sfm-coronavirus-sample-geo.json'
    output_filename = 'output-test-em.json'
    extract_mentions.service_handler(input_filename, output_filename)
    with open(output_filename) as f:
      data = json.load(f)

    data = pd.DataFrame(data)

    # Hand off variable to test functions.
    yield data
    
def test_null_ip(ip_data):
    if "full_text" in ip_data:
        for index, tweet in ip_data.iterrows():
            assert len(tweet['full_text']) > 0

    elif "text" in ip_data:
        for index, tweet in ip_data.iterrows():
            assert len(tweet['text']) > 0

#def test_non_ascii(ip_data):
#    for index, tweet in ip_data.iterrows():
#        assert len(tweet['full_text']) == len(tweet['full_text'].encode())

def test_inv_format(ip_data):
    if "text" in ip_data.columns:
        pass
    elif "full_text" in ip_data.columns:
        pass
    else:
        assert "full_text" in ip_data.columns

def test_mentions_column(data):
    assert 'mentions' in data.columns


