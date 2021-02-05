from discord import	Intents
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext.commands import Bot as BotBase
from discord import Intents
from discord import File
from datetime import datetime
from lib.bot.create_embed import create_embed

PREFIX = "+"

class Bot(BotBase):
	def __init__(self):
		self.PREFIX = PREFIX
		self.ready = False
		self.guild = None
		self.scheduler = AsyncIOScheduler()

		super().__init__(
			command_prefix=PREFIX, 
			intents=Intents.all()
		)

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

	async def on_ready(self):
		if not self.ready:
			self.ready = True
			self.guild = self.get_guild(806626416783130674)
			print("bot ready")

			channel = self.get_channel(806950823396769883)
			await channel.send("Now online!")

			fields = [
				("Name1", "Value1", True),
				("Name2", "Value2", True),
				("A longer Name", "A longer Value", False)
			]

			embed = create_embed(
				title = "Now online!",
				description = "discoRd-bot is now online!",
				colour = 0xc88ffb,
				timestamp = datetime.utcnow(),
				fields = fields,
				author = "discoRd-bot",
				author_icon = self.guild.icon_url,
				thumbnail = self.guild.icon_url,
				image = self.guild.icon_url,
				footer = "iamericfletcher - testing a footer"
			)

			await channel.send(embed=embed)
			# Display image below the embed.
			await channel.send(file=File("./data/images/discoRd_logo_2.png"))

		else:
			print("bot reconnected")

	async def on_message(self, message):
		pass

bot = Bot()