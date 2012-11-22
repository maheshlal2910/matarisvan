#!/usr/bin/env python
#-*- coding:utf-8 -*-

import unittest

from matarisvan.operation_graph.data_operations import Informer, DataExtractor


class DataExtractorTest (unittest.TestCase):
    
    def test_should_set_params(self):
        data_extractor = DataExtractor({'id':'some_id'}, {'name': 'name_val'}, {})
        self.assertEquals({'id':'some_id'}, data_extractor._model_id_mapping)
        self.assertEquals({'name': 'name_val'}, data_extractor._model_data_mapping)
    
    def test_should_augment_id_with_defaults(self):
        data_extractor = DataExtractor({'id':'some_id'}, {'name': 'name_val'}, {'type': 'node_type'})
        self.assertEquals({'id':'some_id', 'type': 'node_type'}, data_extractor._model_id_mapping)
        
    def test_should_accept_only_dicts(self):
        with self.assertRaises(AssertionError):
            DataExtractor([], {'name': 'name_val'}, {})
        with self.assertRaises(AssertionError):
            DataExtractor({'id':'some_id'}, [], {})
        with self.assertRaises(AssertionError):
            DataExtractor({'id':'some_id'}, {'name': 'name_val'}, [])
