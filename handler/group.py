import json

from mirai import At

from plugins.ice import Ice
from handler.command import Command
from handler.response import Response


class GroupHandler:
    plugin = Ice()

    def __init__(self):
        self.command = Command()

    async def handle(self, app, group, member, message):
        r = Response(group, member, message, self.command,
                     self.plugin).get_response()
        if r:
            r.insert(0, At(target=member.id))
            await app.sendGroupMessage(group.id, r)
