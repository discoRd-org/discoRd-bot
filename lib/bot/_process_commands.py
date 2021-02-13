from discord.ext.commands import Context


async def process_commands(self, message):
    ctx = await self.get_context(message, cls=Context)

    # Debug prints
    print(ctx)
    print(ctx.valid)
    print(ctx.command) # Problem, it's None
    print(ctx.guild)

    if ctx.command is not None and ctx.guild is not None:
        if self.ready:
            print("Command is processed in 'process_command()'")  # Debug
            await self.invoke(ctx)
        else:
            await ctx.send("I'm not ready to receive commands. " +
                           "Please wait a few seconds.")
