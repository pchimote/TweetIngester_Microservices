import extract_username
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
    output_filename = 'output-test-eu.json'
    extract_username.service_handler(input_filename, output_filename)
    with open(output_filename) as f:
      data = json.load(f)

    data = pd.DataFrame(data)

    # Hand off variable to test functions.
    yield data
    
def test_null_ip(ip_data):
    for index, tweet in ip_data.iterrows():
        assert len(tweet['user']) > 0

def test_non_ascii(ip_data):
    for index, tweet in ip_data.iterrows():
        assert len(tweet['user']['screen_name']) == len(tweet['user']['screen_name'].encode())

def test_inv_format(ip_data):
    assert "user" in ip_data.columns


def test_username_column(data):
    assert 'username' in data.columns

def test_username_column_data(data):
    # test whether an extracted username are present in tweet data
    ind = random.randrange(0, len(data))
    user = data['username'].iloc[ind]
    screenname = data['user'].iloc[ind]['screen_name']
    assert user == screenname

