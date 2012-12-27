#!/usr/bin/env python
#-*- coding:utf-8 -*-


import urllib2, ast, base64, urllib

import pickle

import simplejson as json

from matarisvan import logger

class Informer(object):
    
    def __init__(self, username=None, password=None):
        self._auth_string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
    
    def using(self, data_sanitizer):
        self._data_sanitizer = data_sanitizer
        return self
    
    def get_data_from(self, url):
        logger.debug(url)
        if not url:
            return []
        request = urllib2.Request(url)
        request.add_header("Authorization", "Basic %s" % self._auth_string)
        result = urllib2.urlopen(request)
        logger.debug("Result found:")
        return self._data_sanitizer.clean(result.read())


class UrlExtractor(object):
    
    def __init__(self, url_descriptor, next_url_generators=[]):
        assert isinstance(url_descriptor, list) or isinstance(url_descriptor, str)
        self._url_descriptor = url_descriptor
        self._next_url_generators = next_url_generators
    
    def _find_url_using(self, url_container, url_descriptor):
        #logger.debug('url_container = %s'%(url_container,))
        url = url_container
        assert url is not None
        for key in url_descriptor:
            url = url[key]
        return url
    
    def _find_url_by_trial_and_error(self, url_container):
        url = url_container
        for key in self._url_descriptor:
            try:
                return self._find_url_using(url, url_descriptor=key)
            except KeyError as e:
                logger.warning(e)
                print 'keyset %s not present. Trying next'%(key,)
        return None
    
    def get_next_url(self, url_container = None):
        url = self._url_descriptor
        if isinstance(self._url_descriptor, list) and isinstance(self._url_descriptor[0], str):
            try:
                url = self._find_url_using(url_container, self._url_descriptor)
            except KeyError as e:
                logger.error(e)
                url = None
        if isinstance(self._url_descriptor, list) and isinstance(self._url_descriptor[0], list):
            url = self._find_url_by_trial_and_error(url_container)
        for generator in self._next_url_generators:
            url =generator.apply_rule_to(url)
        return url


class DataSanitizer(object):
    
    def __init__(self, discard_value=[], data_key=None):
        self._discard_values = discard_value
        self._data_key = data_key
    def clean(self, data):
        #logger.debug('data is ----> %s'%(data,))
        logger.debug("cleaning data")
        logger.debug('Discard%s'%(self._discard_values,))
        for discard_value in self._discard_values:
            data = data.replace(discard_value, '')
        try:
            readable_data = self._clean_for_reading_as_json(data)
            logger.debug("cleaned data ----->%s"%(readable_data,))
            logger.debug('eval the string to get dict')
            cleaned_data = json.loads(readable_data)
            if self._data_key:
                logger.debug('get the data')
                return_value = cleaned_data.get(self._data_key)
                if not return_value:
                    return None
                return return_value
            return cleaned_data
        except Exception as e:
            logger.debug(data)
            logger.error(e)
            return []
    
    def _clean_for_reading_as_json(self, data):
        #data = data.replace("'", '"')
        data = data.replace("self", "this")
        data = data.replace(" :", ":")
        data = data.replace('\n', '')
        data = data.replace('\u', '')
        data = data.strip()
        return data


class DataExtractor(object):
    
    def __init__(self, model_id_mapping, model_data_mapping={}, default=None, using_processors={}):
        assert isinstance(model_id_mapping, dict)
        assert isinstance(model_data_mapping,dict)
        assert default is None or isinstance(default, dict)
        self._model_id_mapping = model_id_mapping
        self._model_data_mapping = model_data_mapping
        self._model_default = default
        self._processors = using_processors
    
    def extract_model_data_from(self, data):
        if self._model_default is None:
                self._model_default = {}
        logger.debug("id_mapping: %s \n data_mapping: %s, \n, default: %s, processors:%s"%(self._model_id_mapping, self._model_data_mapping, self._model_default, self._processors))
        model_data = { attribute : self._process_data(data, processor_id=attribute, reference_mapping=self._model_data_mapping) for attribute in self._model_data_mapping}
        model_ids = {attribute : self._process_data(data, processor_id=attribute, reference_mapping=self._model_id_mapping) for attribute in self._model_id_mapping}
        model_ids.update(self._model_default)
        logger.debug("Model_info: \n %s \n %s"%(model_ids, model_data))
        return model_ids, model_data
    
    def _get_from_model_data(self, data, attrib):
        model_attrib_data = data
        processor_id = attrib
        if not isinstance(attrib, list):
            return model_attrib_data[attrib]
        for attrib_key in attrib:
            model_attrib_data = model_attrib_data[attrib_key]
        return model_attrib_data
    
    def _process_data(self, data, processor_id, reference_mapping):
        logger.debug('processor_id=%s'%(processor_id,))
        extracted_data = self._get_from_model_data(data, attrib=reference_mapping[processor_id])
        processor = self._processors.get(processor_id)
        if processor:
            return processor.process(extracted_data)
        return extracted_data
