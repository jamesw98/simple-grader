#!/usr/bin/env python3
import sys
from os import listdir
from os.path import isfile

from run_tests import grade

# TODO run on dir
# TODO more languages

if len(sys.argv) < 2:
    print("Invalid usage: ./grader.py -help for info")
elif (sys.argv[1] == "-help"):
    print("Usage: ./grader.py <json file> <student source code>")
    print("For more info: https://github.com/jamesw98/simple-grader")
else:
    # case for wanting to grade all files in a dir
    if (len(sys.argv) > 3 and sys.argv[2] == "-d"):
        for f in listdir(sys.argv[3]):
            if (isfile(f)):
                print("Grading: " + f)
                grade(sys.argv[1], f, sys.argv[3] + f + ".txt")
    # user wants to write to a file instead of stdout
    elif (len(sys.argv) == 4 and sys.argv[1] == "-f"):
        grade(sys.argv[2], sys.argv[3], sys.argv[3] + ".txt")
    else:
        grade(sys.argv[1], sys.argv[2])