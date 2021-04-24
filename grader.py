#!/usr/bin/env python3
import sys
from os import listdir
from os.path import isfile

from run_tests import grade

# TODO more languages

if len(sys.argv) < 2:
    print("Invalid usage: ./grader.py -help for info")
elif (sys.argv[1] == "-help"):
    print("Usage: ./grader.py <json file> <student source code>")
    print("For more info: https://github.com/jamesw98/simple-grader")
else:
    # case for wanting to grade all files in a dir
    if (len(sys.argv) > 3 and sys.argv[2] == "-d"):
        # loops through everything in a directory
        for _file in listdir(sys.argv[3]):
            if (isfile(_file) and ".txt" not in _file):
                print(f"Grading: {_file}, outputting to: {sys.argv[3]}{_file.split('.')[0]}.result.txt")
                grade(sys.argv[1], _file, sys.argv[3] + _file.split(".")[0] + ".result.txt")

    # user wants to write to a file instead of stdout
    elif (len(sys.argv) == 4 and sys.argv[1] == "-f"):
        print(f"Grading: {sys.argv[3]}, outputting to: {sys.argv[3].split('.')[0]}.result.txt")
        grade(sys.argv[2], sys.argv[3], sys.argv[3].split(".")[0] + "result.txt")

    # standard case, grade one file, output to stdout
    else:
        grade(sys.argv[1], sys.argv[2])