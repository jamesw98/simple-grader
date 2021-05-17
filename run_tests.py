from read_json import load_grading_data
from read_json import get_all_tests
from read_json import print_test_info
from read_json import get_language
from read_json import get_flags
from read_json import get_generator_info

import subprocess as sp
import os

VALID_SUBMISSION_TYPES = ["py", "hs", "c", "java", "rb", "pas","tar", "zip"]

"""
grades a student's submission
PARAMS  
    grading_json_filename: the json info file for this grading suite
    sub_name: name of the submission (c01.c, p2.hs, threadpool.tar, etc)
    output_file_name: defaults to None, if this isn't None, this is the file to write the output
                      of grading the submission to
"""
def grade(grading_json_filename, sub_name, output_file_name=None):

    output_file = None
    reference_solution = None

    compiled = False
    compressed = False

    compiler = []

    # sets output file if it is being used
    if(output_file_name):
        output_file = open(output_file_name, "w")

    # makes sure the grading data is valid
    if (load_grading_data(grading_json_filename) == None):      
        return

    # makes sure the file is able to be run by the grader
    if (not check_extension(sub_name)):
        return

    # gets the language this assignment is written in
    language = get_language()

    # used for compiling compressed output
    compressed_output = []
    compressed_to_compile = []

    # unzips a compressed submission
    if (".zip" in sub_name):
        # make a temporary directory
        os.mkdir("sg_temp")

        # actually unzip the files
        run_command(["unzip", "-u", sub_name, "-d", "sg_temp/"])

        # get the files that were unzipped
        compressed_output = run_command(["unzip", "-v", sub_name]).stdout.split("\n")
        compressed = True
    
    # untars a compressed submission
    elif (".tar" in sub_name):
        # make a temporary directory
        os.mkdir("sg_temp")

        # untar the files into a dir called "sg_temp"
        out = run_command(["tar", "-xvf", sub_name, "-C", "sg_temp/"])

        # get the files to compile
        compressed_to_compile = out.stdout.split("\n")[:-1] # this always includes one extra line, so strip that one off
        compressed = True

    # get the java files to compile
    # since globs don't work with subprocess for some reason, I can't just do 'sp.run(javac *.java')
    # this doesn't need to be run for tar files, since the output from `tar -xvf` is just the files in the tar
    if (compressed and ".zip" in sub_name and language == "java"):
        for line in compressed_output:
            if (".java" in line):
                compressed_to_compile.append(line[58:]) # oops, magic number, strips the filenames out of `unzip -v`
    
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
    # pascal
    elif (language == "pascal"):
        compiled = True
        compiler.append("fpc")

    # if the program needs to be compiled, compile it
    if (compiled and not compile(sub_name, compiler, language, compressed, compressed_to_compile, get_flags(), output_file)):
        return

    # get generator info, if there is any
    gen_info = get_generator_info()
    if (gen_info):
        # generate an input file
        original_dir = os.getcwd()
        os.chdir("../info/")
        run_command([f"./{gen_info[0]}"] + gen_info[2])
        reference_solution = gen_info[1]
        os.chdir(original_dir)

    # prints the test info
    total_points = print_test_info(output_file)
    total_score = 0

    # runs tests and displays results
    for test in get_all_tests():
        if (test.stdin):
            total_score += run_test_stdin(test, sub_name, compiled, language, compressed, reference_solution, output_file)
        else:
            total_score += run_test(test, sub_name, compiled, language, compressed, reference_solution, output_file)

    # if the langauge is compiled, remove the executable
    if (compiled and not compressed):
        remove_exe(sub_name, language)

    # if the submission was compressed, clean and remove the temp directory
    if (compressed):
        clean_temp_dir()

    # display final grade info from all tests
    output("\n" + "=" * 10 + " Results of All Tests " + "=" * 10, output_file)
    output(f"\nYour score {total_score}/{total_points}", output_file)
    output("Your percent " + str(round(calc_percent(total_score, total_points), 2)) + "%", output_file)

"""
compiles a student's submission, currently supports java, c, and haskell
PARAMS:
    sub_name:    name of the submission (c01.c, p2.hs, threadpool.tar, etc)
    compiler:    the compiler being used (javac, gcc, or ghc)
    language:    the language being used for this submission
    compressed:  whether or not the submission was compressed
    files:       if the file was compressed, this is a list of the files to be compiled for this submission
    flags:       a list of compiler flags to be used for compilation, can be empty
    output_file: defaults to None, if it isn't None, any output from compilation will be written here (this will only happen if the program fails to compile)
"""
def compile(sub_name, compiler, language, compressed, files, flags, output_file=None):
    # attempts to compile the submission
    try:
        # used for compression, get the current directory
        orig_dir = os.getcwd()

        # checks for compression
        if (not compressed):
            if (language == "java"):
                run_command(compiler + [sub_name])
            elif (language == "c" or language == "haskell"):
                run_command(compiler + ["-o", "student_exe", sub_name] + flags)
            elif (language == "pascal"):
                run_command(compiler + [sub_name] + flags)
        else:
            # move to the temp directory
            os.chdir("sg_temp")
            if (language == "java"):
                run_command(compiler + files)
            elif (language == "c" or language == "haskell"):
                run_command(compiler + ["-o", "student_exe", "*.c"])
            # go back to the original directory
            os.chdir(orig_dir)

        return True

    # if the program crashed, write a message and award no points
    except Exception as e:
        os.chdir(orig_dir)
        output(f"FATAL: Your program didn't compile! No points earned!\n{e}", output_file)
        return False

"""
runs the student submission on a certain test and compares the output from the student to the expected output
PARAMS:
    test:        a test object containing all the info needed to run the test
    sub_name:    the name of the submission
    compiled:    whether or not the submission was compiled
    language:    the language of the submission
    compressed:  whether or not the submission was compressed 
    output_file: defaults to None, if it isn't None, write all output to this file instead of stdout

RETURNS:
    the student's score on the test that was run
"""
def run_test(test, sub_name, compiled, language, compressed, ref_sol, output_file=None):
    if (ref_sol):
        sp.run([f"./{ref_sol}"], check=True, universal_newlines=True, stdout=sp.PIPE, stderr=sp.PIPE)

    output("\n" + "=" * 10 + f" Running test: {test.name} " + "=" * 10, output_file)

    points = test.points
    points_off = test.points_off_per_line
    max_points = test.max_points_off
    test_expected = test.expected_output_file
    input_lines = open(f"../info/{test.input_file}", "r").readlines()

    try:
        # if compression was used, move into the temp dir
        if (compressed):
            orig_dir = os.getcwd()
            os.chdir("sg_temp")

        # runs python program
        if (language == "python"):
            if (not compressed):
                student_exe = run_command(["python3", sub_name] + test.arguments)
            else:
                student_exe = run_command(["python3", f"{test.main}"] + test.arguments)
        # runs the ruby program
        elif (language == "ruby"):
            if (not compressed):
                student_exe = run_command(["ruby", sub_name] + test.arguments)
            else:
                student_exe = run_command(["ruby", f"{test.main}"] + test.arguments)
            
        # compiles and runs a compiled language (c, haskell)
        elif (compiled):
            # if the submission was compressed, run the main file
            if (compressed and language == "java"):
                student_exe = run_command(["java", test.main] + test.arguments)
            # if the submission is only one java file, run the one file
            elif (language == "java"):
                student_exe = run_command(["java", sub_name.replace(".java", "")] + test.arguments)
            # if the language is c or haskell, run the compiled executable
            elif (language == "c" or language == "haskell"):
                student_exe = run_command(["./student_exe"] + test.arguments)
            
        # if compression was used, move back to original dir
        if (compressed):
            os.chdir(orig_dir)

    # student program crashed, or failed to compile
    except Exception as e:
        if (compressed):
            os.chdir(orig_dir)

        output(f"\nFATAL: Your program crashed! No points earned!\n{e}", output_file)
        return 0

    # determine if the program is writint to stdout or a file
    if (test.stdout):
        student_output = student_exe.stdout.split("\n")
    else:
        student_output = open(test.student_output, "r").readlines()

    # reads the expected output
    expected_output = open(f"../info/{test_expected}", "r").readlines()
    student_score = points

    # goes through the expected output and compares the student's output
    for i in range(len(expected_output)):
        # checks for missing line at end of file/stdout
        if (i > len(student_output) - 1):
            student_score = check_score(student_score, points_off, points, max_points)
            print_error(i, expected_output[i], "<empty line>", points_off, input_lines, output_file)
            continue
        
        # checks for incorrect line
        if (not check_line(student_output[i], expected_output[i])):
            student_score = check_score(student_score, points_off, points, max_points)
            print_error(i, expected_output[i], student_output[i], points_off, input_lines, output_file)

    # if the student got more points off than the max points, reset the score
    if (student_score < points - max_points):
        student_score = points - max_points
        
    # special message for 100%
    elif (student_score == points):
        output("\nNo errors! Congratulations!\n", output_file)

    output("\nYour score: " + str(student_score) + "/" + str(points), output_file)
    output("Your percent: " + str(round(calc_percent(student_score, points), 2)) + "%", output_file)

    return student_score

def run_test_stdin(test, sub_name, compiled, language, compressed, reference_solution, output_file):
    output("\n" + "=" * 10 + f" Running test: {test.name} " + "=" * 10, output_file)

    points = student_score = test.points
    points_off = test.points_off_per_line
    max_points = test.max_points_off

    input_lines = open(f"../info/{test.input_file}", "r").readlines()

    line_num = 1
    for line in input_lines:
        try:
            # if compression was used, move into the temp dir
            if (compressed):
                orig_dir = os.getcwd()
                os.chdir("sg_temp")

            if (language == "pascal"):
                ref_output = run_command_with_stdin([f"../info/{reference_solution.split('.')[0]}"], line).stdout
                stu_output = run_command_with_stdin([f"./{sub_name.split('.')[0]}"], line).stdout

                if (not check_line(stu_output, ref_output)):
                    student_score = check_score(student_score, points_off, points, max_points)
                    print_error(line_num, ref_output, stu_output, points_off, input_lines, output_file)

                if (student_score < points - max_points):
                    student_score = points - max_points
                            
            # if compression was used, move back to original dir
            if (compressed):
                os.chdir(orig_dir)

        # student program crashed, or failed to compile
        except Exception as e:
            if (compressed):
                os.chdir(orig_dir)

            output(f"\nFATAL: Your program crashed! No points earned!\n{e}", output_file)
            return 0

    return student_score

"""
checks and calculates a student's score
PARAMS:
    student_score: the students score
    points_off:    the points being deducted
    max_points:    the max number of points that can be lost

RETURNS:
    the student's score
"""
def check_score(student_score, points_off, points, max_points):
    if (student_score - points_off > points - max_points):
        return student_score - points_off
    return 0

"""
calculates a percentage score
PARAMS:
    student_score: the student's score
    points:        the max points for this test

RETURNS:
    a percentage value grade
"""
def calc_percent(student_score, points):
    return 100 * float(student_score) / float(points)
            
"""
prints an error message when a student output line doesn't match an expected line
PARAMS:
    num:         the current line number in the input file
    expected:    the expected output for this line
    received:    the received output from the student submission for this line
    points_off:  the points off per line
    input_lines: a list of all the input lines, used to display to the student what line of input caused an incorrect output
    output_file: defaults to None, if this isn't None, write all output to this file instead of stdout
"""
def print_error(num, expected, received, points_off, input_lines, output_file=None):
    expected = expected.replace("\n", "")
    received = received.replace("\n", "")

    if ("\n" in input_lines[num]):
        line = input_lines[num].replace("\n", "")
    else:
        line = input_lines[num]

    output(f"\nError Line #{str(num)} -{str(points_off)} points\n", output_file)
    output(f"Input:    {line}", output_file)
    output(f"Expected: {expected}", output_file)
    output(f"Received: {received}", output_file)

"""
determines what kind of output to use and writes to it
PARAMS:
    string:      the string to output
    output_file: if this is None or empty this will write to stdout, else, it will write to this file
"""
def output(string, output_file):
    if (output_file):
        output_file.write(f"{string}\n")
    else:
        print(string)

"""
checks the extension of a submission
PARAM:
    sub_name: the name of the submission

RETURN:
    true if the submission is valid, false if not
"""
def check_extension(sub_name) -> bool:
    if (sub_name.split(".")[1] not in VALID_SUBMISSION_TYPES):    
        return False
    return True

"""
checks a student outputted line
PARAM:
    student_line:  the line the student's submission outputted
    expected_line: the expected output's line
"""
def check_line(student_line, expected_line):
    return student_line.lower().replace("\n", "") == expected_line.lower().replace("\n", "")

"""
cleans up the temp directory and removes it
"""
def clean_temp_dir():
    for f in os.listdir("sg_temp"):
        os.remove(f"sg_temp/{f}")
    os.removedirs("sg_temp")

"""
this is just a rewrite so I don't have multiple super long lines
PARAMS:
    args: the arguments to pass to subprocess

RETURNS:
    subprocess object
"""
def run_command(args):
    return sp.run(args, check=True, universal_newlines=True, stdout=sp.PIPE, stderr=sp.PIPE)
    # return sp.run(args, check=True, universal_newlines=True, stderr=sp.PIPE)

def run_command_with_stdin(args, stdin):
    return sp.run(args, check=True, universal_newlines=True, stdout=sp.PIPE, stderr=sp.PIPE, input=stdin, shell=True)

"""
removes the compiled executable for a submission
PARAMS:
    sub_name: the name of the submission
    language: the language of the submission
"""
def remove_exe(sub_name, language):
    if (language == "java"):
        os.remove(sub_name.replace(".java", "") + ".class")
    elif (language == "c" or language == "haskell"):
        os.remove("student_exe")