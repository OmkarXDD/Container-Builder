import discord
from discord.ext import commands
from discord import ui


async def setup(bot):
    await bot.add_cog(Help(bot))


class HelpView(ui.LayoutView):
    def __init__(self):
        super().__init__(timeout=None)

        container = ui.Container(accent_color=discord.Colour(0xFFFFFF))

        container.add_item(ui.TextDisplay("## ContainerBuilder — Help"))
        container.add_item(ui.Separator())

        container.add_item(ui.TextDisplay(
            "-# Build and send Components V2 containers interactively — "
            "live preview updates as you add and edit components."
        ))
        container.add_item(ui.Separator())

        container.add_item(ui.TextDisplay(
            "**Command**\n"
            "`!container` — aliases: `!build`, `!cb`\n"
            "Opens the builder. A live preview and control panel are sent together."
        ))
        container.add_item(ui.Separator())

        container.add_item(ui.TextDisplay("**Components  (max 20 per container)**"))
        container.add_item(ui.Separator(visible=False))
        container.add_item(ui.TextDisplay(
            "- **Text Display** — a block of text with full markdown support\n"
            "- **Separator** — a visible divider line or an invisible spacer\n"
            "- **Section & Thumbnail** — text alongside an image on the right\n"
            "- **Media Gallery** — up to 10 images in a grid layout\n"
            "- **Button Row** — up to 5 link buttons in a single row"
        ))
        container.add_item(ui.Separator())

        container.add_item(ui.TextDisplay(
            "-# Only the person who ran the command can use the controls.\n"
            "-# The builder times out after 10 minutes of inactivity."
        ))
        container.add_item(ui.Separator())

        container.add_item(ui.ActionRow(
            ui.Button(label="Support", style=discord.ButtonStyle.link, url="https://discord.gg/bewafa"),
            ui.Button(label="ZyroX", style=discord.ButtonStyle.link, url="https://zyrox-black.vercel.app/"),
        ))

        self.add_item(container)


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.remove_command("help")

    @commands.command(name="help", aliases=["h", "cmds", "commands"])
    async def help_command(self, ctx):
        await ctx.send(view=HelpView())
