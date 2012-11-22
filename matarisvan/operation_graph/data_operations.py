
import urllib2, ast, base64, urllib

class Informer(object):
    
    def __init__(self, username=None, password=None):
        self._username = username
        self._password = password
    
    def get_data_from(self, data_fetch_info):
        pass


class DataSanitizer(object):
    
    def __init__(self, url_descriptor, discard_value=None, data_key=None):
        assert type(url_descriptor) is list or type(url_descriptor) is str
        self._url_descriptor = url_descriptor
        self._discard_value = discard_value
        self._data_key = data_key
    
    def url_described_by(self, url_container = None):
        if type(self._url_descriptor) is str:
            return self._url_descriptor
        assert url_container is not None
        for key in self._url_descriptor:
            url_container = url_container[key]
        return url_container


class DataExtractor(object):
    
    def __init__(self, model_id_mapping, model_data_mapping, default={}):
        assert type(model_id_mapping) is dict
        assert type(model_data_mapping) is dict
        assert type(default) is dict
        model_id_mapping.update(default)
        self._model_id_mapping = model_id_mapping
        self._model_data_mapping = model_data_mapping
    
    def extract_model_data_from(self, data):
        pass
