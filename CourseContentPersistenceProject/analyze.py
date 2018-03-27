#! usr/bin/env python3
from src import _mypath
from course import Course

files = {"course": "Course.tsv",
         "readings": "Readings.tsv",
         "videos": "Videos.tsv",
         "output": "Output.tsv"
        }
courses_dir = "courses/"
analysis_dir = "analysis/"
course_paths = [
                "A/",
                "B/",
                "C/"
             ]
output_labels = ("course\tcoordinator\tage diff\ttotal score\treading score\t"
                  "video score\n")


def run_analysis():
    # Erase previous output file contents and write column headings
    with open(analysis_dir + files["output"], 'w') as output_file:
        output_file.write(output_labels)

        for fp in course_paths:
            curr_course = Course(courses_dir + fp, files)
            curr_course.score()
            curr_course.calc_age_gap()
            row = [
                    curr_course.course_title,
                    curr_course.coordinator,
                    curr_course.age_gap,
                    curr_course.full_score,
                    curr_course.read_score,
                    curr_course.vid_score
                  ]
            for item in row:
                output_file.write(str(item) + '\t')
                # output_file.write('\t')
            output_file.write('\n')
            # output_file.writerow(row)
            # print(row)


def main():
    run_analysis()


if __name__ == '__main__':
    main()
