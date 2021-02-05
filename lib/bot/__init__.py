from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext.commands import Bot as BotBase
from discord import Intents
from discord import File
from datetime import datetime

PREFIX = "+"
OWNER_IDS = [750693589532672100]

class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready = False
        self.guild = None
        self.scheduler = AsyncIOScheduler()

        super().__init__(command_prefix=PREFIX, owner_ids=OWNER_IDS)

        def run(self, version):
            self.VERSION = version

            with open("./lib/bot/token.0.0", "r", encoding="utf-8") as tf:
                self.TOKEN = tf.read()

            print("running bot...")
            super().run(self.TOKEN, reconnect=True)

        async def one_connect(self):
            print("bot connected")

        async def on_disconnect(self):
            print("bot disconnected")

        async def on_ready(self):
            if not self.ready:
                self.ready = True
                self.guild = self.get_guild(806626416783130674)
                print("bot ready")
            else:
                print("bot reconnected")

        async def on_message(self, message):
            pass


bot = Bot()

