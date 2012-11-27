#!/usr/bin/env python
#-*- coding:utf-8 -*-


class OperationNode(object):
    
    def __init__(self, model, informer, data_extractor, url_extractor, data_sanitizer):
        assert 'get_or_create' in dir(model)
        assert 'update' in dir(model)
        self.children = []
        self.parent = None
        self._informer = informer
        self._data_extractor = data_extractor
        self._url_extractor = url_extractor
        self._data_sanitizer = data_sanitizer
    
    def add_child(self, child):
        assert type(child) is OperationNode
        child_rel = Relationship(self, child)
        child.parent = Relationship(child, self)
        self.children.append(child_rel)

    def execute(self, data=None):
        url = self._url_extractor.url_described_by(data)
        response = self._informer.using(self._data_sanitizer).get_data_from(url)
        if type(response) is list:
            map(self._create_model_using, response)
        else:
            self._create_model_using(response)
    
    def _create_model_using(self, data):
        self._data_extractor.extract_model_data_from(data)

class Relationship(object):
    
    def __init__(self, start, end):
        self.end_node = end
        self.start_node = start
