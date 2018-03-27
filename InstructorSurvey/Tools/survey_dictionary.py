import pandas as pd

NaN = "nan"
BLANK = "No Response"


def make_dictionary(keys, short_keys, data_frame, column):
    """
    Returns a dictionary that's ready to be turned into a chart.
    keys: a list of the keys that appear in the dataframe
    short_keys: short hand of keys that will appear in the dictionary
                NOTE: These indices must correspond with their full
                counterparts in "keys"
                Ex:
                keys = [one, two, three, ...]
                short_keys = [1, 2, 3, ...]
    data_frame: pandas dataframe
    column: column of interest in the dataframe
    """
    survey_dict = {}
    # Make survey_dict keys from the "short_keys"
    for s_k in short_keys:
        survey_dict[s_k] = 0
    # Create a k/v pair for BLANK responses
    survey_dict[BLANK] = 0
    # Iterate through data frame column in question
    for item in data_frame[column]:
        s_item = str(item)
        # iterate through all keys
        for i in range(len(keys)):
            # If a key is in the column, increment the corresponding
            # "short key (abbreviation)" in the dictionary
            if keys[i] == s_item:
                survey_dict[short_keys[i]] += 1
        # Check for blank responses
        if NaN in s_item:
            survey_dict[BLANK] += 1
    # If no blanks, remove this pair
    if survey_dict[BLANK] == 0:
        del survey_dict[BLANK]
    return survey_dict
