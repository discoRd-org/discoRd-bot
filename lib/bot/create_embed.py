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