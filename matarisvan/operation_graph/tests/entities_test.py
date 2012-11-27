#!/usr/bin/env python
#-*- coding:utf-8 -*-


import unittest
import mock
from mock import Mock

from matarisvan.operation_graph.entities import OperationNode, Relationship
from matarisvan.operation_graph.data_operations import Informer, DataExtractor, UrlExtractor, DataSanitizer
from matarisvan.operation_graph.tests.test_data import user_test_data

#Stub classes
class StubModel(object):
    
    @classmethod
    def get_or_create(self, **kwds):
        return StubModel()
        
    def update(self, **kwds):
        pass

class Without_get_or_create(object):
    
    def update(self, **kwds):
        pass

class Without_update(object):
    
    def get_or_create(self, **kwds):
        pass

class StubDataExtractor(object):
    
    def extract_data_from(self, data):
        return {'username':'test'}, {'email':'test@test.com'}


class OperationNodeTest(unittest.TestCase):
    
    def setUp(self):
        self.informer = Mock(spec = Informer)
        self.data_extractor = Mock(spec = DataExtractor)
        self.data_extractor.extract_model_data_from.return_value = ({'username':'test'}, {'email':'test@test.com'})
        self.url_extractor = Mock(spec = UrlExtractor)
        self.data_sanitizer = Mock(spec = DataSanitizer)
        self.node = OperationNode(model=StubModel, informer = self.informer, data_extractor = self.data_extractor, url_extractor = self.url_extractor, data_sanitizer = self.data_sanitizer)
        self.stub = StubModel()
    
    def test_should_create_children_as_empty_array(self):
        self.assertTrue("children" in dir(OperationNode(StubModel, self.informer, self.data_extractor, self.url_extractor, self.data_sanitizer)))
    
    def test_should_add_relationship_to_children_when_add_child_called(self):
        child = OperationNode(StubModel, self.informer, self.data_extractor, self.url_extractor, self.data_sanitizer)
        self.node.add_child(child)
        self.assertTrue(self.node.children != [])
        self.assertEquals(child, self.node.children[0].end_node)
    
    def test_shouldnt_add_child_if_passed_object_isnt_Node(self):
        with self.assertRaises(AssertionError):
            self.node.add_child(self.stub)
    
    def test_should_add_parent_to_child(self):
        child = OperationNode(StubModel, self.informer, self.data_extractor, self.url_extractor, self.data_sanitizer)
        self.node.add_child(child)
        self.assertEquals(self.node, child.parent.end_node)
    
    def test_should_raise_error_for_model_without_get_or_create_and_update(self):
        with self.assertRaises(AssertionError):
            OperationNode(Without_get_or_create, self.informer, self.data_extractor, self.url_extractor, self.data_sanitizer)
        with self.assertRaises(AssertionError):
            OperationNode(Without_update, self.informer, self.data_extractor, self.url_extractor, self.data_sanitizer)
        with self.assertRaises(AssertionError):
            OperationNode(object, self.informer, self.data_extractor, self.url_extractor, self.data_sanitizer)
    
    def test_execute_should_get_url_from_url_extractor(self):
        self.node.execute()
        self.url_extractor.url_described_by.assertCalledWith(None)
    
    def test_execute_should_set_data_sanitizer_on_informer(self):
        self.node.execute()
        self.informer.using.assert_called_with(self.data_sanitizer)
    
    def test_execute_should_call_get_data_with_appropriate_url(self):
        data = {'some_data':{'url':'http://localhost'}}
        self.url_extractor.url_described_by.return_value = 'http://localhost'
        self.informer.using.return_value = self.informer
        self.node.execute(data)
        self.url_extractor.url_described_by.assert_called_with(data)
        self.informer.get_data_from.assert_called_with('http://localhost')
    
    def test_execute_should_call_dataExtractor_with_what_get_data_returns(self):
        data = {'some_data':{'url':'http://localhost'}}
        self.informer.using.return_value = self.informer
        self.informer.get_data_from.return_value = user_test_data[0]
        self.node.execute(data)
        self.data_extractor.extract_model_data_from.assert_called_with(user_test_data[0])
    
    def test_execute_should_call_dataExtractor_with_individual_data_snippets_if_get_data_refturns_a_list(self):
        data = {'some_data':{'url':'http://localhost'}}
        self.informer.using.return_value = self.informer
        self.informer.get_data_from.return_value = user_test_data
        self.node.execute(data)
        self.data_extractor.extract_model_data_from.assert_called_with(user_test_data[1])
    
    def test_execute_should_use_data_returned_by_data_extractor_to_create_and_update(self):
        model_class = Mock(spec = StubModel)
        model_instance = Mock(spec = StubModel)
        model_class.get_or_create.return_value = model_instance
        data_extractor = StubDataExtractor()
        node = OperationNode(model_class, self.informer, self.data_extractor, self.url_extractor,self.data_sanitizer)
        data = {'some_data':{'url':'http://localhost'}}
        node.execute(data)
        model_class.get_or_create.assert_called_with(username='test')
        model_instance.update.assert_called_with(email='test@test.com')
