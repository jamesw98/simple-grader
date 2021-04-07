# Simple Grader
## A simple grading tool written in Python
### Introduction
This tool lets graders grade a programs written by students in a variety of languages (supported languages below), assuming the system you are running the grading script on has the compilers installed. It will print the results to `stdout`, but you can always pipe it to a file. I plan on adding writing results to a file soon. 
### How to Use
Start by writing a JSON file with info on grading, here is a simple template (`test.json` in this git repo):  
```json
{
    "language": "python",
    "arguments": true,
    "tests": {
        "test_basic": {
            "input_filename": "test_file_1.txt",
            "expected_output_filename": "exp_output_1.txt",
            "args": ["test_file_1.txt"],
            "points": 110,
            "points_off_per_wrong_line": 10,
            "max_points_off": 100
        }
    }
}
```
This file has the minimum required data if the program you are grading takes input from a file, whose name is passed in `stdin` (currently the only supported means of input)
### Supported Languages
* Python3
* C
* Haskell
* Pascal