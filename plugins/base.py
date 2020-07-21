import typing as T
from abc import ABCMeta, abstractmethod

from mirai import MessageChain
from mirai.image import InternalImage
from mirai.event.message.base import BaseMessageComponent


class PluginBase(metaclass=ABCMeta):
    @abstractmethod
    def chat_with_text(self, text: str) -> T.Union[
        MessageChain,
        BaseMessageComponent,
        T.List[T.Union[BaseMessageComponent, InternalImage]],
        str
    ]:
        pass

    @abstractmethod
    def chat_with_image(self, image_path: str, image_url: str = None) -> T.Union[
        MessageChain,
        BaseMessageComponent,
        T.List[T.Union[BaseMessageComponent, InternalImage]],
        str
    ]:
        pass
