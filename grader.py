#!/usr/bin/env python3
import sys

from run_tests import grade

if len(sys.argv) < 2:
    print("Invalid usage: ./grader.py -help for info")
elif (sys.argv[1] == "-help"):
    print("Usage: ./grader.py <json file> <student source code>")
    print("For more info: https://github.com/jamesw98/simple-grader/tree/master")
else:
    grade(sys.argv[1], sys.argv[2])