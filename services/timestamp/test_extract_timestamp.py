import extract_timestamp
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
    output_filename = 'output-test-et.json'
    extract_timestamp.service_handler(input_filename, output_filename)
    with open(output_filename) as f:
      op_data = json.load(f)

    op_data = pd.DataFrame(op_data)
    # Hand off variable to test functions.
    yield op_data

# Test input data (before running service)
def test_null_ip(ip_data):
    if 'time' in ip_data:
        for index, tweet in ip_data.iterrows():
            assert len(tweet['time']) > 0
    elif 'timestamp_ms' in ip_data:
        for index, tweet in ip_data.iterrows():
            assert len(tweet['timestamp_ms']) > 0
    elif 'created_at' in ip_data:
        for index, tweet in ip_data.iterrows():
            assert len(tweet['created_at']) > 0
    else:
        # An unimplemented format.
        assert False

def test_non_ascii(ip_data):
    if 'time' in ip_data:
        for index, tweet in ip_data.iterrows():
            assert len(tweet['time']) == len(tweet['time'].encode())
    elif 'timestamp_ms' in ip_data:
        for index, tweet in ip_data.iterrows():
            assert len(tweet['timestamp_ms']) == len(tweet['timestamp_ms'].encode())
    elif 'created_at' in ip_data:
        for index, tweet in ip_data.iterrows():
            assert len(tweet['created_at']) == len(tweet['created_at'].encode())
    else:
        # An unimplemented format.
        assert False

def test_inv_format(ip_data):
    assert (("time" in ip_data.columns) or ("timestamp_ms" in ip_data.columns) or ("created_at" in ip_data.columns))

# Test service implementation
def test_timestamp_column(op_data):
    assert 'timestamp' in op_data.columns
