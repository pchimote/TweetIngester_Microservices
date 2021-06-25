import pandas as pd

print("---------------------")
print("ELS Export Service")

def service_handler(filename, to_json):
    """
    Take a dataframe, write to a file, then give it back to the
    client.

    Input
        filename: name of the file to export to
        to_json: True if exporting to a json file, false if parquet.

    Output
        name of the file exported to
    """

    if to_json:
        # Export to json format.
        df.to_json(filename)
    else:
        # Export to parquet format.
        df.to_parquet(filename)

    # Expose the newly exported data.
    from_file()

    # Not really needed, but to maintain input/output schema.
    return filename


def from_file():
    """
    Expose a file for client download.
    """

    # Copy file to client-facing server to access outside ELS?
    # Redirect FE to copied file.
    pass
