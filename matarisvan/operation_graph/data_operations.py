
import urllib2, ast, base64, urllib

class Informer(object):
    
    def __init__(self, username=None, password=None):
        self._username = username
        self._password = password
    
    def get_data_from(self, data_fetch_info):
        pass


class DataFetchInfo(object):
    
    def __init__(self, url_descriptor, discard_value, data_key):
        self._url_descriptor = url_descriptor
        self._discard_value = discard_value
        self._data_key = data_key
    
    def url_described_by(self, url_container = None):
        pass


class DataExtractor(object):
    
    def __init__(self, model_id_mapping, model_data_mapping, default={}):
        assert type(model_id_mapping) is dict
        assert type(model_data_mapping) is dict
        assert type(default) is dict
        model_id_mapping.update(default)
        self._model_id_mapping = model_id_mapping
        self._model_data_mapping = model_data_mapping
    
    def extract_model_data_from(self, data):
        forbidden = ["relationships"]
        model_name = self.reference['should_map_to']
        model_primary = self.reference['model_primary']
        forbidden.append(model_primary)
        data_primary = self.reference['data_primary']
        model_id = {model_primary: self._get_from_model_data(data, data_primary)}
        data_ids = self.reference['data_descriptor']
        model_data = {model_attribute: self._get_from_model_data(data, attrib=data_ids[model_attribute]) for model_attribute in data_ids.keys() if model_attribute not in forbidden}
        default_type = self.reference.get('default')
        if default_type:
            model_id.update(default_type)
        return model_name, model_id, model_data
    
    def _encode_if_necessary(self, value):
        if type(value) is str:
            value = strip_tags(value)
            return unicode(value, 'unicode-escape')
        return value
    
    def _get_from_model_data(self, data, attrib):
        attrib_keys = attrib.split(',')
        model_attrib_data = data
        for attrib_key in attrib_keys:
            model_attrib_data = model_attrib_data[attrib_key.strip()]
        return self._encode_if_necessary(model_attrib_data)
    
    def _get_urls_from(self, data):
        keys = self.reference["urls"].split()
        urls = data
        for key in keys:
            urls = urls[key]
        return {"urls": [urls]}
    
    def using(self,reference):
        self.reference = reference
        return self

