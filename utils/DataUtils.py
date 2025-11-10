import pandas as pd
import os

def get_csv_data(file_name):
    """
    Reads test data from a CSV file in the 'data' directory.
    """
    # Get the absolute path to the data directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, "..", "data")
    file_path = os.path.join(data_dir, file_name)

    df = pd.read_csv(file_path)

    # Convert dataframe to a list of tuples
    # 'itertuples' is a fast way to get rows
    return [tuple(row) for row in df.itertuples(index=False)]

# Note: If pandas is not desired, this can be done
# with the built-in 'csv' module.
