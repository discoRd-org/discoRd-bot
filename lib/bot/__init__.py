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
CHANNEL_HELP_AVAILABLE = 809099330950529085
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
            # Set server-specific bot using server ID
            # Can leave this out for multi-server bot
            self.guild = self.get_guild(SERVER_ID)

            embed_help = create_embed(title=":question: How to ask a good question?",
                                      description="""**A minimal reproducible question** (a.k.a. a good question) should consist of the following:

                                      **1. A clear problem statement.** What are you trying to do? What have you tried? What is the expected output?
                                      **2. The smallest data set necessary to reproduce the problem.** Hint: Use `dput` and **no screenshots**.
                                      **3. All relevant code** that everyone can just copy and paste into their R console.
                                      **4. Proper `formatting` of code blocks and data** if you copy and paste directly.
                                      **5. All relevant packages** needed to reproduce your problem.
                                      **6. All relevant error messages**. Don't just say that you got an error.

                                      For more details, check out: `How to ask a good question? (Detailed)`""",
                                      colour=0xFF0000,
                                      author="discoRd-bot",
                                      author_icon=self.guild.icon_url,
                                      thumbnail=self.guild.icon_url,
                                      image=self.guild.icon_url)

            # Add a job to the scheduler
            self.scheduler.add_job(idle_reminder,
                                   CronTrigger(second="0"),
                                   [self.get_channel(CHANNEL_HELP_AVAILABLE),
                                    IDLE_REMINDER_MINUTES,
                                    embed_help])
            self.scheduler.start()

            print("bot ready")

            # Set channel_test using channel ID
            channel_test = self.get_channel(CHANNEL_TEST)
            await channel_test.send("Now online!")

        else:
            print("bot reconnected")

    # When bot receives a message from a channel
    async def on_message(self, message):
        pass

# Create an instance of Bot
bot = Bot()
