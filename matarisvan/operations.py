from matarisvan.operation_graph.entities import OperationNode
from matarisvan.operation_graph.data_operations import Informer, DataExtractor, DataSanitizer, UrlExtractor

class OperationGraph(object):
    
    def __init__(self):
        self.root = None
        self.current = None
    
    @classmethod
    def using(klass,username, password):
        graph = klass()
        graph._username = username
        graph._password = password
        return graph
    
    def from_url(self, url, discard=None, data_found_at=None, next_url_generators=[]):
        self._url_extractor = UrlExtractor(url, next_url_generators)
        self._data_sanitizer = DataSanitizer(discard, data_found_at)
        self._informer = Informer(self._username, self._password)
        return self
    
    def create_or_update(self, model, model_id_mapping, model_data_mapping={}, default={}):
        data_extractor = DataExtractor(model_id_mapping=model_id_mapping, model_data_mapping=model_data_mapping, default={})
        node = OperationNode(model, informer = self._informer, data_extractor = data_extractor, url_extractor = self._url_extractor, data_sanitizer = self._data_sanitizer)
        if not self.root:
            self.root = node
        self.current = node
        self._informer = None
        self._data_sanitizer = None
        return self
    
    def has_relationship(self, relationship, subgraph_defining_relationship):
        assert self.root
        subgraph_defining_relationship.root.has_relationship_with_parent(relationship)
        self.current.add_child(subgraph_defining_relationship.root)
        return self
    
    def has_relationship_with_self(self):
        assert self.root
        self.root.add_child(self.root)
        return self
    
    def execute(self):
        self.root.execute()
