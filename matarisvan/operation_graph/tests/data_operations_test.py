#!/usr/bin/env python
#-*- coding:utf-8 -*-

import unittest

from mock import Mock
from mock import patch

import base64, urllib2, ast

from matarisvan.operation_graph. data_operations import Informer, DataExtractor, UrlExtractor, DataSanitizer
from matarisvan.operation_graph.tests.test_data import user_test_data, discussion_data
from matarisvan.operation_graph.generation_rules import LimitOffset, DefaultRule


class DataExtractorTest (unittest.TestCase):
    
    def test_should_set_params(self):
        data_extractor = DataExtractor({'id':'some_id'}, {'name': 'name_val'}, {})
        self.assertEquals({'id':'some_id'}, data_extractor._model_id_mapping)
        self.assertEquals({'name': 'name_val'}, data_extractor._model_data_mapping)
    
    def test_should_augment_id_with_defaults(self):
        data_extractor = DataExtractor({'id':'some_id'}, {'name': 'name_val'}, {'type': 'node_type'})
        self.assertEquals({'id':'some_id'}, data_extractor._model_id_mapping)
        self.assertEquals({'type': 'node_type'}, data_extractor._model_default)
        
    def test_should_accept_only_dicts(self):
        with self.assertRaises(AssertionError):
            DataExtractor([], {'name': 'name_val'}, {})
        with self.assertRaises(AssertionError):
            DataExtractor({'id':'some_id'}, [], {})
        with self.assertRaises(AssertionError):
            DataExtractor({'id':'some_id'}, {'name': 'name_val'}, [])
    
    def test_extract_model_data_from_should_get_data_extracted_from_what_is_passed_in(self):
        model_data = {"name": "name",
                    "mytw_user_id": "id",
                    "email": "email"
                    }
        model_ids = {"username":"username"}
        data_extractor = DataExtractor(model_id_mapping = model_ids, model_data_mapping = model_data)
        model_ids, model_data = data_extractor.extract_model_data_from(user_test_data[0])
        self.assertEquals({'username': 'johndoe'}, model_ids)
        self.assertEquals({'email' : 'johndoe@domain.com', 'name':'John Doe', 'mytw_user_id':1278237}, model_data)
    
    def test_extract_model_data_from_should_merge_default_into_model_id_if_specefied(self):
        model_data = {"name": "name",
                    "mytw_user_id": "id",
                    "email": "email"
                    }
        model_ids = {"username":"username"}
        data_extractor = DataExtractor(model_id_mapping = model_ids, model_data_mapping = model_data, default = {'type':'user'})
        model_ids, model_data = data_extractor.extract_model_data_from(user_test_data[0])
        self.assertEquals({'username': 'johndoe', 'type':'user'}, model_ids)
    
    def test_extract_model_data_from_should_get_data_extracted_from_a_key_defined_by_list(self):
        model_ids = {'name': ['message', 'subject']}
        data_extractor = DataExtractor(model_id_mapping=model_ids)
        model_ids, model_data = data_extractor.extract_model_data_from(discussion_data)
        self.assertEquals({'name':'subject is nothing'}, model_ids)


class UrlExtractorTest(unittest.TestCase):
    
    def test_shouldaccept_string_or_list(self):
        url_extractor = UrlExtractor('http://localhost')
        self.assertEquals('http://localhost', url_extractor._url_descriptor)
        url_extractor = UrlExtractor(['hello','world'])
        self.assertEquals(['hello', 'world'], url_extractor._url_descriptor)
    
    def test_shouldnt_accept_anything_other_than_list_or_string_for_url_descriptor_rest_can_be(self):
        with self.assertRaises(AssertionError):
            UrlExtractor({'hello':'world'})
    
    def test_get_next_url_should_return_url_if_set(self):
        url_extractor = UrlExtractor('http://localhost')
        self.assertEquals('http://localhost', url_extractor.get_next_url())
    
    def test_get_next_url_should_return_url_from_data_passed_in_if_descriptor_is_list(self):
        url_extractor = UrlExtractor(['links', 'self', 'url'])
        self.assertEquals('http://localhost', url_extractor.get_next_url({'links':{'self':{'url':'http://localhost'}}}))
    
    def test_get_next_url_should_throw_error_if_data_passed_in_is_none_and_descriptor_is_list(self):
        url_extractor = UrlExtractor(['links', 'self', 'url'])
        with self.assertRaises(AssertionError):
            url_extractor.get_next_url()
    
    def test_get_next_url_should_call_apply_all_rules_on_url(self):
        def_rule = Mock(spec = DefaultRule)
        def_rule.apply_rule_to.return_value = 'http://localhost/2020'
        generation_rule = Mock(spec=LimitOffset)
        generation_rule.apply_rule_to.return_value = 'http://localhost?limit=5&offset=10'
        url_extractor = UrlExtractor('http://localhost', next_url_generators = [def_rule, generation_rule])
        url = url_extractor.get_next_url()
        def_rule.apply_rule_to.assert_called_with('http://localhost')
        generation_rule.apply_rule_to.assert_called_with('http://localhost/2020')
        self.assertEquals('http://localhost?limit=5&offset=10', url)
    
    def test_get_next_url_should_call_apply_all_rules_on_url_from_url_descriptor(self):
        def_rule = Mock(spec = DefaultRule)
        def_rule.apply_rule_to.return_value = 'http://localhost/2020'
        generation_rule = Mock(spec=LimitOffset)
        generation_rule.apply_rule_to.return_value = 'http://localhost?limit=5&offset=10'
        url_extractor = UrlExtractor(['links', 'self', 'url'], next_url_generators = [def_rule, generation_rule])
        url = url_extractor.get_next_url({'links':{'self':{'url':'http://localhost'}}})
        def_rule.apply_rule_to.assert_called_with('http://localhost')
        generation_rule.apply_rule_to.assert_called_with('http://localhost/2020')
        self.assertEquals('http://localhost?limit=5&offset=10', url)


class DataSanitizerTest(unittest.TestCase):
    
    def test_should_clean_data_passed_in(self):
        sanitizer = DataSanitizer(discard_value = 'val', data_key = 'key')
        data = sanitizer.clean(" val {'key' : []}")
        self.assertEquals([], data)
    
    def test_should_return_data_without_truncation_if_no_discard_value(self):
        sanitizer = DataSanitizer(data_key = 'key')
        data = sanitizer.clean("{'key' : [{'hello':1, 'world':2}]}")
        self.assertEquals([{'hello':1, 'world':2}], data)
    
    def test_should_return_data_as_is_if_data_key_not_defined(self):
        sanitizer = DataSanitizer()
        data = sanitizer.clean("{'key' : [{'hello':1, 'world':2}]}")
        self.assertEquals({'key' : [{'hello':1, 'world':2}]}, data)
    
    def test_should_return_None_if_exception_occurs(self):
        with patch.object(ast, 'literal_eval') as mock_literal_eval:
            mock_literal_eval.side_effect = Exception('problem')
            sanitizer = DataSanitizer()
            data = sanitizer.clean("{'key' : [{'hello':1, 'world':2}]}")
            self.assertEquals([], data)


class InformerTest(unittest.TestCase):

    def test_should_encode_username_and_password_to_authstring(self):
        self.informer = Informer(username='test', password='test_pswd')
        auth_string = base64.encodestring('%s:%s' % ('test', 'test_pswd')).replace('\n', '')
        self.assertEquals(auth_string, self.informer._auth_string)
    
    def test_using_should_set_data_sanitizer_to_one_passed_in(self):
        self.informer = Informer(username='', password='')
        self.data_sanitizer = Mock(spec = DataSanitizer)
        self.informer.using(self.data_sanitizer)
        self.assertEquals(self.data_sanitizer, self.informer._data_sanitizer)
    
    def test_using_should_return_self(self):
        self.informer = Informer(username='', password='')
        self.data_sanitizer = Mock(spec = DataSanitizer)
        informer = self.informer.using(self.data_sanitizer)
        self.assertEquals(self.informer, informer)
    
    def test_should_fetch_data_from_url_and_sanitize_it_return_sanitized_data(self):
        self.informer = Informer(username='test', password='password')
        self.data_sanitizer = Mock(spec = DataSanitizer)
        self.data_sanitizer.clean.return_value = {'key':[]}
        auth_string = base64.encodestring('%s:%s' % ('test', 'password')).replace('\n', '')
        request = urllib2.Request('http://localhost')
        request.add_header("Authorization", "Basic %s" % auth_string)
        with patch.object(urllib2, 'urlopen') as mock_urllib:
            mock_urllib.return_value = "val {'key' : []}"
            data = self.informer.using(self.data_sanitizer).get_data_from(url = "http://localhost")
            self.data_sanitizer.clean.assert_called_with("val {'key' : []}")
            self.assertEquals({'key':[]}, data)
