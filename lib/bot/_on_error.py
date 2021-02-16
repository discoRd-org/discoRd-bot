import lib.constants as const


# Error event handling for when a command results in an error
async def on_error(self, err, *args, **kwargs):
    if err == "on_command_error":
        await args[0].send("Something went wrong.")

    channel_test = self.get_channel(const.CHANNEL_TEST)
    await channel_test.send("An error occured.")
    raise(err)
