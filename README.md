# Simple Grader
### Introduction
This tool lets graders grade a programs written by students in a variety of languages (supported languages below), assuming the system you are running the grading script on has the compilers installed. It will print the results to `stdout`, but you can always pipe it to a file. I plan on adding writing results to a file soon. 
### How to Use: Simple Example
Start by writing a JSON file with info on grading, here is a simple template (`test.json` in this git repo):  
```json
{
    "language": "python",
    "arguments": true,
    "stdout": true,
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
This file has the minimum required data if the program you are grading takes input from a file, whose name is passed in `stdin` (currently the only supported means of input). This specific test json was written for the `string_fun_*.py` files, which are in this repo. These files output to `stdout`, so the grader captures that and compares the output to the file `exp_output_1.txt`. Output looks like this, depending on if you run the correct or wrong string fun file:  
**Correct**
```
Tests to be run:
0. test_basic
   Points: 110
   Input File: test_file_1.txt

========== Running test: test_basic ==========

No errors! Congratulations!

Your score: 110/110
Your percent: 100.0%

========== Results of All Tests ==========

Your score 110/110
Your percent 100.0%
```
**Wrong**
```
Tests to be run:
0. test_basic
   Points: 110
   Input File: test_file_1.txt

========== Running test: test_basic ==========

Error Line #5
-10 points
Expected: cat reversed is: "tac"
Received: cat reversed is: "cat"

Error Line #9
-10 points
Expected: "A" occures 0 times in "attack"
Received: "A" occures 1 times in "attack"

Error Line #10
-10 points
Expected: "a" occures 2 times in "attack"
Received: "a" occures 3 times in "attack"

Your score: 80/110
Your percent: 72.73%

========== Results of All Tests ==========

Your score 80/110
Your percent 72.73%
```  
Yes, test numbers start at 0, to quote one of my professors, "All goodhearted people start counting at 0."  
### How to Use: Multiple Tests
If you want to have more than one test per run, you can construct your json file like this:  
```json
{
    "language": "c", 
    "stdout": true,
    "arguments": true,  
    "tests": {
        "test_basic": {
            "input_filename": "test.txt",
            "expected_output_filename": "test.txt",
            "args": ["test.txt"],
            "points": 40,
            "points_off_per_wrong_line": 10,
            "max_points_off": 40
        },
        "test_ryan": {
            "input_filename": "test_2.txt",
            "expected_output_filename": "test_2.txt",
            "args": ["test_2.txt"],
            "points": 90,
            "points_off_per_wrong_line": 10,
            "max_points_off": 90
        },
        "test_gman": {
            "input_filename": "test_3.txt",
            "expected_output_filename": "test_3.txt",
            "args": ["test_3.txt"],
            "points": 90,
            "points_off_per_wrong_line": 10,
            "max_points_off": 90
        }
    }
}
```
This json file (`args_test.json`) with the corresponding txt files and the c file that this was made to grade (`args_test.c` and `args_test_wrong.c`) are included in this repo
### Supported Languages
* Python
* C
* Haskell
* Pascal