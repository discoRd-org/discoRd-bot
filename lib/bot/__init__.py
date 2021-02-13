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
import lib.bot._commands as cmd  # Bot commands

from lib.db import db  # Database
import lib.constants as const  # Bot constants


class Bot(BotBase):

    def __init__(self):
        self.PREFIX = const.PREFIX
        self.ready = False
        self.guild = None
        self.scheduler = AsyncIOScheduler()

        db.autosave(self.scheduler)

        # Inherits BotBase
        super().__init__(command_prefix=const.PREFIX, intents=Intents.all())

    # Initializes bot using TOKEN
    def run(self, version):
        self.VERSION = version

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

    # Bot commands
    move_message = cmd.move_message
    ping = cmd.ping


# Create an instance of Bot
bot = Bot()
