from glob import glob
from discord.ext.commands import CommandNotFound, CommandInvokeError
import platform

# Bot command prefix
PREFIX = "$"
# Avoid magic numbers
SERVER_ID = 806626416783130674
CHANNEL_TEST = 806950823396769883
CHANNEL_HELP_AVAILABLE = 809099330950529085
EMBED_DEFAULT_FOOTER = "This is an automated message"
# If the last message sent in a channel was longer than this number of minutes,
# the idle reminder will send the reminder
IDLE_REMINDER_MINUTES = 20
# Every 10 minutes
IDLE_REMINDER_CRON_TIMER = {"second": "0", "minute": "0,10,20,30,40,50"}
CHANNEL_MSG_HISTORY_LIMIT = 100  # Look up a maximum of this many past messages
# Ignore these errors. Already defined as command specific errors
IGNORED_EXCEPTIONS = (CommandNotFound, CommandInvokeError) 

if platform.system() == "Linux":
    COGS = [path.split("/")[-1][:-3] for path in glob("./lib/cogs/*.py")]
elif platform.system() == "Windows":
    COGS = [path.split("\\")[-1][:-3] for path in glob("./lib/cogs/*.py")]
else:
    raise(RuntimeError("Unexpected operating system"))
