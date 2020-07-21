import json

from utils.base import UtilBase


class Config(UtilBase):
    with open('config/config.json') as f:
        config = json.load(f)


config = Config.config
