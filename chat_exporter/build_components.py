import discord

from chat_exporter.emoji_convert import convert_emoji
from chat_exporter.build_html import fill_out, component_button, PARSE_MODE_NONE, PARSE_MODE_MARKDOWN, PARSE_MODE_EMOJI


class BuildComponents:
    styles = {
        "primary": "#5865F2",
        "secondary": "grey",
        "success": "#57F287",
        "danger": "#ED4245",
        "blurple": "#5865F2",
        "grey": "grey",
        "gray": "grey",
        "green": "#57F287",
        "red": "#ED4245",
        "link": "grey",
    }

    components: str = ""

    def __init__(self, component, guild):
        self.component = component
        self.guild = guild

    async def build_component(self, c):
        if isinstance(c, discord.Button):
            await self.build_button(c)

    async def build_button(self, c):
        icon = ""
        url = c.url if c.url else ""
        label = c.label if c.label else ""
        emoji = await convert_emoji(str(c.emoji)) if c.emoji else ""
        style = self.styles[str(c.style).split(".")[1]]

        if url:
            icon = (
                ' <img class="chatlog__reference-icon" '
                'src="https://cdn.jsdelivr.net/gh/mahtoid/DiscordUtils@master/discord-external-link.svg"> '
            )
        self.components += await fill_out(self.guild, component_button, [
            ("URL", str(url), PARSE_MODE_NONE),
            ("LABEL", str(label), PARSE_MODE_MARKDOWN),
            ("EMOJI", str(emoji), PARSE_MODE_EMOJI),
            ("ICON", str(icon), PARSE_MODE_NONE),
            ("STYLE", style, PARSE_MODE_NONE)
        ])

    async def flow(self):
        for c in self.component.children:
            await self.build_component(c)
        return self.components
