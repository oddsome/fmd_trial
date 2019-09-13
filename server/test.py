#!/usr/bin/env python3

import unittest

from server import sint, process_posts_query
from math import isnan

class PostsTests(unittest.TestCase):

    def testSint(self) :
        """integer conversion tests"""
        assert isnan(sint("wtf")), "incorrect string handling"
        assert 42 == sint("42"), "obviously wrong conversion"
        assert isnan(sint(None)), "None isn't NaN"
    
    def testProcessPostsQuery(self) :
        """query processing sanity check"""
        data = [
            {"title": "z"},
            {"title": "a"},
            {"title": "b"},
            {"title": "c"},
            {"title": "d"}
        ]
        assert [] == process_posts_query(data, "", "", 0, 0), "empty (1) not empty"
        assert [] == process_posts_query(data, "", "", 5, -100), "empty (2) not empty"
        assert 2 == len(process_posts_query(data, "", "", 0, 2)), "improper count (1)"
        assert 2 == len(process_posts_query(data, "", "", 1, 2)), "improper count (1)"
        f, *_ = process_posts_query(data, "title", "desc", 0, 10)
        assert f == {"id" : 1, "title" : "z"} , "wrong sorting (1)"
        f, *_ = process_posts_query(data, "title", "asc", 0, 10)
        assert f == {"id" : 1, "title" : "a"} , "wrong sorting (1)"

if __name__ == "__main__" :
    unittest.main()
    