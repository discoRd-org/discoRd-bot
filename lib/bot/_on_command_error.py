from discord.ext.commands import CommandNotFound


# Command error event handling
async def on_command_error(self, ctx, exception):
    # Checks if bot command is not found
    if isinstance(exception, CommandNotFound):
        pass

    else:
        raise exception
