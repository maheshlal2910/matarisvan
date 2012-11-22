import unittest
from mock import Mock

from matarisvan.operation_graph.entities import OperationNode, Relationship
from matarisvan.operation_graph.data_operations import Informer, DataExtractor, DataSanitizer

#Stub classes
class StubModel(object):
    
    def get_or_create(self, **kwds):
        pass
        
    def update(self, **kwds):
        pass

class Without_get_or_create(object):
    
    def update(self, **kwds):
        pass

class Without_update(object):
    
    def get_or_create(self, **kwds):
        pass


class OperationNodeTest(unittest.TestCase):
    
    def setUp(self):
        self.informer = Mock(spec = Informer)
        self.data_extractor = Mock(spec = DataExtractor)
        self.data_sanitizer = Mock(spec = DataSanitizer)
        self.node = OperationNode(model=StubModel, informer = self.informer, data_extractor = self.data_extractor, data_sanitizer = self.data_sanitizer)
        self.stub = StubModel()
    
    def test_should_create_children_as_empty_array(self):
        self.assertTrue("children" in dir(OperationNode(StubModel, self.informer, self.data_extractor, self.data_sanitizer)))
    
    def test_should_add_relationship_to_children_when_add_child_called(self):
        child = OperationNode(StubModel, self.informer, self.data_extractor, self.data_sanitizer)
        self.node.add_child(child)
        self.assertTrue(self.node.children != [])
        self.assertEquals(child, self.node.children[0].end_node)
    
    def test_shouldnt_add_child_if_passed_object_isnt_Node(self):
        with self.assertRaises(AssertionError):
            self.node.add_child(self.stub)
    
    def test_should_add_parent_to_child(self):
        child = OperationNode(StubModel, self.informer, self.data_extractor, self.data_sanitizer)
        self.node.add_child(child)
        self.assertEquals(self.node, child.parent.end_node)
    
    def test_should_raise_error_for_model_without_get_or_create_and_update(self):
        with self.assertRaises(AssertionError):
            OperationNode(Without_get_or_create, self.informer, self.data_extractor, self.data_sanitizer)
        with self.assertRaises(AssertionError):
            OperationNode(Without_update, self.informer, self.data_extractor, self.data_sanitizer)
        with self.assertRaises(AssertionError):
            OperationNode(object, self.informer, self.data_extractor, self.data_sanitizer)
    
    def test_execute_should_get_url_from_data_sanitizer(self):
        self.node.execute()
        self.data_sanitizer.url_described_by.assertCalledWith(None)
