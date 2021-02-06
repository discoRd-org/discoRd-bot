from discord.ext.commands import Cog
from discord.ext.commands import command
from random import choice, randint
from discord import Member
from typing import Optional


class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="hello", aliases=["hi"])
    async def say_hello(self, ctx):
        await ctx.send(f"{choice(('Hello', 'Hi', 'Hey', 'Hiya'))} {ctx.author.mention}!")

    @command(name="dice", aliases=["roll"])
    async def roll_dice(self, ctx, die_string: str):
        dice, value = (int(term) for term in die_string.split("d"))
        rolls = [randint(1, value) for i in range(dice)]
        await ctx.send(f"{ctx.author.mention} see below for results!\n"
                       f"Number of dice: {value}\n"
                       f"Maximum number: : {dice}")
        await ctx.send(" + ".join([str(r) for r in rolls]) + f" = {sum(rolls)}")

    @command(name="slap", aliases=["hit"])
    async def slap_member(self, ctx, member: Member, *, reason: Optional[str] = "for no reason at all!"):
        await ctx.send(f"{ctx.author.mention} slapped {member.display_name} {reason }!")

    @command(name="echo", aliases=["say"])
    async def echo_message(self, ctx, *, message):
        await ctx.message.delete()
        await ctx.send(message)


    # Listen for events
    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("fun")


def setup(bot):
    # Also can use to schedule tasks
    bot.add_cog(Fun(bot))

