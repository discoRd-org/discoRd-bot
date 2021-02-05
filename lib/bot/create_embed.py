from discord import Embed

def create_embed(
	title,
	description,
	fields,
	colour = None,
	timestamp = None,
	author = None,
	author_icon = None,
	thumbnail = None,
	image = None,
	footer = None
):
	"""Create an Embed

	Args:
		title (str): Set title
		description (str): Set description
		fields (tuple): Set fields
		colour (int, optional): Set color. Defaults to None.
		timestamp (datetime, optional): Set timestamp. Defaults to None.
		author (str, optional): Set author. Defaults to None.
		author_icon (str, optional): Set author icon using image url. Defaults to None.
		thumbnail (str, optional): Set thumbnail using image url. Defaults to None.
		image (str, optional): Set image using image url. Defaults to None.
		footer (str, optional): Set footer. Defaults to None.

	Returns:
		embed: returns an embed
	"""

	embed = Embed(
		title=title, 
		description=description, 
		colour=colour,
		timestamp=timestamp
	)

	for name, value, inline in fields:
		embed.add_field(name=name, value=value, inline=inline)

	embed.set_author(name=author, icon_url=author_icon)
	embed.set_footer(text=footer)
	embed.set_thumbnail(url=thumbnail)
	embed.set_image(url=image)

	return embed