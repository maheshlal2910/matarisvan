#!/usr/bin/env python
#-*- coding:utf-8 -*-

import unittest

from matarisvan.operation_graph.generation_rules import LimitOffset


class LimitOffsetTest(unittest.TestCase):
    
    def test_should_append_limit_and_offset_to_url(self):
        limit_offset = LimitOffset(limit=1, offset=0)
        processed_url = limit_offset.apply_rule_to("http://localhost%s")
        self.assertEquals('http://localhost?limit=1&offset=0', processed_url)
    
    def test_should_increase_offset(self):
        limit_offset = LimitOffset(limit=1, offset=0)
        processed_url = limit_offset.apply_rule_to("http://localhost%s")
        self.assertEquals(1, limit_offset._limit)
        self.assertEquals(1, limit_offset._offset)
