import logging
import json

import requests



logging.basicConfig(level=logging.INFO,
                format='[%(levelname)s] %(message)s [%(filename)s][line:%(lineno)d] %(asctime)s ',
                datefmt='%d %b %Y %H:%M:%S')



class KVClient:

    def __init__(self):

        self.baseurl = 'http://localhost.devnode.com:8080/kv'

    def put(self, k, v):
        s, b = self._requests_put(k, data=v)
        return s, b

    def get(self, k):
        s, b = self._requests_get(k)
        return s, b

    def delete(self, k):
        s, b = self._requests_delete(k)
        return s, b

    def _rslash(self, suffix_url):
        return '/' + suffix_url.lstrip('/')

    def _requests_get(self, suffix_url='', headers=None, data=None):

        resp = requests.get(self.baseurl+self._rslash(suffix_url),
                headers=headers)
        # page = resp.headers
        page = resp.text
        code = resp.status_code
        logging.debug('put_resp:{}, code:{}'.format(page, code))
        return code, page

    def _requests_put(self, suffix_url='', headers=None, data=None):
        if isinstance(data, dict):
            logging.debug('data is dict')
            resp = requests.put(self.baseurl+self._rslash(suffix_url),
                headers=headers, data=json.dumps(data))
        elif isinstance(data, str):
            logging.debug('data is str')
            resp = requests.put(self.baseurl+self._rslash(suffix_url),
                headers=headers, data=data)
        else:
            logging.debug('data is not str or dict')
            resp = requests.put(self.baseurl+self._rslash(suffix_url),
                headers=headers, data=data)
        # page = resp.headers
        page = resp.text
        code = resp.status_code
        logging.debug('put_resp:{}, code:{}'.format(page, code))
        return code, page

    def _requests_delete(self, suffix_url='', headers=None, data=None):

        resp = requests.delete(self.baseurl+self._rslash(suffix_url),
                headers=headers)
        # page = resp.headers
        page = resp.text
        code = resp.status_code
        logging.debug('put_resp:{}, code:{}'.format(page, code))
        return code, page


k = KVClient()
print(k.put('d1', 'dataofd1'))
print(k.get('d1'))
print(k.put('d2', b'dataofd2'))
print(k.delete('d1'))
print(k.get('d1'))
print(k.get('d2'))

for i in range(100):
    print(k.put('d{}'.format(i), 'dataofd{}'.format(i)))

for i in range(100):
    print(k.get('d{}'.format(i)))
