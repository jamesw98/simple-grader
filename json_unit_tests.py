#!/usr/bin/env python3
import unittest

from read_json import *

class test_json(unittest.TestCase):
    def test_load(self):
        assert(load_grading_data("testfiles/bad_1.json") == []) # empty json
        assert(load_grading_data("testfiles/bad_2.json") == []) # no tests
        assert(load_grading_data("testfiles/bad_3.json") == []) # empty tests
        assert(load_grading_data("testfiles/bad_4.json") == []) # no input filename
        assert(load_grading_data("testfiles/bad_5.json") == []) # no expected output filename
        assert(load_grading_data("testfiles/bad_6.json") == []) # no points for test

        assert(len(load_grading_data("testfiles/bad_7.json")) == 1) # returns a list with one test 
        assert(len(load_grading_data("testfiles/test.json")) == 2) # returns a list with two tests

if __name__ == "__main__":
    unittest.main()