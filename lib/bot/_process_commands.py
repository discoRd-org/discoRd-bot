from discord.ext.commands import Context


async def process_commands(self, message):
    ctx = await self.get_context(message, cls=Context)

    if ctx.command is not None and ctx.guild is not None:
        if self.ready:
            await self.invoke(ctx)
        else:
            await ctx.send("I'm not ready to receive commands. " +
                           "Please wait a few seconds.")
