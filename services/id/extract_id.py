import pandas as pd
import utils

def service_handler(input_filename, output_filename):
    """
    Input
        df: dataframe of tweets
    Output
        dataframe of tweets with id column/field to index on
    """

    # Convert id column to string, if needed.
    df = pd.read_json(input_filename)
    if 'id_str' in df:
        df['id'] = df['id_str']
    elif 'id' in df:
        id_col = df['id'];
        if len(id_col) > 0 and not isinstance(id_col[0], str):
            df['id'] = df['id'].astype('string')
    else:
        assert False

    # Return the dataframe with tweets + id field
    df.to_json(output_filename)


print('extract_id.py starting...')
if __name__ == '__main__':
    input_filename = utils.get_input('JSON_FILENAME')
    output_filename = utils.get_output('ID_FILENAME')
    service_handler(input_filename, output_filename)
