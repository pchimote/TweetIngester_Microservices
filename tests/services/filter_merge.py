import pandas as pd
import utils

def service_handler(fm_mode, fm_args, output_filename):
    """
    Input
    Output
    """

    if fm_mode == 'filter':
        # Filter mode.
        input_filename = fm_args[0]
        print(len(fm_args))
        if len(fm_args) == 1:
            # No fields given, output empty json.
            df = pd.DataFrame()
        else:
            # Fields given, pull them out.
            filter_fields = fm_args[1]
            df = pd.read_json(input_filename)[filter_fields]
    else:
        # Merge mode, from each pair, pull out the specified field.
        df = pd.DataFrame()
        for filename, field in fm_args:
            df[field] = pd.read_json(filename)[field]

    df.to_json(output_filename, orient='records')


print('filter_merge.py starting...')
if __name__ == '__main__':
    output_filename = utils.get_output()
    fm_mode, fm_args = utils.gen_fm_args()
    service_handler(fm_mode, fm_args, output_filename)
