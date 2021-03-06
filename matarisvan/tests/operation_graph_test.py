import unittest
from mock import Mock, patch

import base64

from matarisvan.operations import OperationGraph

from matarisvan.operation_graph.entities import OperationNode


class StubModel(object):
    
    def get_or_create(self, **kwds):
        pass
        
    def update(self, **kwds):
        pass


class OperationGraphTest(unittest.TestCase):
    
    def setUp(self):
        self.g = OperationGraph.using('test', 'password')
    
    def test_using_should_return_instance_of_graph(self):
        self.assertIsNotNone(self.g)
        self.assertEquals(type(self.g), OperationGraph)
        self.assertEquals(self.g._username, 'test')
        self.assertEquals(self.g._password, 'password')
    
    def test_using_should_return_graph_with_no_root_no_current_node(self):
        self.assertEquals(self.g.root, None)
        self.assertEquals(self.g.current, None)
    
    def test_from_url_should_set_all_variables_to_the_graph_object(self):
        self.g.from_url('http://localhost', discard=['nonsense'], data_found_at='data')
        auth_string = base64.encodestring('%s:%s' % ('test', 'password')).replace('\n', '')
        self.assertIsNotNone(self.g._informer)
        self.assertEquals(auth_string, self.g._informer._auth_string)
        self.assertEquals('http://localhost', self.g._url_extractor._url_descriptor)
        self.assertEquals(['nonsense'], self.g._data_sanitizer._discard_values)
        self.assertEquals('data', self.g._data_sanitizer._data_key)
    
    def test_from_url_should_return_self(self):
        graph = self.g.from_url('http://localhost', discard=['nonsense'], data_found_at='data')
        self.assertEquals(self.g, graph)
    
    def test_create_or_update_should_set_root_and_current_if_none_exist(self):
        self.g.from_url('http://localhost', discard=['nonsense'], data_found_at='data').create_or_update(StubModel(), {}, {})
        self.assertIsNotNone(self.g.root)
        self.assertIsNotNone(self.g.current)
    
    def test_create_or_update_should_set_root_and_current(self):
        self.g.from_url('http://localhost', discard=['nonsense'], data_found_at='data').create_or_update(StubModel(), {}, {})
        self.assertEquals(self.g.root, self.g.current)
    
    def test_create_or_update_should_set_locals_except_cred_to_none(self):
        self.g.from_url('http://localhost', discard=['nonsense'], data_found_at='data', next_url_generators=[]).create_or_update(StubModel(), {}, {})
        self.assertTrue('test', self.g._password)
        self.assertTrue('password', self.g._username)
        self.assertTrue(self.g._informer is None)
        self.assertTrue(self.g)
        self.assertTrue(self.g._data_sanitizer is None)
    
    def test_create_or_update_should_create_informer_and_data_extractor_on_node(self):
        self.g.from_url('http://localhost', discard=['nonsense'], data_found_at='data').create_or_update(StubModel, {}, {})
        self.assertIsNotNone(self.g.current._informer)
        self.assertIsNotNone(self.g.current._data_extractor)
        self.assertIsNotNone(self.g.current._url_extractor)
    
    def test_create_or_update_should_accept_blank_model_data_mapping(self):
        self.g.from_url('http://localhost', discard=['nonsense'], data_found_at='data').create_or_update(StubModel, model_id_mapping={})
    
    def test_has_relationship_should_throw_exception_root_is_none(self):
        subgraph = OperationGraph.using('test', 'password').from_url("http://localhost")
        with self.assertRaises(AssertionError):
            self.g.has_relationship('relationship', subgraph)
    
    def test_has_relationship_should_create_child_to_curent(self):
        self.g.from_url('http://localhost', discard=['nonsense'], data_found_at='data').create_or_update(StubModel(), {}, {})
        subgraph = OperationGraph.using('test', 'password').from_url("http://localhost").create_or_update(StubModel(), {}, {})
        self.g.has_relationship('relationship', subgraph)
        current = self.g.current
        self.assertEquals(subgraph.root, current.children[0].end_node)
    
    def test_has_relationship_should_clear_all_current_variables(self):
        self.g.from_url('http://localhost', discard=['nonsense'], data_found_at='data').create_or_update(StubModel(), {}, {})
        subgraph = OperationGraph.using('test', 'password').from_url("http://localhost").create_or_update(StubModel(), {}, {})
        self.g.has_relationship('relationship', subgraph)
        self.assertTrue(self.g._informer is None)
        self.assertTrue(self.g._data_sanitizer is None)
    
    def test_has_relationship_should_add_subgraph_supplied_as_subgraph_defining_relationship(self):
        self.g.from_url('http://localhost', discard=['nonsense'], data_found_at='data').create_or_update(StubModel(), {}, {})
        subgraph = OperationGraph.using('test', 'password').from_url("http://localhost").create_or_update(StubModel(), {}, {})
        self.g.has_relationship('some_relationship', subgraph_defining_relationship = subgraph)
        current = self.g.current
        self.assertEquals('some_relationship', current.children[0].end_node._has_relationship)
    
    def test_has_relationship_with_self_should_add_self_as_child(self):
        self.g.from_url('http://localhost', discard=['nonsense'], data_found_at='data').create_or_update(StubModel(), {}, {}).has_relationship_with_self()
        self.assertEquals(self.g.root, self.g.root.children[0].end_node)
    
    def test_has_relationship_with_self_should_return_graph_object(self):
        g = self.g.from_url('http://localhost', discard=['nonsense'], data_found_at='data').create_or_update(StubModel(), {}, {}).has_relationship_with_self()
        self.assertEquals(self.g, g)
    
    def test_has_relationship_with_self_should_throw_error_if_root_is_none(self):
        with self.assertRaises(AssertionError):
            self.g.has_relationship_with_self()
    
    def test_has_more_like_this_should_add_next_to_operation_node(self):
        g = self.g.from_url('http://localhost', discard=['nonsense'], data_found_at='data').create_or_update(StubModel(), {}, {}).has_more_like_this()
        self.assertEquals(self.g.root.next.end_node, g.root)
    
    def test_has_more_like_this_should_return_graph_object(self):
        g = self.g.from_url('http://localhost', discard=['nonsense'], data_found_at='data').create_or_update(StubModel(), {}, {}).has_more_like_this()
        self.assertEquals(self.g, g)
    
    def test_has_more_like_this_should_throw_error_if_root_is_none(self):
        with self.assertRaises(AssertionError):
            self.g.has_more_like_this()
