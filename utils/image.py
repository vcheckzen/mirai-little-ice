import re
from random import randint
from shutil import rmtree
from os import listdir, mkdir
from datetime import datetime

import requests

from utils.config import config
from utils.base import UtilBase


class ImageHelper(UtilBase):
    def __init__(self):
        self.pub_img_path = config['image']['public']
        self.suffix_seeker = re.compile(r'image/([a-z-.]+)')

    def get_rand_img(self, path):
        imgs = listdir(path)
        return path + '/' + imgs[randint(0, len(imgs)-1)]

    def download_img(self, url, resp=None):
        if not resp:
            resp = requests.get(url)

        sfx = self.suffix_seeker.findall(resp.headers['Content-Type'])[0]
        if sfx == 'jpeg':
            sfx = 'jpg'
        elif 'icon' in sfx:
            sfx = 'icon'

        ts = datetime.now().timestamp()
        name = '{}/{}.{}'.format(self.pub_img_path, ts, sfx)

        with open(name, 'wb') as f:
            f.write(resp.content)

        return name

    async def del_pub_imgs(self):
        rmtree(self.pub_img_path)
        mkdir(self.pub_img_path)


image_helper = ImageHelper()
