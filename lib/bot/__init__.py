from apscheduler.schedulers.asyncio import AsyncIOScheduler  # Scheduler init

from discord.ext.commands import Bot as BotBase
# Discord's preivileged gateway intents
# (go to discord's Developer Portal > Application > discoRd > Bot)
from discord import Intents

# Bot methods
from lib.bot._on_ready import on_ready
from lib.bot._on_connect import on_connect
from lib.bot._on_disconnect import on_disconnect
from lib.bot._on_message import on_message
from lib.bot._on_error import on_error
from lib.bot._on_command_error import on_command_error
from lib.bot._process_commands import process_commands

from lib.db import db  # Database
import lib.constants as const  # Bot constants

# Cogs Ready class 
class Ready(object):
    def __init__(self):
        for cog in const.COGS:
            setattr(self, cog, False)

    def ready_up(self, cog):
        setattr(self, cog, True)
        print(f"  {cog} cog ready")

    def all_ready(self):
        return all([getattr(self, cog) for cog in const.COGS])


class Bot(BotBase):

    def __init__(self):
        self.PREFIX = const.PREFIX
        self.ready = False
        self.cogs_ready = Ready() # Instantiate cogs ready
        self.guild = None
        self.scheduler = AsyncIOScheduler()

        db.autosave(self.scheduler)

        # Inherits BotBase
        super().__init__(command_prefix=const.PREFIX, intents=Intents.all())

    # Loads extensions such as cogs / commands / listeners
    def setup(self):
        for cog in const.COGS:
            self.load_extension(f"lib.cogs.{cog}")
            print(f"  {cog} cog loaded")

    # Initializes bot using TOKEN
    def run(self, version):
        self.VERSION = version

        print("running setup...")
        self.setup()

        with open("./lib/bot/token.0", "r", encoding="utf-8") as tf:
            self.TOKEN = tf.read()

        print("running bot...")
        super().run(self.TOKEN, reconnect=True)

    on_connect = on_connect
    on_disconnect = on_disconnect
    on_error = on_error
    on_command_error = on_command_error
    on_ready = on_ready
    on_message = on_message
    process_commands = process_commands


# Create an instance of Bot
bot = Bot()
