#!/usr/bin/env python
#-*- coding:utf-8 -*-


import urllib2, ast, base64, urllib

class Informer(object):
    
    def __init__(self, username=None, password=None):
        self._auth_string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
    
    def using(self, data_sanitizer):
        self._data_sanitizer = data_sanitizer
        return self
    
    def get_data_from(self, url):
        request = urllib2.Request(url)
        request.add_header("Authorization", "Basic %s" % self._auth_string)
        result = urllib2.urlopen(request)
        return self._data_sanitizer.clean(result)


class UrlExtractor(object):
    
    def __init__(self, url_descriptor, next_url_generators=[]):
        assert isinstance(url_descriptor, list) or isinstance(url_descriptor, str)
        self._url_descriptor = url_descriptor
    
    def get_next_url(self, url_container = None):
        if isinstance(self._url_descriptor, str):
            return self._url_descriptor
        assert url_container is not None
        for key in self._url_descriptor:
            url_container = url_container[key]
        return url_container


class DataSanitizer(object):
    
    def __init__(self, discard_value=None, data_key=None):
        self._discard_value = discard_value
        self._data_key = data_key
    
    def clean(self, data):
        if self._discard_value:
            data = data.replace(self._discard_value, '')
        data = data.strip()
        cleaned_data = ast.literal_eval(data)
        if self._data_key:
            return cleaned_data.get(self._data_key)
        return cleaned_data


class DataExtractor(object):
    
    def __init__(self, model_id_mapping, model_data_mapping, default={}):
        assert isinstance(model_id_mapping, dict)
        assert isinstance(model_data_mapping,dict)
        assert isinstance(default, dict)
        self._model_id_mapping = model_id_mapping
        self._model_data_mapping = model_data_mapping
        self._model_default = default
    
    def extract_model_data_from(self, data):
        model_data = { attribute : data[self._model_data_mapping[attribute]] for attribute in self._model_data_mapping}
        model_ids = {attribute : data[self._model_id_mapping[attribute]] for attribute in self._model_id_mapping}
        model_ids.update(self._model_default)
        return model_ids, model_data
