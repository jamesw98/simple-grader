# Simple Grader
## Introduction
This tool lets graders grade a programs written by students in a variety of languages (supported languages below), assuming the system you are running the grading script on has the compilers installed. It will print the results to `stdout`, but you can always pipe it to a file. I plan on adding writing results to a file soon. 
## How to Use
### Simple Example
Start by writing a JSON file with info on grading, here is a simple template (`examples/test.json` in this git repo):  
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
This file has the minimum required data if the program you are grading takes input from a file, whose name is passed in `stdin` (currently the only supported means of input). This specific test json was written for the `examples/string_fun_*.py` files, which are in this repo. These files output to `stdout`, so the grader captures that and compares the output to the file `examples/exp_output_1.txt`. Run the grader with a command formatted like this:  
```
./grader.py <json file name> <student source code>
```  
Output looks like this, depending on if you run the correct or wrong string fun file:  
 
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
### Multiple Tests
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
This json file (`examples/args_test.json`) with the corresponding txt files and the c file that this was made to grade (`examples/args_test.c` and `examples/args_test_wrong.c`) are included in this repo. The output will look like this: 
```
Tests to be run:
0. test_basic
   Points: 40
   Input File: test.txt
1. test_ryan
   Points: 90
   Input File: test_2.txt
2. test_gman
   Points: 90
   Input File: test_3.txt

========== Running test: test_basic ==========

No errors! Congratulations!

Your score: 40/40
Your percent: 100.0%

========== Running test: test_ryan ==========

No errors! Congratulations!

Your score: 90/90
Your percent: 100.0%

========== Running test: test_gman ==========

No errors! Congratulations!

Your score: 90/90
Your percent: 100.0%

========== Results of All Tests ==========

Your score 220/220
Your percent 100.0%
```
### Crashing/Not Compiling Checking
The grader will also check if the student's program crashes or fails to compile. Here is some output of a version of `examples/args_test.c` that segfaults on tests 1 and 2: 
```
Tests to be run:
0. test_basic
   Points: 40
   Input File: test.txt
1. test_ryan
   Points: 90
   Input File: test_2.txt
2. test_gman
   Points: 90
   Input File: test_3.txt

========== Running test: test_basic ==========

No errors! Congratulations!

Your score: 40/40
Your percent: 100.0%

========== Running test: test_ryan ==========

FATAL: Your program crashed or didn't compile! No points earned!
Command '['./student_exe', 'test_2.txt']' died with <Signals.SIGSEGV: 11>.

========== Running test: test_gman ==========

FATAL: Your program crashed or didn't compile! No points earned!
Command '['./student_exe', 'test_3.txt']' died with <Signals.SIGSEGV: 11>.

========== Results of All Tests ==========

Your score 40/220
Your percent 18.18%
```
### Compressed Submissions
The grader can also take `.tar` and `.zip` compressed files as submissions. The grader will then unpack them, and compile the files inside based on the language. For example, `test.zip` and `test.tar` have two files in them, `tri_main.java` and `triangle.java`. If you are using a compressed submission that has Java as the language, you will also have to specify a "main" so the grader knows what class contains the main function. This is not required for other supported languages. Here is an example of a compressed submission json:
```json
{
    "language": "java", 
    "compressed": true,
    "stdout": true,
    "arguments": false,  
    "main": "tri_main",
    "tests": {
        "test_basic": {
            "input_filename": "test.txt",
            "expected_output_filename": "test_zip.txt",
            "args": [""],
            "points": 40,
            "points_off_per_wrong_line": 10,
            "max_points_off": 40
        }
    }
}
```
This would work for both `.tar` and `.zip` submissions.
## Supported Languages/Submission Formats
### Languages
* Python
* C
* Haskell
* Java
### Submission Formats
* Single File (.py, .c, .hs, etc)
* .tar
* .zip
