from read_json import load_grading_data
from read_json import get_all_tests
from read_json import print_test_info
from read_json import get_language

import subprocess as sp
import os

# compiles the student's programs
def compile(prog_name, compiler, language, compressed, files):
    try:
        if (not compressed):
            if (language == "java"):
                sp.run(compiler + [prog_name], check=True, universal_newlines=True, stdout=sp.PIPE, stderr=sp.PIPE)
            elif (language == "c" or language == "haskell"):
                sp.run(compiler + ["-o", "student_exe", prog_name], check=True, universal_newlines=True, stdout=sp.PIPE, stderr=sp.PIPE)
        else:
            if (language == "java"):
                sp.run(compiler + files, check=True, universal_newlines=True) # TODO fix this, glob usage seems to not work with javac for some godforsaken reason
            elif (language == "c" or language == "haskell"):
                sp.run(compiler + ["-o", "student_exe", "*.c"], check=True, universal_newlines=True, stdout=sp.PIPE, stderr=sp.PIPE)
            
        return True
    except Exception as e:
        print(f"FATAL: Your program didn't compile! No points earned!\n{e}")
        return False

# removes compiled executables/.class files 
def remove_exe(prog_name, language, compressed):
    if (compressed and language == "java"):
        # os.remove("*.class") # probably shouldn't do *, but works for now
        pass
    elif (language == "java"):
        os.remove(prog_name.replace(".java", "") + ".class")
    elif (language == "c" or language == "haskell"):
        os.remove("student_exe")

# grades a student program
def grade(grading_json_filename, prog_name):

    compiled = False
    compressed = False
    compiler = []

    # makes sure the grading data is valid
    if (load_grading_data(grading_json_filename) == None):      
        return

    # makes sure the file is able to be run by the grader
    if (not check_extension(prog_name)):
        return

    # gets the language this assignment is written in
    language = get_language()

    compressed_output = []
    if (".zip" in prog_name):
        # actually unzip the files
        sp.run(["unzip", "-u", prog_name], stdout=sp.PIPE, universal_newlines=True, stderr=sp.PIPE)

        # get the files that were unzipped
        out = sp.run(["unzip", "-v", prog_name], stdout=sp.PIPE, universal_newlines=True, stderr=sp.PIPE) 
        compressed_output = out.stdout.split("\n")
        compressed = True
    elif (".tar" in prog_name):
        compressed = True
    
    # haskell
    if (language == "haskell"):
        compiled = True
        compiler.append("ghc")
    # c
    elif (language == "c"):
        compiled = True
        compiler.append("gcc")
    # java
    elif (language == "java"):
        compiled = True
        compiler.append("javac")

    compressed_to_compile = []
    if (compressed):
        for line in compressed_output:
            if (language == "java" and ".java" in line):
                compressed_to_compile.append(line[58:]) # oops, magic number
    
    # if the program needs to be compiled, compile it
    if (compiled and not compile(prog_name, compiler, language, compressed, compressed_to_compile)):
        return

    # prints the test info
    total_points = print_test_info()
    total_score = 0

    # runs tests and displays results
    for test in get_all_tests():
        total_score += run_test(test, prog_name, compiled, language, compressed)

    # if the langauge is compiled, remove the executable
    if (compiled):
        remove_exe(prog_name, language, compressed)

    # display over all results
    print("\n" + "=" * 10 + " Results of All Tests " + "=" * 10)
    print(f"\nYour score {total_score}/{total_points}")
    print("Your percent " + str(round(calc_percent(total_score, total_points), 2)) + "%")

# checks if program has valid extension
def check_extension(prog_name) -> bool:
    if (".py" not in prog_name and ".hs" not in prog_name and ".c" not in prog_name 
        and ".java" not in prog_name and ".zip" not in prog_name and ".tar" not in prog_name):
        print("Invalid program type, currently only Python and Haskell are supported")
        return False

    return True

# runs tests
def run_test(test, prog_name, compiled, language, compressed):
    print("\n" + "=" * 10 + f" Running test: {test.name} " + "=" * 10)

    # renames variables to make it easier to read
    points = test.points
    points_off = test.points_off_per_line
    max_points = test.max_points_off
    test_expected = test.expected_output_file

    try:
        # TODO compiler flags
        # TODO compressed (tar, zip)

        # runs python program
        if (language == "python"):
            student_exe = sp.run(["python3", prog_name] + test.arguments, check=True, universal_newlines=True, stdout=sp.PIPE, stderr=sp.PIPE)
    
        # compiles and runs a compiled language (c, haskell)
        elif (compiled):
            if (compressed and language == "java"):
                student_exe = sp.run(["java", test.main] + test.arguments, check=True, universal_newlines=True, stdout=sp.PIPE, stderr=sp.PIPE)
            elif (language == "java"):
                student_exe = sp.run(["java", prog_name.replace(".java", "")] + test.arguments, check=True, universal_newlines=True, stdout=sp.PIPE, stderr=sp.PIPE)
            elif (language == "c" or language == "haskell"):
                student_exe = sp.run(["./student_exe"] + test.arguments, check=True, universal_newlines=True, stdout=sp.PIPE, stderr=sp.PIPE)

    # student program crashed, or failed to compile
    except Exception as e:
        print(f"\nFATAL: Your program crashed! No points earned!\n{e}")
        return 0

    # determine if the program is writint to stdout or a file
    if (test.stdout):
        student_output = student_exe.stdout.split("\n")
    else:
        student_output = open(test.student_output, "r").readlines()

    # reads the expected output
    expected_output = open(test_expected, "r").readlines()
    student_score = points

    # goes through the expected output and compares the student's output
    for i in range(len(expected_output)):
        # checks for missing line at end of file/stdout
        if (i > len(student_output) - 1):
            student_score = check_score(student_score, points_off, points, max_points)
            print_error(i, expected_output[i], "<empty line>", points_off)
            continue
        
        # checks for incorrect line
        if (not check_line(student_output[i], expected_output[i])):
            student_score = check_score(student_score, points_off, points, max_points)
            print_error(i, expected_output[i], student_output[i], points_off)

    if (student_score < points - max_points):
        student_score = points - max_points

    if (student_score == points):
        print("\nNo errors! Congratulations!")

    print("\nYour score: " + str(student_score) + "/" + str(points))
    print("Your percent: " + str(round(calc_percent(student_score, points), 2)) + "%")

    return student_score

# checks and calculates a score for the student
def check_score(student_score, points_off, points, max_points):
    if (student_score - points_off > points - max_points):
        return student_score - points_off
    return 0

# calculates percentage
def calc_percent(student_score, points):
    return 100 * float(student_score) / float(points)
            
# prints error message
def print_error(num, expected, received, points_off):
    expected = expected.replace("\n", "")
    received = received.replace("\n", "")

    print(f"\nError Line #{str(num)}")
    print(f"-{str(points_off)} points")
    print(f"Expected: {expected}")
    print(f"Received: {received}")

# compares a student line to an expected line
def check_line(student_line, expected_line):
    return student_line.lower().replace("\n", "") == expected_line.lower().replace("\n", "")
    