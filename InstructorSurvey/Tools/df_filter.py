import pandas as pd


def col_cell_value(data_frame, column, cell_val):
    """
    Return a dataframe that is filtered by cell_val
    in a certain column.
    Ex: column = "Color", cell_val = "Green"
    Also works on a "contains basis"
    Ex: cell = [Blue/Green], cell_val = "Green" => cell will
    be kept.
    """
    # Drop NaN responses
    new_data_frame = data_frame.dropna(subset=[column])
    # Look for cells in "column" that contain "cell_val"
    new_data_frame = new_data_frame[new_data_frame[column].str.contains(cell_val)]
    new_data_frame = new_data_frame.reset_index(drop=True)
    return new_data_frame
