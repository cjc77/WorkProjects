#! usr/bin/env python3
import os
import pandas as pd
import random

SS_DIR = 'Spreadsheets'
Q1 = 'Question1'
Q2 = 'Question2'
Q3 = 'Question3'

def rename_files():
    ch = 65
    for fn in os.listdir(SS_DIR):
        print(fn)
        old_name = SS_DIR + '/' + fn
        new_name = SS_DIR + '/' + chr(ch) + '.tsv'
        os.rename(old_name, new_name)
        print(fn)
        ch += 1


def scrub_text(frame, ipsum):
    # for each row in frame, generate random sized ipsum
    # if a cell is non-empty, replace the text with the ipsum
    keys = [Q1, Q2, Q3]
    ipsum_size = len(ipsum)
    for index, row in frame.iterrows():
        # Go through all keys
        for k in keys:
            if pd.isnull(row[k]):
                # print(row[Q1])
                continue
            else:
                # Find length of text in cell & replace with lorem ipsum
                text_size = len(row[k])
                upper_bound = ipsum_size - text_size
                rand_upper = random.randrange(0, upper_bound)
                rand_lower = rand_upper - text_size
                ipsum_sample = ipsum[rand_lower:rand_upper + 1]
                frame.set_value(index, k, ipsum_sample)


def main():
    # rename_files()
    ipsum = open('lorem-ipsum.txt')
    ipsum_str = ipsum.read()
    for fn in os.listdir(SS_DIR):
        frame = pd.read_csv(SS_DIR + '/' + fn, sep='\t')
        scrub_text(frame, ipsum_str)
        # Write out scrubbed data
        frame.to_csv(SS_DIR + '/' + fn, sep='\t')
        # print(frame)


if __name__ == '__main__':
    main()
