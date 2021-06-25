import extract_hashtags
import random
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
def op_data():
    # read data (.json)
    input_filename = 'sfm-coronavirus-sample-geo.json'
    output_filename = 'output-test-eh.json'
    extract_hashtags.service_handler(input_filename, output_filename)
    with open(output_filename) as f:
      op_data = json.load(f)

    op_data = pd.DataFrame(op_data)
    # Hand off variable to test functions.
    yield op_data

# Test input data (before running service)
def test_null_ip(ip_data):
    if "full_text" in ip_data:
        for index, tweet in ip_data.iterrows():
            assert len(tweet['full_text']) > 0

    elif "text" in ip_data:
        for index, tweet in ip_data.iterrows():
            assert len(tweet['text']) > 0

#def test_non_ascii(ip_data):
#    if "full_text" in ip_data:
#        for index, tweet in ip_data.iterrows():
 #           assert len(tweet['full_text']) == len(tweet['full_text'].encode())

#    elif "text" in ip_data:
#        for index, tweet in ip_data.iterrows():
#            assert len(tweet['text']) == len(tweet['text'].encode())

def test_inv_format(ip_data):
    if "text" in ip_data.columns:
        pass
    elif "full_text" in ip_data.columns:
        pass
    else:
        assert "full_text" in ip_data.columns

# Test service implementation
def test_hashtag_column(op_data):
    assert 'hashtags' in op_data.columns

def test_hashtag_column_data(op_data):
    ind = random.randrange(0, len(op_data))
    hashtags = op_data['hashtags'].iloc[ind]
    tweet_data = op_data['text'].iloc[ind]
    assert hashtags[0] in tweet_data
