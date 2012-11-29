#!/usr/bin/env python
#-*- coding:utf-8 -*-

class LimitOffset(object):
    
    def __init__(self, limit, offset):
        self._limit = limit
        self._offset = offset
    
    def apply_rule_to(self, url):
        params = '?limit=%s&offset=%s'%(self._limit, self._offset)
        self._offset = self._offset + self._limit
        return url%(params)


class DefaultRule(object):
    
    def apply_rule_to(self, url):
        return url
