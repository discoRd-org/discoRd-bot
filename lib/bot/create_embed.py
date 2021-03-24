from typing import List, Tuple
from discord import Embed
from datetime import datetime

def create_embed(
    title: str,
    description: str,
    fields: List[Tuple[str, str, bool]] = Embed.Empty,
    colour: str = Embed.Empty,
    timestamp: datetime = datetime.utcnow(),
    author: str = Embed.Empty,
    author_icon: str = Embed.Empty,
    thumbnail: str = Embed.Empty,
    image: str = Embed.Empty,
    footer: str = Embed.Empty
) -> Embed:
    """Create an Embed

    Args:
        title (str): Set title
        description (str): Set description
        fields (list of tuples): Set fields
        colour (int, optional): Set color. Defaults to Embed.Empty.
        timestamp (datetime, optional): Set timestamp. Defaults to current time.
        author (str, optional): Set author. Defaults to Embed.Empty.
        author_icon (str, optional): Set author icon using image url. Defaults to Embed.Empty.
        thumbnail (str, optional): Set thumbnail using image url. Defaults to Embed.Empty.
        image (str, optional): Set image using image url. Defaults to Embed.Empty.
        footer (str, optional): Set footer. Defaults to Embed.Empty.

    Returns:
        embed: returns an embed
    """

    embed = Embed(
        title=title,
        description=description,
        colour=colour,
        timestamp=timestamp
    )

    if fields is not Embed.Empty and fields is not None:
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

    embed.set_author(name=author, icon_url=author_icon)
    embed.set_footer(text=footer)
    embed.set_thumbnail(url=thumbnail)
    embed.set_image(url=image)

    return embed
