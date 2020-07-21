from mirai import At, AtAll, Plain, Image, Face

from utils.config import config
from utils.image import image_helper


class Response:
    def __init__(self, group, member, message, command, plugin):
        self.group = group
        self.member = member
        self.message = message
        self.command = command
        self.plugin = plugin

        self.ats = message.getAllofComponent(At)
        self.at_alls = message.getAllofComponent(AtAll)
        self.plains = message.getAllofComponent(Plain)
        self.faces = message.getAllofComponent(Face)
        self.images = message.getAllofComponent(Image)
        self.plain_text = ' '.join((p.text.strip()
                                    for p in self.plains)).strip()

        self.responses = []

    def __handle_at_all__(self):
        if self.at_alls:
            self.responses.append(Plain('遇到问题了吗，先尝试下公告的解决方案吧！'))
            return 'END'

    def __handle_command__(self):
        self.responses.extend(self.command.handlers[self.plain_text]())

    def __handle_plain_text__(self):
        if self.plain_text in self.command.handlers:
            self.__handle_command__()
            return 'END'
        elif self.plain_text:
            self.responses.extend(
                self.plugin.chat_with_text(self.plain_text))

    def __handle_image__(self):
        if self.images:
            name = image_helper.download_img(self.images[0].url)
            self.responses.extend(self.plugin.chat_with_image(name))

    def __handle_face__(self):
        if self.faces:
            self.responses.extend(self.faces*2)

    def get_response(self):
        if self.__handle_at_all__():
            return self.responses

        if not self.command.chat_mode:
            bot = config['mirai_http_api']['qq']
            if bot not in (at.target for at in self.ats):
                return self.responses

        if self.__handle_plain_text__():
            return self.responses

        self.__handle_face__()
        self.__handle_image__()

        if not self.responses:
            rand_img = image_helper.get_rand_img(
                config['image']['not_understand'])
            return [Image.fromFileSystem(rand_img)]

        return self.responses
