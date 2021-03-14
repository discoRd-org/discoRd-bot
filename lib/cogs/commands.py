from discord import Member, TextChannel, File
from discord.ext.commands import Cog, command
from discord.ext.commands import (CommandInvokeError)
from typing import Optional
import re # Regular expressions
import io
import lib.constants as const
from lib.bot.create_embed import create_embed  # For embed creation


class GeneralCommand(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="ping")
    async def ping_test(self, ctx):
        """
        Ping the bot to test if it's responding
        """
        await ctx.send("pong!")

    async def transfer_message(self, ctx, 
                        member: Member,
                        target_channel: TextChannel, 
                        msgs: str = "1",
                        copy: bool = True,
                        reason: Optional[str] = "No reason"):       
        """
        Copy/Move message(s), mentioning the author. Several messages will
        be consolidated to one message separated by a new line.

        member: Member. Mention or user ID to move messages for.
        target_channel: TextChannel. The channel to copy/move to.
        msgs(optional): str. 
                        "d" - How many user messages to move? 
                        "d-d" - Range of messages to move?
                        "<msgID>" - Which message to move?
                        "<msgID>,d" - How many message starting from <msgID> to move?
                        Defaults to "1".
        copy(optional): bool. If True, the original messages will not be deleted.
                        Defaults to 'True'.
        reason(optional): str. Reason for moving/copying message.
                          Defaults to 'No reason".
        """
        print("Running 'Move' command")

        # Delete calling message, and also avoids moving the command itself
        # When the user moves their own messages
        await ctx.message.delete()

        # `<msgID>,d` form
        if re.search(r"^\d+,\d+$", msgs):
            msgs = msgs.split(",")
        else:
            msgs = [msgs]

        # Parse msgs argument
        image_types = ["png", "jpeg", "gif", "jpg"]
        msg_to_move = list()
        msg_attachments = list()

        for msg_params in msgs:
            # `<msgID>` form
            if re.search(r"^\d+$", msg_params) and len(msg_params) > 3:
                msg_by_id = await ctx.channel.fetch_message(msg_params)

                if msg_by_id.author.id == member.id:
                    # Download any attachments
                    for attachment in msg_by_id.attachments:
                        if any(attachment.filename.lower().endswith(image) for image in image_types):
                            msg_attachments.append(await attachment.to_file(use_cached = True))
                        else:
                            fp = io.BytesIO()
                            await attachment.save(fp)
                            msg_attachments.append(File(fp, filename=attachment.filename, spoiler=attachment.is_spoiler()))
                            
                    msg_to_move.append(msg_by_id)
                else:
                    await ctx.channel.send("Message not by selected member")
                    return
            # `d` or `d-d` form
            else:
                if re.search(r"^\d+-\d+$", msg_params):
                    msg_from, msg_to = (int(num) for num in msg_params.split("-"))
                    msg_from -= 1
                    msg_params = msg_to - msg_from
                elif re.search(r"^\d+$", msg_params):
                    msg_from = 0
                    msg_to = int(msg_params)
                    msg_params = int(msg_params)
                else:
                    await ctx.channel.send("`msgs` argument not in proper format")
                    return

                counter = 0
                msg_counter = 0
                # Retreive messages before the selected message 
                # if `msgs` in the form `<msg_id>,<num_msgs>`
                if len(msgs) == 2:
                    msg_before = msg_to_move[0]
                else:
                    msg_before = None
                
                async for msg in ctx.channel.history(limit=const.CHANNEL_MSG_HISTORY_LIMIT, before=msg_before):
                    if counter >= msg_params:
                        break
                    if msg.author.id == member.id:
                        if msg_counter >= msg_from and msg_counter < msg_to:
                            msg_to_move.append(msg)

                            # Download any attachments
                            for attachment in msg.attachments:
                                if any(attachment.filename.lower().endswith(image) for image in image_types):
                                    msg_attachments.append(await attachment.to_file(use_cached = True))
                                else:
                                    fp = io.BytesIO()
                                    await attachment.save(fp)
                                    msg_attachments.append(File(fp, filename=attachment.filename, spoiler=attachment.is_spoiler()))
                                
                            counter += 1
                        msg_counter += 1

        msg_to_move.reverse()  # Order messages collected from oldest to newest
        msg_all = ""
        for msg in msg_to_move:
            msg_all += msg.content + "\n"

        if not msg_all:
            msg_all = "<No text>"

        copied_bool = {True: "Copied", False: "Moved"}

        embed_move = create_embed(title=f"Message {copied_bool[copy]} from another channel",
                                  description=msg_all,
                                  colour=0x4A90E2,
                                  author=member.display_name,
                                  author_icon=member.avatar_url,
                                  footer=const.EMBED_DEFAULT_FOOTER)

        embed_move.add_field(name=f"{copied_bool[copy]} from", value=ctx.channel.mention, inline=True)
        embed_move.add_field(name=f"{copied_bool[copy]} by", value=ctx.author.mention, inline=True)
        embed_move.add_field(name=f"Reason", value=reason, inline=False)

        await target_channel.send(f"{member.mention}")
        await target_channel.send(embed=embed_move)

        # Send attachments if any exists
        if msg_attachments:
            await target_channel.send(files=list(reversed(msg_attachments)))

        # Delete original message copy command is used
        if not copy:
            if isinstance(msgs, str) and len(msgs) > 3:
                await msg_by_id.delete()
            else:
                for msg in msg_to_move:
                    await msg.delete()


    @command(name="move", aliases=["mv"])
    async def move_message(self, ctx, 
                        member: Member,
                        target_channel: TextChannel, 
                        msgs: str = "1",
                        *, reason: Optional[str] = "No reason"):
        """
        Move message(s), mentioning the author. Several messages will
        be consolidated to one message separated by a new line.

        member: Member. Mention or user ID to move messages for.
        target_channel: TextChannel. The channel to move to.
        msgs(optional): str. 
                        "d" - How many user messages to move? 
                        "d-d" - Range of messages to move?
                        "<msgID>" - Which message to move?
                        "<msgID>,d" - How many message starting from <msgID> to move?
                        Defaults to "1".
        reason(optional): str. Reason for moving message.
                          Defaults to 'No reason".
        """
        await self.transfer_message(ctx, member, target_channel, msgs, False, reason)

    @move_message.error
    async def move_message_error(self, ctx, exc):
        if isinstance(exc, CommandInvokeError):
            await ctx.send("Unknown Message. Make sure you're moving a message from this channel")
            raise exc.original

    @command(name="copy", aliases=["cp"])
    async def copy_message(self, ctx, 
                        member: Member,
                        target_channel: TextChannel, 
                        msgs: str = "1",
                        *, reason: Optional[str] = "No reason"):
        """
        Copy message(s), mentioning the author. Several messages will
        be consolidated to one message separated by a new line.

        member: Member. Mention or user ID to copy messages for.
        target_channel: TextChannel. The channel to copy to.
        msgs(optional): str. 
                        "d" - How many user messages to move? 
                        "d-d" - Range of messages to move?
                        "<msgID>" - Which message to move?
                        "<msgID>,d" - How many message starting from <msgID> to move?
                        Defaults to "1".
        reason(optional): str. Reason for copying message.
                          Defaults to 'No reason".
        """
        await self.transfer_message(ctx, member, target_channel, msgs, True, reason)

    @copy_message.error
    async def copy_message_error(self, ctx, exc):
        if isinstance(exc, CommandInvokeError):
            await ctx.send("Unknown Message. Make sure you're copying a message from this channel")
            raise exc.original

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("commands")


def setup(bot):
    bot.add_cog(GeneralCommand(bot))
