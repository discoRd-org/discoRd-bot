from discord.ext.commands import Cog


class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot

    # Listen for events
    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("fun")


def setup(bot):
    # Also can use to schedule tasks
    bot.add_cog(Fun(bot))

