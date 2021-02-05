from apscheduler.schedulers.asyncio import AsyncIOScheduler 
from discord.ext.commands import Bot as BotBase
# Discord's preivileged gateway intents 
# (go to discord's Developer Portal > Application > discoRd > Bot)
from discord import Intents 
from discord import File
from datetime import datetime
from lib.bot.create_embed import create_embed

# Bot command prefix
PREFIX = "+"

class Bot(BotBase):
	def __init__(self):
		self.PREFIX = PREFIX
		self.ready = False
		self.guild = None
		self.scheduler = AsyncIOScheduler()

		# Inherits BotBase
		super().__init__(
			command_prefix=PREFIX, 
			intents=Intents.all()
		)

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

	async def on_ready(self):
		if not self.ready:
			self.ready = True

			# Set server-specific bot using server ID
			# Can leave this out for multi-server bot
			self.guild = self.get_guild(806626416783130674)
			print("bot ready")

			# Set channel using channel ID
			channel = self.get_channel(806950823396769883)
			await channel.send("Now online!")

			# Create and send embed to channel
			fields = [
				("Name1", "Value1", True),
				("Name2", "Value2", True),
				("A longer Name", "A longer Value", False)
			]

			embed = create_embed(
				title = "Now online!",
				description = "discoRd-bot is now online!",
				colour = 0xFF0000,
				timestamp = datetime.utcnow(),
				fields = fields,
				author = "discoRd-bot",
				author_icon = self.guild.icon_url,
				thumbnail = self.guild.icon_url,
				image = self.guild.icon_url,
				footer = "testing a footer"
			)

			await channel.send(embed=embed)

		else:
			print("bot reconnected")

	# When bot receives a message from a channel
	async def on_message(self, message):
		pass

# Create an instance of Bot
bot = Bot()