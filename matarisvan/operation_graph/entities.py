#!/usr/bin/env python
#-*- coding:utf-8 -*-

from matarisvan import logger

class OperationNode(object):
    
    def __init__(self, model, informer, data_extractor, url_extractor, data_sanitizer):
        assert 'get_or_create' in dir(model)
        assert 'update' in dir(model)
        self.children = []
        self.next = None
        self.parent = None
        self._informer = informer
        self._data_extractor = data_extractor
        self._url_extractor = url_extractor
        self._data_sanitizer = data_sanitizer
        self._model = model
        self._has_relationship = ''
    
    def add_child(self, child):
        assert isinstance(child, OperationNode)
        child_rel = Relationship(self, child)
        child.parent = Relationship(child, self)
        self.children.append(child_rel)
    
    def add_next(self, next):
        assert isinstance(next, OperationNode)
        self. next = Relationship(self, next)
    
    def execute(self, data=None, parent=None):
        logger.debug('begin execute')
        url = self._url_extractor.get_next_url(data)
        response = self._informer.using(self._data_sanitizer).get_data_from(url)
        if response is None:
            logger.debug("No data")
            return
        if isinstance(response, list):
            logger.debug("Is list")
            for reponse_object in response:
                self._create_model_using(reponse_object, parent)
        else:
            self._create_model_using(response, parent = parent)
        if self.next:
	            self.next.end_node.execute()
    
    def _create_model_using(self, data, parent=None):
        
        logger.debug("model_data %s"%(data,))
        #try:
        model_ids, model_data = self._data_extractor.extract_model_data_from(data)
        model = self._model.get_or_create(**model_ids).update(**model_data)
        logger.debug(model)
        if parent and self._has_relationship!='':
            logger.debug('%s ----- %s ----> %s'%(parent, self._has_relationship, model))
            getattr(parent, self._has_relationship)(model)
        for child in self.children:
            child.end_node.execute(data=data, parent=model)
        #except Exception as e:
        #logger.error(e)
    
    def has_relationship_with_parent(self, relation_name):
        self._has_relationship = relation_name


class Relationship(object):
    
    def __init__(self, start, end):
        self.end_node = end
        self.start_node = start
