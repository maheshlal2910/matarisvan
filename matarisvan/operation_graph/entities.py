from matarisvan.operation_graph.data_operations import Informer, DataExtractor

class OperationNode(object):
    
    def __init__(self, model, informer, data_extractor, data_fetch_info):
        assert 'get_or_create' in dir(model)
        assert 'update' in dir(model)
        self.children = []
        self.parent = None
        self._informer = informer
        self._data_extractor = data_extractor
        self._data_fetch_info = data_fetch_info
    
    def add_child(self, child):
        assert type(child) is OperationNode
        child_rel = Relationship(self, child)
        child.parent = Relationship(child, self)
        self.children.append(child_rel)
    
    def create_or_update(self, model, model_id_mapping, model_data_mapping, default):
        assert type(model_id_mapping) is dict
        assert type(model_data_mapping) is dict
        assert type(default) is dict
        model_id_mapping.update(default)
        self._model = model
        self._model_data_mapping = model_data_mapping
        self._model_id_mapping = model_id_mapping
    
    def execute(self, data=None):
        pass


class Relationship(object):
    
    def __init__(self, start, end):
        self.end_node = end
        self.start_node = start
