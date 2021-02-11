from datetime import datetime, timedelta, timezone


async def idle_reminder(channel, wait_minutes, embed):
    """
    Checks if 'channel' has been idle for more than 'wait_minutes'
    minutes. If so, sends an embed to that channel.

    Args:
        channel (TextChannel): Which channel to check.
        wait_minutes (int): Check this many minutes since last message passed.
        embed (embed): An embed object to send

    Returns:
        None
    """
    print("Running idle_reminder()")

    last_message = await channel.history(limit=1).flatten()

    if not last_message[0].author.bot:
        now_time = datetime.now(tz=timezone.utc)
        last_time = last_message[0].created_at.replace(tzinfo=timezone.utc)
        wait_time = timedelta(minutes=wait_minutes)
        delta = now_time - last_time

        if delta > wait_time:
            await channel.send(embed=embed)
