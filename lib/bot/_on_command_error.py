from discord.ext.commands import CommandInvokeError, BadArgument, MissingRequiredArgument
from discord.errors import NotFound, HTTPException, Forbidden
import lib.constants as const  # Bot constants

# Command error event handling
async def on_command_error(self, ctx, exc):
    if any([isinstance(exc, error) for error in const.IGNORED_EXCEPTIONS]):
        pass

    elif isinstance(exc, BadArgument):
        await ctx.send("Bad arguments")

    elif isinstance(exc, MissingRequiredArgument):
        await ctx.send("Missing required arguments")

    elif isinstance(exc, NotFound):
        await ctx.send("Message not found")

    elif isinstance(exc, HTTPException):
        await ctx.send("Unable to send message")

    elif isinstance(exc, Forbidden):
        await ctx.send("I do not have permission to do that")

    raise exc.original
