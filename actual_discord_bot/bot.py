import logging
import os

import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

logger = logging.getLogger(__name__)


@bot.event
async def on_ready() -> None:
    logger.info("%s has connected to Discord!", bot.user)


@bot.event
async def on_message(message: discord.Message) -> None:
    if message.author == bot.user:
        return

    await message.channel.send(f"Echo: {message.content}")


def main() -> None:
    bot.run(os.getenv("DISCORD_TOKEN"))


if __name__ == "__main__":
    main()
