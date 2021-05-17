#!/usr/bin/env python3
import sys
import os

from read_json import load_grading_data
from read_json import get_important_info
from os import listdir
from os.path import isfile
from os.path import isdir
from run_tests import grade

# TODO more languages

def validate_important_files(json_filename) -> bool:
    if (not isdir("info")):
        print("Error: 'info' dir not found, please create it and place any grading info there (json, input files, expected output, etc)")
        return False

    info_files = listdir("info")
    if (json_filename not in info_files):
        print(f"Error: {json_filename} not found in dir 'info'")
        return False

    load_grading_data(f"info/{json_filename}")

    for f in get_important_info():
        if (f != json_filename and f not in info_files):
            print(f"Error: {f} was provided in json info file, but was not found in dir 'info'")            
            return False

    return True

if len(sys.argv) < 2:
    print("Invalid usage: ./grader.py -help for info")
elif (sys.argv[1] == "-help"):
    print("Usage: ./grader.py <student source code> <json file>")
    print("For more info: https://github.com/jamesw98/simple-grader")
else:
    # case for wanting to grade all files in a dir
    if (len(sys.argv) > 3 and sys.argv[1] == "-d"):
        if (not validate_important_files(sys.argv[3])):
            exit(1)
        
        # loops through everything in a directory
        if (not isdir(sys.argv[2])):
            print(f"ERROR: {sys.argv[2]} is not a directory, please try again.")
        else:
            os.chdir(sys.argv[2])
            for _file in listdir(os.getcwd()):
                if (isfile(_file) and ".txt" not in _file):
                    print(f"Grading: {_file}, outputting to: {sys.argv[2]}{_file.split('.')[0]}.result.txt")
                    grade(f"../info/{sys.argv[3]}", _file, _file.split(".")[0] + ".result.txt")

    # user wants to write to a file instead of stdout
    elif (len(sys.argv) == 4 and sys.argv[1] == "-f"):
        print(f"Grading: {sys.argv[3]}, outputting to: {sys.argv[2].split('.')[0]}.result.txt")
        grade(sys.argv[3], sys.argv[2], sys.argv[2].split(".")[0] + ".result.txt")

    # standard case, grade one file, output to stdout
    else:
        grade(sys.argv[2], sys.argv[1])
        