import asyncio
import logging
import sys

import discord
from discord import ui
from discord.ext import commands

import config
from logger import logger

logging.basicConfig(
    level=logging.WARNING,
    format="[%(asctime)s] [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.FileHandler("logs/discord.log")],
)

EXTENSIONS = [
    "commands.help",
    "commands.builder",
]


class ZyroxContext(commands.Context):
    async def fail(self, message: str):
        container = ui.Container(accent_color=None)
        container.add_item(ui.TextDisplay(f"-# {message}"))
        view = ui.LayoutView(timeout=None)
        view.add_item(container)
        await self.send(view=view, allowed_mentions=discord.AllowedMentions.none())


class Zyrox(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True

        super().__init__(
            command_prefix=config.PREFIX,
            intents=intents,
            case_insensitive=True,
        )

    async def get_context(self, message, *, cls=ZyroxContext):
        return await super().get_context(message, cls=cls)

    async def setup_hook(self):
        logger.banner()
        logger.info("INIT", "Zyrox is starting up")
        logger.info("INIT", "Loading extensions")
        for ext in EXTENSIONS:
            try:
                await self.load_extension(ext)
                logger.success("INIT", f"Loaded: {ext}")
            except Exception as e:
                logger.error("INIT", f"Failed to load {ext}: {e}", e)

    async def on_ready(self):
        logger.success("READY", f"Logged in as {self.user} (ID: {self.user.id})")
        logger.info("READY", f"Serving {len(self.guilds)} guild(s)")
        logger.success("READY", "Zyrox is online and ready!")

    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        if self.user in message.mentions and message.content.strip() in (
            f"<@{self.user.id}>",
            f"<@!{self.user.id}>",
        ):
            container = ui.Container(accent_color=None)
            container.add_item(ui.TextDisplay("### ZyroX Container Builder"))
            container.add_item(ui.Separator())
            container.add_item(ui.TextDisplay(
                f"Hey there, {message.author.mention}\n"
                f"Use `{config.PREFIX}container` to build and send Components V2 containers.\n"
                f"Run `{config.PREFIX}help` to see all available commands."
            ))
            container.add_item(ui.Separator())
            container.add_item(ui.TextDisplay(
                "-# Need help? [Join Support](https://discord.gg/bewafa)"
            ))
            view = ui.LayoutView(timeout=None)
            view.add_item(container)
            await message.reply(view=view, allowed_mentions=discord.AllowedMentions.none())
            return

        await self.process_commands(message)

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                f"Missing required argument: `{error.param.name}`. "
                f"Run `{ctx.prefix}help` for usage."
            )
            return
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to use this command.")
            return
        if isinstance(error, commands.BotMissingPermissions):
            await ctx.send("I don't have the required permissions for this command.")
            return
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"This command is on cooldown. Try again in {error.retry_after:.1f}s.")
            return
        logger.error("CMD", f"Unhandled error in {ctx.command}: {error}", error)


async def main():
    token = config.TOKEN
    if not token or token == "your token here":
        logger.error("INIT", "No bot token configured. Set DISCORD_TOKEN in config.py or as an environment variable.")
        sys.exit(1)

    bot = Zyrox()
    async with bot:
        await bot.start(token)


if __name__ == "__main__":
    asyncio.run(main())
