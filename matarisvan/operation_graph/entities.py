from matarisvan.operation_graph.data_operations import Informer, DataExtractor

class OperationNode(object):
    
    def __init__(self, model, informer, data_extractor, data_sanitizer):
        assert 'get_or_create' in dir(model)
        assert 'update' in dir(model)
        self.children = []
        self.parent = None
        self._informer = informer
        self._data_extractor = data_extractor
        self._data_sanitizer = data_sanitizer
    
    def add_child(self, child):
        assert type(child) is OperationNode
        child_rel = Relationship(self, child)
        child.parent = Relationship(child, self)
        self.children.append(child_rel)

    def execute(self, data=None):
        
        pass


class Relationship(object):
    
    def __init__(self, start, end):
        self.end_node = end
        self.start_node = start
