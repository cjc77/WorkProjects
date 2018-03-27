import pandas as pd
from nltk.tokenize import RegexpTokenizer
from rake_nltk import Rake
import numpy as np
import re
from string import punctuation

CLASS_SIZE = 45
SECTION = 'Section'
Q1 = 'Question1'
Q2 = 'Question2'
Q3 = 'Question3'
MAX = 'Max'
AVG = 'Average'

ROUNDTO = 1
RATE = 4


class Course:
    """
    A class to group information relevant to
    courses.
    """
    def __init__(self, tsv_target_file):
        self.program = tsv_target_file.split('/', 1)[1].split('-', 1)[0]
        self.course_name = tsv_target_file.split('/', 1)[1].split('.', 1)[0]
        # pandas dataframe from responses on survey
        self.responses = pd.read_csv(tsv_target_file, sep='\t')
        # stripped data frame for section count calculation
        self.response_rates = self.responses.groupby(SECTION).count()
        self.class_size = 0
        self.set_class_size()
        # response_rates.shape[0] = num unique secitons
        self.total_students = self.class_size * self.response_rates.shape[0]
        # print(self.course_name + ": ", self.total_students)
        # values = lists of feedback strings for each question
        self.feedback = {Q1: None, Q2: None, Q3: None}
        # values = number of feedback strings per question
        # NOTE: a new key, MAX, will be the largest of the 3
        # {MAX: n1, Q1: n2, ...}
        self.feedback_counts = {Q1: None, Q2: None, Q3: None}
        # fill in values for feedback and feedback_counts
        self.response_rates = {MAX: None, Q1: None, Q2: None, Q3: None}
        # values = avg word count per feedback string
        # NOTE: a new key, AVG, will be the average of the 3 other averages
        # {MAX: n1, Q1: n2,...}
        self.avg_word_counts = {Q1: None, Q2: None, Q3: None}
        self.q1_key_phrases = []
        self.q2_key_phrases = []

        # Go through and fill in feedback/feedback_counts dictionaries
        self.process_feedback()
        # Calculate response rates
        self.find_response_rates()
        # Calculate average word counts
        self.find_word_counts()
        # Find the key phrases
        self.find_key_phrases()

    def __str__(self):
        # representation = str(self.responses)
        representation = "Program: " + self.program +\
                         "\nCourse: " + self.course_name +\
                         "\nQ1 Count: " + str(self.feedback_counts[Q1]) +\
                         "\nQ2 Count: " + str(self.feedback_counts[Q2]) +\
                         "\nQ3 Count: " + str(self.feedback_counts[Q3]) +\
                         "\nMax Count: " + str(self.feedback_counts[MAX]) +\
                         "\nQ1 Response Rate: " + str(self.response_rates[Q1]) +\
                         "\nQ2 Response Rate: " + str(self.response_rates[Q2]) +\
                         "\nQ3 Response Rate: " + str(self.response_rates[Q3]) +\
                         "\nTotal Response Rate (student responded to one or more question): " +\
                         str(self.response_rates[MAX]) +\
                         "\nQ1 Avg. Word Count: " + str(self.avg_word_counts[Q1]) +\
                         "\nQ2 Avg. Word Count: " + str(self.avg_word_counts[Q2]) +\
                         "\nQ3 Avg. Word Count: " + str(self.avg_word_counts[Q3]) +\
                         "\nTotal Avg. Word Count: " + str(self.avg_word_counts[AVG])
        return representation

    def set_class_size(self):
        self.class_size = CLASS_SIZE

    def process_feedback(self):
        # Convert columns to lists of strings
        self.feedback[Q1] = self.responses[Q1].tolist()
        self.feedback[Q2] = self.responses[Q2].tolist()
        self.feedback[Q3] = self.responses[Q3].tolist()

        # Remove NaN's from the lists
        # AND find the lengths of the resulting lists of strings
        for key in self.feedback:
            self.feedback[key] = [w for w in self.feedback[key]
                                  if not pd.isnull(w)]
            # Record the lengths of each list
            self.feedback_counts[key] = len(self.feedback[key])
        # Find largest feedback length
        # NOTE: this will be added to the feedback_counts dictionary
        self.feedback_counts[MAX] = max(self.feedback_counts.values())

    def find_response_rates(self):
        keys = [MAX, Q1, Q2, Q3]
        for key in keys:
            self.response_rates[key] = round((self.feedback_counts[key] /
                                              self.total_students), RATE)
            if self.response_rates[key] > 1:
                self.response_rates[key] = 1

    def find_word_counts(self):
        tokenizer = RegexpTokenizer(r'\w+')
        q1_wd_cnt = [len(tokenizer.tokenize(w)) for w in self.feedback[Q1]]
        q2_wd_cnt = [len(tokenizer.tokenize(w)) for w in self.feedback[Q2]]
        q3_wd_cnt = [len(tokenizer.tokenize(w)) for w in self.feedback[Q3]]
        self.avg_word_counts[Q1] = round(np.mean(q1_wd_cnt), ROUNDTO)
        self.avg_word_counts[Q2] = round(np.mean(q2_wd_cnt), ROUNDTO)
        self.avg_word_counts[Q3] = round(np.mean(q3_wd_cnt), ROUNDTO)
        tot_avg = round(np.mean([v for k, v in self.avg_word_counts.items()]), ROUNDTO)
        self.avg_word_counts[AVG] = tot_avg

    def print_feedback(self):
        print(self.feedback)
        print('counts: ', self.feedback_counts)

    def find_key_phrases(self):
        q1_string = " ".join(self.feedback[Q1])
        q2_string = " ".join(self.feedback[Q2])

        q1_rake = Rake()
        q1_rake.extract_keywords_from_text(q1_string)
        q1_phrases = q1_rake.get_ranked_phrases()
        self.q1_key_phrases = self.filter_phrases(q1_phrases, 2, 2)

        q2_rake = Rake()
        q2_rake.extract_keywords_from_text(q2_string)
        q2_phrases = q2_rake.get_ranked_phrases()
        self.q2_key_phrases = self.filter_phrases(q2_phrases, 2, 2)

    def filter_phrases(self, phrase_list, lower, upper):
        """
        Returns a new list with only keyphrases of desired length.
        """
        new_keywords = []
        r = re.compile(r'[{}]'.format(punctuation))
        for s in phrase_list:
            new_strs = r.sub(' ', s)
            if lower <= len(new_strs.split()) <= upper:
                new_keywords.append(s)
        return new_keywords
