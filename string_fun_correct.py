#!/usr/bin/env python3

import sys

# This is a little test program used to test the 
# grader program
# This would be a decent example of a early APCS
# program

# checks if a string is a palindrome
def check_pal(string):
    if (string != string[::-1]):
        print('Nope, "' + string + '" is not a palindrome!')
        return
    
    print('Yep! "' + string + '" is a palindrome!')

# reverses a string
def rev(string):
    print(string + ' reversed is: "' + string[::-1] + '"')

# counts occurence of a character in a string
def occurence(string, char):
    count = 0
    for c in string:
        if (c == char):
            count += 1

    print('"' + char + '" occures ' + str(count) + ' times in "' + string + '"')

# file reading code
filename = sys.argv[1]
file = open(filename, "r")
lines = file.readlines()

# reads line by line
for line in lines:
    line = line.replace("\n", "")
    
    if (not line.strip()):
        continue

    split = line.split(" ")

    if (split[1] == ""):
        print("Invalid Input")
        continue

    if (split[0] == "ispalindrome"):
        check_pal(split[1])
    elif (split[0] == "reverse"):
        rev(split[1])
    elif (split[0] == "occurenceof"):
        if (len(split) < 3):
            print("Invalid Input")
            continue
        
        occurence(split[2], split[1])
