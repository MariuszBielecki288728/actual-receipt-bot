import asyncio
import os

import discord
from cogwatch import watch
from discord.ext import commands


class ActualDiscordBot(commands.Bot):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)

    @watch(path="actual_discord_bot", preload=True)
    async def on_ready(self) -> None:
        print("Bot ready.")

    async def on_message(self, message: discord.Message) -> None:
        if message.author == self.user:
            return

        await message.channel.send(f"Echo: {message.content}")


async def main() -> None:
    client = ActualDiscordBot()
    await client.start(os.getenv("DISCORD_TOKEN"))


if __name__ == "__main__":
    asyncio.run(main())
