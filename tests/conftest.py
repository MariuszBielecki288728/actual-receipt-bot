import pytest

from actual_discord_bot.bot import ActualDiscordBot


@pytest.fixture
def bot():
    return ActualDiscordBot()
