#!/usr/bin/env python
#-*- coding:utf-8 -*-

import unittest

from matarisvan.operation_graph.data_operations import Informer, DataExtractor, DataSanitizer


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


class DataSanitizerTest(unittest.TestCase):
    
    def test_shouldaccept_string_or_list(self):
        data_sanitizer = DataSanitizer('http://localhost')
        self.assertEquals('http://localhost', data_sanitizer._url_descriptor)
        data_sanitizer = DataSanitizer(['hello','world'])
        self.assertEquals(['hello', 'world'], data_sanitizer._url_descriptor)
    
    def test_shouldnt_accept_anything_other_than_list_or_string_for_url_descriptor_rest_can_be(self):
        with self.assertRaises(AssertionError):
            DataSanitizer({'hello':'world'})
    
    def test_url_described_by_should_return_url_if_set(self):
        data_sanitizer = DataSanitizer('http://localhost')
        self.assertEquals('http://localhost', data_sanitizer.url_described_by())
    
    def test_url_described_by_should_return_url_from_data_passed_in_if_descriptor_is_list(self):
        data_sanitizer = DataSanitizer(['links', 'self', 'url'])
        self.assertEquals('http://localhost', data_sanitizer.url_described_by({'links':{'self':{'url':'http://localhost'}}}))
    
    def test_url_described_by_should_throw_error_if_data_passed_in_is_none_and_descriptor_is_list(self):
        data_sanitizer = DataSanitizer(['links', 'self', 'url'])
        with self.assertRaises(AssertionError):
            data_sanitizer.url_described_by()
