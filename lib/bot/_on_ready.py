from apscheduler.triggers.cron import CronTrigger  # For scheduled tasks
from lib.bot.create_embed import create_embed  # For embed creation
from lib.bot.idle_reminder import idle_reminder  # To add as a scheduled job
import lib.constants as const


async def on_ready(self):
    if not self.ready:
        self.ready = True
        # Set server-specific bot using server ID
        # Can leave this out for multi-server bot
        self.guild = self.get_guild(const.SERVER_ID)

        embed_help = create_embed(title=":question: How to ask a good question?",
                                  description="""**A minimal reproducible question** (a.k.a. a good question) should consist of the following:

                                  **1. A clear problem statement.** What are you trying to do? What have you tried? What is the expected output?
                                  **2. The smallest data set necessary to reproduce the problem.** Hint: Use `dput` and **no screenshots**.
                                  **3. All relevant code** that everyone can just copy and paste into their R console.
                                  **4. Proper `formatting` of code blocks and data** if you copy and paste directly.
                                  **5. All relevant packages** needed to reproduce your problem.
                                  **6. All relevant error messages**. Don't just say that you got an error.

                                  For more details, check out: `How to ask a good question? (Detailed)`""",
                                  colour=0xFF0000,
                                  author="discoRd-bot",
                                  author_icon=self.guild.icon_url,
                                  thumbnail=self.guild.icon_url,
                                  image=self.guild.icon_url)

        # Add a job to the scheduler
        self.scheduler.add_job(idle_reminder,
                               CronTrigger(**const.IDLE_REMINDER_CRON_TIMER),
                               [self.get_channel(const.CHANNEL_HELP_AVAILABLE),
                                const.IDLE_REMINDER_MINUTES,
                                embed_help])
        self.scheduler.start()

        print("bot ready")

        # Set channel_test using channel ID
        channel_test = self.get_channel(const.CHANNEL_TEST)
        await channel_test.send("Now online!")

    else:
        print("bot reconnected")
