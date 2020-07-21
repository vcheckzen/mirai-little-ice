import os
import re
import time
import random
import logging
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from mirai import Plain, Image

from utils.config import config
from utils.image import image_helper
from plugins.base import PluginBase


logging.basicConfig(level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S',
                    format='[%(asctime)s][Plugin][Ice] %(levelname)s: %(message)s')


class Ice(PluginBase):
    def __init__(self):
        self.header_path = config['plugins']['ice']['header']
        self.image_save_path = config['image']['public']
        self.__read_headers__()
        self.ice_id = 5175429989
        self.chat_api = 'https://m.weibo.cn/api/chat/'
        self.upload_api = f'{self.chat_api}upload'
        self.send_api = f'{self.chat_api}send'
        self.recv_api = f'{self.chat_api}list?uid={self.ice_id}&count=10&unfollowing=0'
        self.session = requests.Session()

    def __get_content__(self, url, headers=None):
        if not headers:
            headers = self.headers
        return self.session.get(url, headers=headers)

    def __post_data__(self, url, data):
        return self.session.post(url, headers=self.headers, data={
            'uid': self.ice_id,
            'st': self.headers['x-xsrf-token'],
            **data
        })

    def __post_file__(self, url, files):
        headers = self.headers.copy()
        headers.pop('content-type')
        return self.session.post(url, files=files, params={
            'tuid': self.ice_id,
            'st': self.headers['x-xsrf-token']
        }, headers=headers)

    def __read_headers__(self):
        self.headers = {}
        with open(self.header_path, 'r') as f:
            for l in f.readlines():
                l = l.strip().split(': ')
                self.headers[l[0]] = l[1]
        logging.info('ice headers read.')

    def __write_headers__(self):
        with open(self.header_path, 'w') as f:
            for k, v in self.headers.items():
                f.write(f'{k}: {v}{os.linesep}')

    def __refresh_headers__(self):
        r = self.__get_content__(
            self.recv_api, {'cookie': self.headers['cookie']})
        self.headers['x-xsrf-token'] = r.cookies['XSRF-TOKEN']
        self.headers['cookie'] = self.headers['cookie'].replace(
            re.compile(r'XSRF-TOKEN=(.{,10});').findall(
                self.headers['cookie']
            )[0],
            r.cookies['XSRF-TOKEN']
        )
        self.__write_headers__()
        logging.info('ice headers refreshed.')

    def __pull_responses__(self, send_time, wait_time):
        time.sleep(wait_time)
        logging.info('get responses by polling...')
        msgs = []
        for _ in range(10):
            r = self.__get_content__(self.recv_api).json()

            for msg in r.get('data', {}).get('msgs', {}):
                if msg['sender_id'] != self.ice_id:
                    continue

                t = msg['created_at']
                f = '%a %b %d %H:%M:%S +0800 %Y'
                if send_time > datetime.strptime(t, f).timestamp():
                    continue

                if 'attachment' in msg:
                    msg['text'] = self.__download_img__(
                        msg['attachment']['original_image']['url'])

                msgs.extend((self.__remove_bad_html__(msg['text'])))
                logging.info('message fetched: {}'.format(msg['text']))

            if msgs:
                return self.__validate_responses__(msgs)

            time.sleep(random.random())

        logging.warning('fetch responses failed.')
        return msgs

    def __remove_bad_html__(self, text):
        soup = BeautifulSoup(f'<div>{text}</div>', 'html.parser')
        plain = soup.get_text().strip()
        msgs = []
        if plain:
            msgs.append(plain)
        for img in soup.findAll('img'):
            msgs.append(self.__download_img__(img['src']))
        for a in soup.findAll('a'):
            msgs.append(a['text']+a['href'])
        return msgs

    def __validate_send__(self, send):
        r = send()
        if r['ok'] != 1:
            logging.warning('ice headers invalid, renewing...')
            self.__refresh_headers__()
            r = send()
        return r

    def __validate_responses__(self, resps):
        valid_resps = []
        for r in resps:
            if r.startswith(self.image_save_path):
                valid_resps.append(Image.fromFileSystem(r))
            else:
                valid_resps.append(Plain(r))
        return valid_resps

    def __download_img__(self, url):
        return image_helper.download_img(url, self.__get_content__(url))

    def __upload_img__(self, img_path):
        suffix = img_path.split('.')[-1]
        if suffix == 'jpg':
            suffix = 'jpeg'
        elif suffix == 'icon':
            suffix = 'x-icon'

        def send():
            return self.__post_file__(self.upload_api, {
                'file': (
                    os.path.basename(img_path),
                    open(img_path, 'rb'),
                    f'image/{suffix}'
                )}).json()

        r = self.__validate_send__(send)
        return r['data']['fids']

    def __send_and_get_resp__(self, send, ctype, wait):
        start = datetime.now().timestamp()
        self.__validate_send__(send)

        logging.info(f'{ctype} sended.')
        return self.__pull_responses__(start, wait)

    def chat_with_text(self, text: str):
        def send():
            return self.__post_data__(self.send_api, {
                'content': text,
            }).json()

        return self.__send_and_get_resp__(send, 'text', 0.5)

    def chat_with_image(self, image_path: str, image_url: str = None):
        if image_url:
            image_path = image_helper.download_img(image_url)

        def send():
            return self.__post_data__(self.send_api, {
                'fids': self.__upload_img__(image_path),
            }).json()

        return self.__send_and_get_resp__(send, 'image', 1)
