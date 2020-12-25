#!/usr/bin/env python3
import json

from test import Test

all_tests = []

# prints out test info
def print_test_info():
    print("All tests run for this grader:")
    
    count = 0
    for test in all_tests:
        print(str(count) + ". " + test.name)
        print("   Points: " + str(test.points))
        print("   Input File: " + test.input_file)
        count += 1

def load_grading_data(filename) -> bool:
    if (".json" not in filename):
        print("Error: invalid file type")
        return False

    try:
        with open(filename) as f:
            data = json.load(f)
    except:
        print("Error: could not load file: '" + filename + "'")

    return validate_json(data)
    
# ensures the json is valid and adds the tests to the list of all tests
def validate_json(data) -> bool:
    if ("total_points" not in data):
        print("Error: Missing 'total_points'")
        return False

    if ("tests" not in data ):
        print("Error: 'tests' was not included")
        return False

    if (len(data["tests"]) == 0):
        print("Error: 'tests' included, but is empty")
        return False
    
    for test in data["tests"]:
        curr_test = data["tests"][test]

        if ("input_filename" not in curr_test):
            print("Error: Test: '" + test + "' does not have an input file ('input_filename')")
            return False
        
        input_filename = curr_test["input_filename"]
        
        if ("expected_output_filename" not in curr_test):
            print("Error: Test: '" + test + "' does not have an expected output file ('expected_output_filename')")
            return False

        expected_output_filename = curr_test["expected_output_filename"]
        
        if ("points" not in curr_test):
            print("Error: Test: '" + test + "' does not have a point value")

        points = curr_test["points"]
        
        if ("points_off_per_wrong_line" not in curr_test):
            print("Warning: 'points_off_per_wrong_line' missing, defaulting to '1'")
            points_per_line = 1
        else:
            points_per_line = curr_test["points_off_per_wrong_line"]

        if ("max_points_off" not in curr_test):
            print("Warning: 'max_points_off' missing, defaulting to 'points'/2")
            max_off = points // 2
        else:
            max_off = curr_test["max_points_off"]

        all_tests.append(Test(test, points, input_filename, expected_output_filename, points_per_line, max_off))
    
    return True