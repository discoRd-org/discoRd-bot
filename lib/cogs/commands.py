from discord import Member, TextChannel, File
from discord.ext.commands import Cog, command
import tempfile
import lib.constants as const


class GeneralCommand(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="ping")
    async def ping_test(self, ctx):
        """
        Ping the bot to test if it's responding
        """
        await ctx.send("pong!")

    @command(name="move")
    async def move_message(self, ctx, member: Member,
                           target_channel: TextChannel, num_msg: int = 1,
                           copy: bool = False):
        """
        Copy/Move message(s), mentioning the author. Several messages will
        be consolidated to one message separated by a new line.

        member: Member. Mention or user ID to move messages for.
        target_channel: TextChannel. The channel to copy/move to.
        num_msg(optional): Integer. How many user messages to move?
                           Defaults to 1.
        copy(optional): Bool. If True, the original messages will be deleted.
                        Defaults to 'False'.
        """
        print("Running 'move' command")

        # Delete calling message, and also avoids moving the command itself
        # When the user moves their own messages
        await ctx.message.delete()

        counter = 0
        msg_to_move = list()
        async for msg in ctx.channel.history(limit=const.CHANNEL_MSG_HISTORY_LIMIT):
            if counter >= num_msg:
                break
            if msg.author.id == member.id:
                msg_to_move.append(msg)
                counter += 1

        msg_to_move.reverse()  # Order messages collected from oldest to newest
        msg_all = ""
        attachments_all = list()
        for msg in msg_to_move:
            attachments_all.extend(msg.attachments)
            msg_all += msg.content + "\n"

        await target_channel.send(f"Original message by: {member.mention}")
        await target_channel.send(msg_all)

        if attachments_all:
            for att in attachments_all:
                tmp = tempfile.TemporaryFile("w+b")
                tmp.write(await att.read())
                await target_channel.send(File(tmp, att.filename))
                tmp.close()

        if not copy:
            for msg in msg_to_move:
                await msg.delete()

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs.ready_up("commands")


def setup(bot):
    bot.add_cog(GeneralCommand(bot))
