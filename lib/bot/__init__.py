from discord import	Intents
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import Context, CommandNotFound, BadArgument
from discord import Intents
from discord import File
from datetime import datetime
from lib.bot.create_embed import create_embed
from glob import glob
from asyncio import sleep
from discord.errors import HTTPException, Forbidden
from discord.ext.commands import (CommandNotFound, BadArgument, MissingRequiredArgument)

from ..db import db

PREFIX = "$"
# Goes through the directory and return any .py file
COGS = [path.split("/")[-1][:-3] for path in glob("./lib/cogs/*.py")]
IGNORE_EXCEPTIONS = (CommandNotFound, BadArgument)


class Ready(object):
	def __init__(self):
		for cog in COGS:
			setattr(self, cog, False)

	def ready_up(self, cog):
		setattr(self, cog, True)
		print(f" {cog} cog ready")

	def all_ready(self):
		return all([getattr(self, cog) for cog in COGS])


class Bot(BotBase):
	def __init__(self):
		self.PREFIX = PREFIX
		self.ready = False
		self.cogs_ready = Ready()
		self.guild = None
		self.scheduler = AsyncIOScheduler()

		db.autosave(self.scheduler)

		super().__init__(
			command_prefix=PREFIX, 
			intents=Intents.all()
		)

	def setup(self):
		for cog in COGS:
			self.load_extension(f"lib.cogs.{cog}")
			print(f" {cog} cog loaded")

		print("setup complete!")

	def run(self, version):
		self.VERSION = version

		print("running setup...!")
		self.setup()

		with open("./lib/bot/token.0", "r", encoding="utf-8") as tf:
			self.TOKEN = tf.read()

		print("running bot...")
		super().run(self.TOKEN, reconnect=True)

	# Don't allow commands to be sent until the bot is ready.
	async def process_commands(self, message):
		ctx = await self.get_context(message, cls=Context)

		if ctx.command is not None and ctx.guild is not None:
			if self.ready:
				await self.invoke(ctx)

			else:
				await ctx.send("I am not ready to receive commands. Please wait a few seconds.")

	async def rules_reminder(self):
		await self.stdout.send("I am a timed notification!")

	async def on_connect(self):
		print(" bot connected!")

	async def on_disconnect(self):
		print("bot disconnected")

	async def on_error(self, err, *args, **kwargs):

		if err == "on_command_error":
			await args[0].send("Something went wrong.")

		else:
			await self.stdout.send("Oh no! An error occurred.")

		raise

	async def on_command_error(self, ctx, exc):
		if any([isinstance(exc, error) for error in IGNORE_EXCEPTIONS]):
			pass

		elif isinstance(exc, BadArgument):
			pass

		elif isinstance(exc, MissingRequiredArgument):
			await ctx.send("One or more required arguments are missing.")

		elif isinstance(exc.original, HTTPException):
			await ctx.send("Unable to send message")

		elif isinstance(exc.original, Forbidden):
			await ctx.send("I do not have permission to do that.")

		else:
			raise exc.original

	async def on_ready(self):
		if not self.ready:
			self.guild = self.get_guild(806626416783130674)
			self.stdout = self.get_channel(806950823396769883)
			self.scheduler.add_job(self.rules_reminder, CronTrigger(minute=59))
			self.scheduler.start()

			# fields = [
			# 	("Name1", "Value1", True),
			# 	("Name2", "Value2", True),
			# 	("A longer Name", "A longer Value", False)
			# ]
			#
			# embed = create_embed(
			# 	title = "Now online!",
			# 	description = "discoRd-bot is now online!",
			# 	colour = 0xc88ffb,
			# 	timestamp = datetime.utcnow(),
			# 	fields = fields,
			# 	author = "discoRd-bot",
			# 	author_icon = self.guild.icon_url,
			# 	thumbnail = self.guild.icon_url,
			# 	image = self.guild.icon_url,
			# 	footer = "iamericfletcher - testing a footer."
			# )
			#
			# await channel.send(embed=embed)
			# # Display image below the embed.
			# await channel.send(file=File("./data/images/discoRd_logo_2.png"))

			while not self.cogs_ready.all_ready():
				await sleep(0.5)

			await self.stdout.send("Now online!")
			self.ready = True
			print(" bot ready")

		else:
			print("bot reconnected")

	async def on_message(self, message):
		if not message.author.bot:
			await self.process_commands(message)


bot = Bot()
