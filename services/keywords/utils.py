import os
import sys

def throw_invalid_env(var):
    """
    Throw a ValueError with a message related to the missing environment variable.
    """
    raise ValueError('Required environment variable `{}` not found'.format(var))


def throw_not_found(filename, var):
    """
    Throw a FileNotFoundError with a message related to the missing file.
    """
    raise FileNotFoundError('`{}` (from environment variable `{}`) not found'.format(filename, var))


def warning_overwrite(filename):
    """
    Log a warning related to overwriting an existing file.
    """
    print('Warning: will overwrite file `{}`'.format(filename), file=sys.stderr)


def throw_invalid_args(args, var):
    """
    Throw a FileNotFoundError with a message related to the missing file.
    """
    raise ValueError('Invalid content `{}` (from environment variable `{}`)'.format(args, var))


def get_input(var_name):
    """
    Grab input filename from the environment and validate.
    """

    # We must be provided with an input filename, or error.
    env_vars = os.environ
    if var_name not in env_vars:
        throw_invalid_env(var_name)

    # Validate that the input file exists.
    input_filename = env_vars[var_name]
    if not os.path.isfile(input_filename):
        throw_not_found(input_filename, var_name)

    return input_filename


def get_output(var_name):
    """
    Grab output filename from the environment and validate.
    """

    # We must be provided with an output filename, or error.
    env_vars = os.environ
    if var_name not in env_vars:
        throw_invalid_env(var_name)

    # Check whether the output file exists.
    output_filename = env_vars[var_name]
    if os.path.isfile(output_filename):
        warning_overwrite(output_filename)

    return output_filename


def gen_fm_args():
    """
    Generate filter/merge mode and argument values from the environment.
    """

    # We must be provided with both mode/args, or error.
    env_vars = os.environ
    if 'FM_MODE' not in env_vars:
        throw_invalid_env('FM_MODE')
    elif 'FM_ARGS' not in env_vars:
        throw_invalid_env('FM_ARGS')

    # Validate the mode is one of filter/merge, and build args
    # accordingly.
    fm_mode = env_vars['FM_MODE']
    split_args = env_vars['FM_ARGS'].split(',')
    if fm_mode == 'filter':
        # Treat as a filename and a list of fields.
        fm_args = (split_args[0], split_args[1:])
    elif fm_mode == 'merge' and len(split_args) % 2 == 0:
        # Treat as a list of filename/field pairs.
        fm_args = []
        for i in range(0, len(split_args), 2):
            fm_args.append((split_args[i], split_args[i + 1]))
    else:
        throw_invalid_args(split_args, 'FM_ARGS')

    return fm_mode, fm_args
