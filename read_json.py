#!/usr/bin/env python3
import json

ERROR_START = "Error: Test: '"

all_tests = []
language = []
flags = []

# gets all the test
def get_all_tests():
    return all_tests

# prints out test info, returns the max points
def print_test_info(output_file):
    if (output_file):
        output_file.write("Tests to be run:\n")
    else:
        print("Tests to be run:")

    total_points = 0
    
    count = 0
    for test in all_tests:
        if (output_file):
            output_file.write(str(count) + ". " + test.name + "\n")
            output_file.write("   Points: " + str(test.points) + "\n")
            output_file.write("   Input File: " + test.input_file + "\n")
        else:
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

def get_language():
    return language[0]

def get_flags():
    return flags

# ensures the json is valid and adds the tests to the list of all tests
# returns true if everything is valid, false is something is wrong
def validate_json(data) -> bool:
    stdout = True
    main = ""

    language.append(data["language"])

    if ("flags" in data):
        for f in data["flags"]:
            flags.append(f)

    # ensures proper formatting for the base json
    # tests
    if ("tests" not in data):
        print("Error: 'tests' was not included")
        return False

    # makes sure there actually are tests
    if (len(data["tests"]) == 0):
        print("Error: 'tests' included, but is empty")
        return False
    
    # checks if stdout is specified
    if ("stdout" not in data):
        print("Warning: Missing 'stdout', defaulting to 'true'")
    else: 
        if (not data["stdout"]):
            stdout = False
        if (not data["stdout"] and "student_output" not in data):
            print("Error: 'student_output' missing while 'stdout' is false is not valid")
            return False
    
    # checks if the submission is compressed (zip/tar)
    if ("compressed" in data):
        if (data["compressed"] and data["language"] == "java" and "main" not in data):
            print("Error for compressed Java submissions, you must also have a 'main' field in the json file")
            return False
        else:   
            main = data["main"]

    # checks each test
    for test in data["tests"]:
        # gets the current test
        curr_test = data["tests"][test]

        # make sure there is an input filename, so it knows what to report so the student can check
        if ("input_filename" not in curr_test):
            print(f"{ERROR_START} {test}' does not have an input file ('input_filename')")
            return False
        
        input_filename = curr_test["input_filename"]
        
        # makes sure there is an expected output file
        if ("expected_output_filename" not in curr_test):
            print(f"{ERROR_START} {test}' does not have an expected output file ('expected_output_filename')")
            return False

        expected_output_filename = curr_test["expected_output_filename"]
        
        # makes sure each test has a point value
        if ("points" not in curr_test):
            print("{ERROR_START} {test}' does not have a point value")
            return False

        points = curr_test["points"]

        # if there are arguments, add them
        if ("args" in curr_test):
            args = curr_test["args"]      
        else:
            args = []
        
        # makes sure there are points off per line specified
        if ("points_off_per_wrong_line" not in curr_test):
            print(f"{ERROR_START} {test}' does not have 'points_off_per_wrong_line'")
            return False

        points_per_line = curr_test["points_off_per_wrong_line"]

        # checks if max points off was specified, if not, defaults to the total points for that test
        if ("max_points_off" not in curr_test):
            print("Warning: 'max_points_off' missing, defaulting to 'points'")
            max_off = points
        else:
            max_off = curr_test["max_points_off"]
        
        # if the program writes to stdout, student output doesn't matter
        if (stdout):
            student_output = ""
        # if the program writes to a file, gets the file
        else:
            student_output = data["student_output"]

        # adds the test
        all_tests.append(Test(test, points, input_filename, expected_output_filename, points_per_line, max_off, stdout, student_output, args, main))
    
    return True

class Test:
    def __init__(self, name, points, input_file, expected_output_file,
                 points_off_per_line, max_points_off, stdout, student_output, arguments, main):
        self.name = name # test name
        self.points = points # points for this test
        self.input_file = input_file # the name for the input file 
        self.expected_output_file = expected_output_file # name of the expected output file
        self.points_off_per_line = points_off_per_line # points taken off for incorrect line
        self.max_points_off = max_points_off # maximum point deduction
        self.stdout = stdout # whether or not the program writes to stdout
        self.student_output = student_output # the student output file (if not writing to stdout)
        self.arguments = arguments # the arguments for the program (if any)
        self.main = main # the main program name (for java programs given in a compressed file)