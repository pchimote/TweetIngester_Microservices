import filter_merge

import numpy as np
import pandas as pd

import json
import os


SFM_INPUT = 'sfm-coronavirus-sample-geo.json'
SFM_INPUT2 = 'sfm-coronavirus-sample-geo-copy.json'
OUTPUT_FILENAME = 'output-test-fm.json'


def test_filter_zero():
    """
    Validate that filtering zero fields returns empty json.
    """

    # Run the service.
    filter_merge.service_handler('filter', [SFM_INPUT], OUTPUT_FILENAME)

    # Make sure the file exists.
    assert os.path.exists(OUTPUT_FILENAME)

    # Validate file contents.
    with open(OUTPUT_FILENAME, 'r') as f:
        new_json = json.loads(f.read())

    assert len(new_json) == 0


def test_filter_one():
    """
    Validate that filtering one field returns valid, record-oriented json,
    while overwriting the existing file.
    """

    # Clean up from previous runs.
    if os.path.exists(OUTPUT_FILENAME):
        os.remove(OUTPUT_FILENAME)

    # Run the service.
    filter_merge.service_handler('filter', [SFM_INPUT, ['text']], OUTPUT_FILENAME)

    # Make sure the file exists.
    assert os.path.exists(OUTPUT_FILENAME)

    # Validate file contents.
    orig_df = pd.read_json(SFM_INPUT)
    with open(OUTPUT_FILENAME, 'r') as f:
        new_json = json.loads(f.read())

    new_df = pd.DataFrame(new_json)
    assert orig_df[['text']].equals(new_df)

    # Rerun with different filter to test overwrite.
    filter_merge.service_handler('filter', [SFM_INPUT, ['id_str']], OUTPUT_FILENAME)
    assert os.path.exists(OUTPUT_FILENAME)
    orig_df = pd.read_json(SFM_INPUT)
    with open(OUTPUT_FILENAME, 'r') as f:
        new_json = json.loads(f.read())

    new_df = pd.DataFrame(new_json)
    assert orig_df[['id_str']].equals(new_df)


def test_filter_two():
    """
    Validate that filtering two fields returns valid, record-oriented
    json, while maintaining order.
    """

    # Run the service.
    filter_merge.service_handler('filter', [SFM_INPUT, ['text', 'id_str']], OUTPUT_FILENAME)

    # Make sure the file exists.
    assert os.path.exists(OUTPUT_FILENAME)

    # Validate file contents.
    orig_df = pd.read_json(SFM_INPUT)
    with open(OUTPUT_FILENAME, 'r') as f:
        new_json = json.loads(f.read())

    new_df = pd.DataFrame(new_json)
    assert orig_df[['text', 'id_str']].equals(new_df)

    # Rerun with re-ordered filter.
    filter_merge.service_handler('filter', [SFM_INPUT, ['id_str', 'text']], OUTPUT_FILENAME)
    assert os.path.exists(OUTPUT_FILENAME)
    orig_df = pd.read_json(SFM_INPUT)
    with open(OUTPUT_FILENAME, 'r') as f:
        new_json = json.loads(f.read())

    new_df = pd.DataFrame(new_json)
    assert orig_df[['id_str', 'text']].equals(new_df)


def test_filter_nested():
    """
    Validate that filtering nested fields returns valid, record-oriented
    json.
    """

    # Run the service.
    filter_merge.service_handler('filter', [SFM_INPUT, ['user']], OUTPUT_FILENAME)

    # Make sure the file exists.
    assert os.path.exists(OUTPUT_FILENAME)

    # Validate file contents.
    orig_df = pd.read_json(SFM_INPUT)
    with open(OUTPUT_FILENAME, 'r') as f:
        new_json = json.loads(f.read())

    new_df = pd.DataFrame(new_json)
    assert orig_df[['user']].equals(new_df)


def test_merge_zero():
    """
    Validate that merging zero files/fields returns empty json.
    """

    # Run the service.
    filter_merge.service_handler('merge', [], OUTPUT_FILENAME)

    # Make sure the file exists.
    assert os.path.exists(OUTPUT_FILENAME)

    # Validate file contents.
    with open(OUTPUT_FILENAME, 'r') as f:
        new_json = json.loads(f.read())

    assert len(new_json) == 0


def test_merge_one():
    """
    Validate that merging one file/field returns valid, record-oriented
    json.
    """

    # Run the service.
    filter_merge.service_handler('merge', [(SFM_INPUT, 'text')], OUTPUT_FILENAME)

    # Make sure the file exists.
    assert os.path.exists(OUTPUT_FILENAME)

    # Validate file contents.
    orig_df = pd.read_json(SFM_INPUT)
    with open(OUTPUT_FILENAME, 'r') as f:
        new_json = json.loads(f.read())

    new_df = pd.DataFrame(new_json)
    assert orig_df[['text']].equals(new_df)


def test_merge_two():
    """
    Validate that merging two files/fields returns valid, record-oriented
    json, whether from the same file or different files.
    """

    # Run the service.
    filter_merge.service_handler('merge', [(SFM_INPUT, 'text'), (SFM_INPUT, 'id_str')], OUTPUT_FILENAME)

    # Make sure the file exists.
    assert os.path.exists(OUTPUT_FILENAME)

    # Validate file contents.
    orig_df = pd.read_json(SFM_INPUT)
    with open(OUTPUT_FILENAME, 'r') as f:
        new_json = json.loads(f.read())

    new_df = pd.DataFrame(new_json)
    assert orig_df[['text', 'id_str']].equals(new_df)

    # Rerun with different files.
    filter_merge.service_handler('merge', [(SFM_INPUT, 'text'), (SFM_INPUT2, 'id_str')], OUTPUT_FILENAME)
    assert os.path.exists(OUTPUT_FILENAME)
    orig_df = pd.read_json(SFM_INPUT)
    with open(OUTPUT_FILENAME, 'r') as f:
        new_json = json.loads(f.read())

    new_df = pd.DataFrame(new_json)
    assert orig_df[['text', 'id_str']].equals(new_df)
