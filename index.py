from mirai import Mirai, Group, Member, MessageChain, GroupMessage

from utils.config import config
from handler.task import TaskHandler
from handler.group import GroupHandler

groups = {}
cfg = config['mirai_http_api']
lnk = 'mirai://{}?authKey={}&qq={}'
app = Mirai(lnk.format(cfg['address'], cfg['auth_key'], cfg['qq']))


@app.receiver(GroupMessage)
async def GMHandler(app: Mirai, group: Group, member: Member, message: MessageChain):
    if group.id not in groups:
        groups[group.id] = GroupHandler()
        TaskHandler(app, group.id)

    await groups[group.id].handle(app, group, member, message)


if __name__ == "__main__":
    app.run()
