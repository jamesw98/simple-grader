#!/usr/bin/env python3
import json

from test import Test

ERROR_START = "Error: Test: '"

all_tests = []

# gets all the test
def get_all_tests():
    return all_tests

# prints out test info
def print_test_info():
    print("Tests to be run:")

    total_points = 0
    
    count = 0
    for test in all_tests:
        print(str(count) + ". " + test.name)
        print("   Points: " + str(test.points))
        print("   Input File: " + test.input_file)
        count += 1
        total_points += test.points

    return total_points
    
    

# loads the grading data from a json file
# returns None on failure, a list of tests on success 
def load_grading_data(filename):
    all_tests.clear()
    if (".json" not in filename):
        print("Error: invalid file type")
        return False

    try:
        with open(filename) as f:
            data = json.load(f)
            if not validate_json(data):
                return None
            return all_tests
    except Exception as e:
        print(e)
        print("Error: could not load file: '" + filename + "'")
        return None

    
# ensures the json is valid and adds the tests to the list of all tests
# returns true if everything is valid, false is something is wrong
def validate_json(data) -> bool:
    stdout = True

    if ("tests" not in data):
        print("Error: 'tests' was not included")
        return False

    if (len(data["tests"]) == 0):
        print("Error: 'tests' included, but is empty")
        return False
    
    if ("arguments" not in data):
        print("Error: 'arguments' not included")
        return False
    
    if ("stdout" not in data):
        print("Warning: Missing 'stdout', defaulting to 'true'")
    else: 
        if (not data["stdout"]):
            stdout = False
        if (not data["stdout"] and "student_output" not in data):
            print("Error: 'student_output' missing while 'stdout' is false is not valid")
            return False

    for test in data["tests"]:
        curr_test = data["tests"][test]

        if ("input_filename" not in curr_test):
            print(f"{ERROR_START} {test}' does not have an input file ('input_filename')")
            return False
        
        input_filename = curr_test["input_filename"]
        
        if ("expected_output_filename" not in curr_test):
            print(f"{ERROR_START} {test}' does not have an expected output file ('expected_output_filename')")
            return False

        expected_output_filename = curr_test["expected_output_filename"]
        
        if ("points" not in curr_test):
            print("{ERROR_START} {test}' does not have a point value")
            return False

        points = curr_test["points"]

        if ("arguments" in data):
            if ("args" not in curr_test):
                print(f"{ERROR_START} {test} does not have arguments")
                return False

            args = curr_test["args"]      
        else:
            args = []
        
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
        
        if (stdout):
            student_output = ""
        else:
            student_output = data["student_output"]

        all_tests.append(Test(test, points, input_filename, expected_output_filename, points_per_line, max_off, stdout, student_output, args))
    
    return True