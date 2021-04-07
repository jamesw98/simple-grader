from read_json import load_grading_data
from read_json import get_all_tests
from read_json import print_test_info

import subprocess as sp

def grade(grading_json_filename, prog_name):
    # makes sure the grading data is valid
    if (load_grading_data(grading_json_filename) == None):      
        return

    # makes sure the file is able to be run by the grader
    if (not check_extension(prog_name)):
        return

    # prints the test info
    total_points = print_test_info()

    total_score = 0

    # runs tests and displays results
    for test in get_all_tests():
        total_score += run_test(test, prog_name)

    print("\n" + "=" * 10 + " Results of All Tests " + "=" * 10)
    print(f"\nYour score {total_score}/{total_points}")
    print("Your percent " + str(round(calc_percent(total_score, total_points), 2)) + "%")

# checks if program has valid extension
def check_extension(prog_name) -> bool:
    if (".py" not in prog_name and ".hs" not in prog_name and ".pas" not in prog_name and ".c" not in prog_name):
        print("Invalid program type, currently only Python and Haskell are supported")
        return False

    return True

# runs tests
def run_test(test, prog_name):
    print("\n" + "=" * 10 + f" Running test: {test.name} " + "=" * 10)

    # renames variables to make it easier to read
    points = test.points
    points_off = test.points_off_per_line
    max_points = test.max_points_off

    test_expected = test.expected_output_file
    
    # checks for python or haskell
    if (".py" in prog_name):
        student_exe = sp.run(["python3", prog_name] + test.arguments, universal_newlines=True, stdout=sp.PIPE, stderr=sp.PIPE)
    # compiles and runs the haskell program
    elif (".hs" in prog_name):
        sp.run(["ghc", "-o", "student_exe", prog_name])
        student_exe = sp.run(["./student_exe"] + test.arguments, universal_newlines=True, stdout=sp.PIPE, stderr=sp.PIPE)
    elif (".c" in prog_name):
        sp.run(["gcc", "-o", "student_exe", prog_name])
        student_exe = sp.run(["./student_exe"] + test.arguments, universal_newlines=True, stdout=sp.PIPE, stderr=sp.PIPE)

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

    return student_score

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
    expected = expected.replace("\n", "")
    received = received.replace("\n", "")

    print(f"\nError Line #{str(num)}")
    print(f"-{str(points_off)} points")
    print(f"Expected: {expected}")
    print(f"Received: {received}")

# compares a student line to an expected line
def check_line(student_line, expected_line):
    return student_line.lower().replace("\n", "") == expected_line.lower().replace("\n", "")