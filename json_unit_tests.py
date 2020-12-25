#!/usr/bin/env python3
import unittest

from read_json import *

class test_json(unittest.TestCase):
    def test_load(self):
        assert(load_grading_data("bad_1.json") == False) # empty json
        assert(load_grading_data("bad_2.json") == False) # no tests
        assert(load_grading_data("bad_3.json") == False) # empty tests

        assert(load_grading_data("test.json") == True)

if __name__ == "__main__":
    unittest.main()