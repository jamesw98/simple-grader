from read_json import load_grading_data
from read_json import get_all_tests
from read_json import print_test_info

import subprocess as sp

def grade(grading_json_filename, exe_name):
    if (load_grading_data(grading_json_filename) == None):      
        return

    if (".py" not in exe_name and ".hs" not in exe_name):
        print("Invalid program type, currently only Python and Haskell are supported")
        return

    print_test_info()

    for test in get_all_tests():
        run_test(test, exe_name)

# runs tests
def run_test(test, exe_name):
    print(f"\nRunning test: {test.name}")

    # renames variables to make it easier to read
    points = test.points
    points_off = test.points_off_per_line
    max_points = test.max_points_off

    test_filename = test.input_file
    test_expected = test.expected_output_file
    
    # checks for python or haskell
    if (".py" in exe_name):
        student_exe = sp.run(["python3", exe_name, test_filename], universal_newlines=True, stdout=sp.PIPE, stderr=sp.PIPE)
    # compiles and runs the haskell program
    else:
        sp.run(["ghc", "-o", "student_exe", exe_name])
        student_exe = sp.run(["./student_exe"], universal_newlines=True, stdout=sp.PIPE, stderr=sp.PIPE)

    # determine if the program is writint to stdout or a file
    if (test.stdout):
        student_output = student_exe.stdout.split("\n")
    else:
        student_output = open(test.student_output, "r").readlines()

    # reads the expected output
    expected_output = open(test_expected, "r").readlines()
    student_score = points

    # goes through the expected output and compares the student's output
    for i in range(len(expected_output)):
        # checks for missing line at end of file/stdout
        if (i > len(student_output) - 1):
            student_score = check_score(student_score, points_off, points, max_points)
            print_error(i, expected_output[i], "<empty line>", points_off)
            continue
        
        # checks for incorrect line
        if (not check_line(student_output[i], expected_output[i])):
            student_score = check_score(student_score, points_off, points, max_points)
            print_error(i, expected_output[i], student_output[i], points_off)

    if (student_score < points - max_points):
        student_score = points - max_points

    if (student_score == points):
        print("\nNo errors! Congratulations!")

    print("\nYour score: " + str(student_score) + "/" + str(points))
    print("Your percent: " + str(round(calc_percent(student_score, points), 2)) + "%")

# checks and calculates a score for the student
def check_score(student_score, points_off, points, max_points):
    if (student_score - points_off > points - max_points):
        return student_score - points_off
    return 0

# calculates percentage
def calc_percent(student_score, points):
    return 100 * float(student_score) / float(points)
            
# prints error message
def print_error(num, expected, received, points_off):
    print(f"\nError Line #{str(num)}")
    print(f"- {str(points_off)} points")
    print(f"Expected: {expected[:-1]}")
    print(f"Received: {received[:-1]}")

# compares a student line to an expected line
def check_line(student_line, expected_line):
    return student_line.lower().replace("\n", "") == expected_line.lower().replace("\n", "")