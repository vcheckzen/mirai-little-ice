from apscheduler.schedulers.asyncio import AsyncIOScheduler

from mirai import Image

from utils.config import config
from utils.image import image_helper


class TaskHandler:
    tasks = AsyncIOScheduler()
    tasks.add_job(image_helper.del_pub_imgs, 'interval', hours=1)
    tasks.start()

    def __init__(self, app, group):
        self.app = app
        self.group = group
        self.tasks.add_job(self.good_night, 'cron',
                           day_of_week='0-6', hour=22, minute=30)

    async def good_night(self):
        rand_img = image_helper.get_rand_img(config['image']['good_night'])
        await self.app.sendGroupMessage(self.group, [Image.fromFileSystem(rand_img)])
