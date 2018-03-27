import Course
import csv
import os

SS_DIR = 'Spreadsheets'


def read_courses(courses):
    for fn in os.listdir(SS_DIR):
        courses.append(Course.Course(SS_DIR + '/' + fn))


def print_courses(courses):
    for c in courses:
        print(c)


def write_file(courses):
    # Collect all of the data items in their appropriate columns
    data = [["program", "course", "q1-response-rate",
             "q2-response-rate", "q3-response-rate",
             "max-response-rate", "q1-avg-word-count",
             "q2-avg-word-count", "q3-avg-word-count",
             "total-avg-word-count"]]
    for c in courses:
        data.append(
            [c.program, c.course_name, c.response_rates[Course.Q1],
             c.response_rates[Course.Q2], c.response_rates[Course.Q3],
             c.response_rates[Course.MAX], c.avg_word_counts[Course.Q1],
             c.avg_word_counts[Course.Q2], c.avg_word_counts[Course.Q3],
             c.avg_word_counts[Course.AVG]]
        )

    write_file = open('processed-quantitative-course-data.csv', 'w')
    with write_file:
        writer = csv.writer(write_file)
        writer.writerows(data)


def write_positive_phrases(courses):
    for c in courses:
        with open('KeyPhrases/' + c.course_name + '.txt', 'w') as write_file:
            # write pos
            write_file.write('POSITIVE FEEDBACK\n\n')
            for phrase in c.q1_key_phrases:
                write_file.write(phrase)
                write_file.write('\n')

            # write neg
            write_file.write('\n\n\nNEGATIVE FEEDBACK\n\n')
            for phrase in c.q2_key_phrases:
                write_file.write(phrase)
                write_file.write('\n')



def main():
    courses = []
    read_courses(courses)
    # print_courses(courses)
    write_file(courses)
    write_positive_phrases(courses)


if __name__ == '__main__':
    main()
