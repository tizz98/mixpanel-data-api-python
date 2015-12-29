import re
from collections import namedtuple

import six

from .request import Request
from .util import get_date_string, jsonl_decoder


class Export(object):
    def __init__(self, from_date, to_date, event=None, where='', bucket=''):
        """
        Get a "raw dump" of tracked events over a time period
        :param from_date: The date from which to begin querying for the event.
                          This date is inclusive.
        :param to_date: The date from which to stop querying for the event.
                        This date is inclusive.
        :param event: The event or events that you wish to get data for.
        :param where: An expression to filter events by.
                      See: https://goo.gl/t6Q7kq
        :param bucket: The specific data bucket you would like to query.
        """
        self.from_date = get_date_string(from_date)
        self.to_date = get_date_string(to_date)

        if not isinstance(event, list)\
                and isinstance(event, six.string_types):
            self.event = [event]
        elif isinstance(event, list):
            self.event = event
        else:
            self.event = []

        self.where = where
        self.bucket = bucket

        self._populate()

    @staticmethod
    def _set_list_data(obj, data_list, key):
        for data_item in data_list:
            if isinstance(data_item, dict):
                data_item = Export.list_handler(data_item)
            elif isinstance(data_item, list):
                data_item = Export.list_handler(data_item)

            setattr(obj, Export.clean_key(key), data_item)

    @staticmethod
    def dict_handler(data_dict, key=''):
        KeyClass = namedtuple(key, ' '.join(data_dict.keys()))
        ret_obj = KeyClass()

        for k, v in data_dict.items():
            if isinstance(v, list):
                v = Export.list_handler(v, key=k)
            elif isinstance(v, dict):
                v = Export.dict_handler(v)

            setattr(ret_obj, Export.clean_key(k), v)

        return ret_obj

    @staticmethod
    def list_handler(data_list, key=''):
        return_data = []

        for data_item in data_list:
            if isinstance(data_item, list):
                data_item = Export.list_handler(data_item, key=key)
            elif isinstance(data_item, dict):
                data_item = Export.dict_handler(data_item, key=key)

            return_data.append(data_item)

        return return_data

    @staticmethod
    def clean_key(key):
        return re.sub(r'\W|^(?=\d)', '_', key)

    def _set_data(self, data):
        self._set_list_data(self, data, 'events')

    def _populate(self):
        params = {
            'from_date': self.from_date,
            'to_date': self.to_date,
            'event': self.event,
        }

        if self.where:
            params['where'] = self.where
        if self.bucket:
            params['bucket'] = self.bucket

        response = Request('export', subdomain='data',
                           json_decoder=jsonl_decoder, **params)
        data = response.json()

        if 'error' not in data:
            self._set_data(data)
        else:
            self.events = []
