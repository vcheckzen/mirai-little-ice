from mirai import Plain, Image


class Command:
    def __init__(self):
        self.chat_mode = False
        self.handlers = {
            '开启聊天模式': self.__open_chat_mode__,
            '关闭聊天模式': self.__close_chat_mode__
        }

    def __open_chat_mode__(self):
        self.chat_mode = True
        return [Plain('好的，现在你可以直接发消息，不需要@我！要退出的话，发送“关闭聊天模式”')]

    def __close_chat_mode__(self):
        self.chat_mode = False
        return [Plain('玩去喽，有事@我！')]
