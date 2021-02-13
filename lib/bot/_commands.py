from discord.ext.commands import command
from discord import Member, TextChannel

import lib.constants as const


@command(name="move")
async def move_message(self, ctx, member: Member, target_channel: TextChannel,
                       num_msg: int = 1):
    print("Running 'move' command")
    counter = 0
    msg_to_move = list()
    async for msg in ctx.channel.history(limit=const.CHANNEL_MSG_HISTORY_LIMIT):
        if counter >= num_msg:
            break
        if msg.author.id == member.id:
            msg_to_move.append(msg)
            counter += 1

    msg_to_move.reverse()  # Order messages collected from oldest to newest
    await ctx.channel.send("Test!")


@command(name="ping")
async def ping(self, ctx):
    await ctx.send("Pong!")
