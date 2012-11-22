import unittest
from mock import Mock, patch

from matarisvan.operations import OperationGraph

from matarisvan.operation_graph.entities import OperationNode
from matarisvan.operation_graph.data_operations import Informer, DataExtractor


class StubModel(object):
    
    def get_or_create(self, **kwds):
        pass
        
    def update(self, **kwds):
        pass


class OperationGraphTest(unittest.TestCase):
    
    def setUp(self):
        self.g = OperationGraph.using('mahesh', 'password')
    
    def test_using_should_return_instance_of_graph(self):
        self.assertIsNotNone(self.g)
        self.assertEquals(type(self.g), OperationGraph)
        self.assertEquals(self.g._username, 'mahesh')
        self.assertEquals(self.g._password, 'password')
    
    def test_using_should_return_graph_with_no_root_no_current_node(self):
        self.assertEquals(self.g.root, None)
        self.assertEquals(self.g.current, None)
    
    def test_from_url_should_set_all_variables_to_the_graph_object(self):
        self.g.from_url('http://localhost', discard='nonsense', data_found_at='data')
        self.assertIsNotNone(self.g._informer)
        self.assertEquals('mahesh', self.g._informer._username)
        self.assertEquals('password', self.g._informer._password)
        self.assertIsNotNone(self.g._data_fetch_info)
        self.assertEquals('http://localhost', self.g._data_fetch_info._url_descriptor)
        self.assertEquals('nonsense', self.g._data_fetch_info._discard_value)
        self.assertEquals('data', self.g._data_fetch_info._data_key)
    
    def test_from_url_should_return_self(self):
        graph = self.g.from_url('http://localhost', discard='nonsense', data_found_at='data')
        self.assertEquals(self.g, graph)
    
    def test_create_or_update_should_set_root_and_current_if_none_exist(self):
        self.g.from_url('http://localhost', discard='nonsense', data_found_at='data').create_or_update(StubModel(), {}, {})
        self.assertIsNotNone(self.g.root)
        self.assertIsNotNone(self.g.current)
    
    def test_create_or_update_should_set_root_and_current(self):
        self.g.from_url('http://localhost', discard='nonsense', data_found_at='data').create_or_update(StubModel(), {}, {})
        self.assertEquals(self.g.root, self.g.current)
    
    def test_create_or_update_should_set_locals_except_cred_to_none(self):
        self.g.from_url('http://localhost', discard='nonsense', data_found_at='data').create_or_update(StubModel(), {}, {})
        self.assertTrue('mahesh', self.g._password)
        self.assertTrue('password', self.g._username)
        self.assertTrue(self.g._informer is None)
        self.assertTrue(self.g._data_fetch_info is None)
    
    def test_create_or_update_should_create_informer_and_data_extractor_on_node(self):
        self.g.from_url('http://localhost', discard='nonsense', data_found_at='data').create_or_update(StubModel, {}, {})
        self.assertIsNotNone(self.g.current._informer)
        self.assertIsNotNone(self.g.current._data_extractor)
        self.assertIsNotNone(self.g.current._data_fetch_info)
        
    def test_has_subgraph_should_make_subgraph_root_if_root_is_none(self):
        subgraph = OperationGraph.using('mahesh', 'password').from_url("http://localhost").create_or_update(StubModel(), {}, {})
        self.g.has_subgraph(subgraph)
        root = self.g.root
        self.assertEquals(subgraph.root, root )
    
    def test_has_subgraph_should_create_child_to_curent(self):
        self.g.from_url('http://localhost', discard='nonsense', data_found_at='data').create_or_update(StubModel(), {}, {})
        subgraph = OperationGraph.using('mahesh', 'password').from_url("http://localhost").create_or_update(StubModel(), {}, {})
        self.g.has_subgraph(subgraph)
        current = self.g.current
        self.assertEquals(subgraph.root, current.children[0].end_node )
    
    def test_has_subgraph_should_clear_all_current_variables(self):
        self.g.from_url('http://localhost', discard='nonsense', data_found_at='data').create_or_update(StubModel(), {}, {})
        subgraph = OperationGraph.using('mahesh', 'password').from_url("http://localhost").create_or_update(StubModel(), {}, {})
        self.g.has_subgraph(subgraph)
        self.assertTrue(self.g._informer is None)
        self.assertTrue(self.g._data_fetch_info is None)
