import logging
import json
import asyncio
import time

import requests
import aiohttp


logging.basicConfig(level=logging.INFO,
                format='[%(levelname)s] %(message)s [%(filename)s][line:%(lineno)d] %(asctime)s ',
                datefmt='%d %b %Y %H:%M:%S')

ROUND = 10000

KV_URL = 'http://localhost.devnode.com:8080/kv'


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



async def aput():
    async with aiohttp.ClientSession() as session:
        for i in range(ROUND):
            async with session.put('{}/d{}'.format(KV_URL, i), data='dataofd{}'.format(i)) as resp:
                print(resp.status)
                print(await resp.text())


async def aget():
    async with aiohttp.ClientSession() as session2:
        for i in range(ROUND):
            async with session2.get('{}/d{}'.format(KV_URL, i)) as resp:
                print(resp.status)
                print(await resp.text())


async def adelete():
    async with aiohttp.ClientSession() as session2:
        for i in range(ROUND):
            async with session2.get('{}/d{}'.format(KV_URL, i)) as r:
                if r.status == 200:
                    async with session2.delete('{}d{}'.format(KV_URL, i)) as resp:
                        print(resp.status)
                        print(await resp.text())


if __name__ == '__main__':
    start = time.time()
    #
    # k = KVClient()
    # print(k.put('d1', 'dataofd1'))
    # print(k.get('d1'))
    # print(k.put('d2', b'dataofd2'))
    # print(k.delete('d1'))
    # print(k.get('d1'))
    # print(k.get('d2'))

    # for i in range(ROUND):
    #     print(k.put('d{}'.format(i), 'dataofd{}'.format(i)))

    # 21.78s
    # for i in range(ROUND):
    #     print(k.get('d{}'.format(i)))

    # for i in range(ROUND):
    #     print(k.delete('d{}'.format(i)))

    #


    loop = asyncio.get_event_loop()
    tasks = [
        # asyncio.ensure_future(aput()), # 16.2s
        # asyncio.ensure_future(aget()), # 12.6s
        # asyncio.ensure_future(adelete()), # 22s
        ]

    loop.run_until_complete(asyncio.gather(*tasks))
    loop.close()

    end = time.time()
    dur = end-start
    print('start: ', start)
    print('end', end)
    print('dur', dur)
