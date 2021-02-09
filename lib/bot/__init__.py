# For scheduled tasks
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from discord.ext.commands import Bot as BotBase
from discord.ext.commands import CommandNotFound
# Discord's preivileged gateway intents
# (go to discord's Developer Portal > Application > discoRd > Bot)
from discord import Intents
from discord import File
from datetime import datetime
from lib.bot.create_embed import create_embed
from lib.bot.idle_reminder import idle_reminder
from lib.db import db

# Bot command prefix
PREFIX = "$"
# Avoid magic numbers
SERVER_ID = 806626416783130674
CHANNEL_TEST = 806950823396769883
# If the last message sent in a channel was longer than this number of minutes,
# the idle reminder will send the reminder
IDLE_REMINDER_MINUTES = 5


class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready = False
        self.guild = None
        self.scheduler = AsyncIOScheduler()

        db.autosave(self.scheduler)

        # Inherits BotBase
        super().__init__(command_prefix=PREFIX, intents=Intents.all())

    # Initializes bot using TOKEN
    def run(self, version):
        self.VERSION = version

        with open("./lib/bot/token.0", "r", encoding="utf-8") as tf:
            self.TOKEN = tf.read()

        print("running bot...")
        super().run(self.TOKEN, reconnect=True)

    # Print message for scheduled job
    async def idle_reminder(self, minutes):
        # TODO create an embed and pass it to the function:
        # embed = create_embed()
        await idle_reminder(self.get_channel(CHANNEL_TEST), minutes)

    async def on_connect(self):
        print("bot connected!")

    async def on_disconnect(self):
        print("bot disconnected")

    # Error event handling for when a command results in an error
    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            await args[0].send("Something went wrong.")

        channel_test = self.get_channel(CHANNEL_TEST)
        await channel_test.send("An error occured.")

    # Command error event handling
    async def on_command_error(self, ctx, exception):
        # Checks if bot command is not found
        if isinstance(exception, CommandNotFound):
            pass

        else:
            raise exception.original

    async def on_ready(self):
        if not self.ready:
            self.ready = True
            # Checks every minute
            self.scheduler.add_job(self.idle_reminder,
                                   CronTrigger(second="0"),
                                   [IDLE_REMINDER_MINUTES])
            self.scheduler.start()

            # Set server-specific bot using server ID
            # Can leave this out for multi-server bot
            self.guild = self.get_guild(SERVER_ID)
            print("bot ready")

            # Set channel_test using channel ID
            channel_test = self.get_channel(CHANNEL_TEST)
            await channel_test.send("Now online!")

            # # Create and send embed to channel
            # fields = [
            #     ("Name1", "Value1", True),
            #     ("Name2", "Value2", True),
            #     ("A longer Name", "A longer Value", False)
            # ]

            # embed = create_embed(
            #     title = "Now online!",
            #     description = "discoRd-bot is now online!",
            #     colour = 0xFF0000,
            #     timestamp = datetime.utcnow(),
            #     fields = fields,
            #     author = "discoRd-bot",
            #     author_icon = self.guild.icon_url,
            #     thumbnail = self.guild.icon_url,
            #     image = self.guild.icon_url,
            #     footer = "testing a footer"
            # )

            # await channel_test.send(embed=embed)

        else:
            print("bot reconnected")

    # When bot receives a message from a channel
    async def on_message(self, message):
        pass

# Create an instance of Bot
bot = Bot()
