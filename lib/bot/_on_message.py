# When bot receives a message from a channel
async def on_message(self, message):
    if not message.author.bot:
        await self.process_commands(message)
