#! usr/bin/env python3

import pandas as pd
import copy as cp


O = ord('0')
TERMS = 4
YT = "Year/Term"


class Course:
    """
    Course is made up of three pandas dataframes:
    course, readings, videos.
    """

    def __init__(self, dir_path, files):
        """
        dir_path -> path to tsv files
        files -> dictionary of 3 tsv files with keys: "course", "readings",
                 "videos"
        terms -> list of terms of interest in chronological order
        """
        self.details = pd.read_csv(dir_path+files["course"], sep='\t')
        self.readings = pd.read_csv(dir_path+files["readings"], sep='\t')
        self.videos = pd.read_csv(dir_path+files["videos"], sep='\t')
        self.course_title = self.details["Course"].iloc[0]
        # NOTE: This only grabs the coordinator for FTT
        self.coordinator = self.details["Coordinator"].iloc[0]
        self.terms = [str(w) for w in self.details[YT].tolist()]
        self.age_gap = None
        self.read_ht = self.readings.shape[0]
        self.vid_ht = self.videos.shape[0]
        self.read_score = -1
        self.vid_score = -1
        self.full_score = -1

    def score(self):
        r_rep = 0
        v_rep = 0
        original = ""
        for t in range(1, len(self.terms)):
            for j in range(0, self.read_ht):
                original = self.readings.loc[j, self.terms[0]]
                if self.readings.loc[j, self.terms[t]] == original:
                    r_rep += 1

        for t in range(1, len(self.terms)):
            for j in range(0, self.vid_ht):
                original = self.videos.loc[j, self.terms[t]]
                if self.videos.loc[j, self.terms[t]] == original:
                    v_rep += 1
        # Decimal score - amount of original material that is still present
        # for readings, videos, and then total
        self.read_score = 1 - ((self.read_ht - r_rep) / self.read_ht)
        self.read_score = round(self.read_score, 2)
        self.vid_score = 1 - ((self.vid_ht - v_rep) / self.vid_ht)
        self.vid_score = round(self.vid_score, 2)
        self.full_score = 1 - (((self.vid_ht - v_rep) + (self.read_ht - r_rep)) /\
                           (self.vid_ht + self.read_ht))
        self.full_score = round(self.full_score, 2)

    def calc_age_gap(self):
        year_diff = term_diff = 0
        fst_year = find_year(self.terms[0])
        lst_year = find_year(self.terms[1])
        fst_term = find_term(self.terms[0])
        lst_term = find_term(self.terms[1])

        year_diff = lst_year - fst_year
        term_diff = (lst_term - fst_term) / TERMS
        self.age_gap = year_diff + term_diff


def find_year(string):
    year = (ord(string[0]) - O) * (10 ** 3) + \
           (ord(string[1]) - O) * (10 ** 2) + \
           (ord(string[2]) - O) * 10 + \
           (ord(string[3]) - O)
    return year


def find_term(string):
    term = ord(string[-1]) - O
    return term
