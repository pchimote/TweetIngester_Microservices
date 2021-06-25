import extract_geolocations
import pandas as pd
import numpy as np
import json
import pytest

@pytest.fixture(scope='module')
def ip_data():

  input_filename = 'sfm-coronavirus-sample-geo.json'
  with open(input_filename) as f:
    ip_data = json.load(f)

  ip_data = pd.DataFrame(ip_data)
  # Hand off variable to test functions.
  yield ip_data


@pytest.fixture(scope='module')
def op_data():
  input_filename = 'sfm-coronavirus-sample-geo.json'
  output_filename = 'output-test-eg.json'
  extract_geolocations.service_handler(input_filename, output_filename)
  with open(output_filename) as f:
    op_data = json.load(f)

  op_data = pd.DataFrame(op_data)
  yield op_data

#test input data
def test_null_ip(ip_data):
  for index, tweet in ip_data.iterrows():
    if not (tweet['coordinates'] == None):
      assert len(tweet['coordinates']) > 0

def test_non_ascii(ip_data):
  for index, tweet in ip_data.iterrows():
    if not (tweet['coordinates'] == None):
      listToStr = ' '.join([str(elem) for elem in tweet['coordinates']])
      assert len(listToStr) == len(listToStr.encode())

def test_inv_format(ip_data):
  assert "coordinates" in ip_data.columns

#test the implementation (output data)
def test_geolocation_column(op_data):
  assert 'geolocation' in op_data.columns
