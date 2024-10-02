import pytest
from actual import Actual

from actual_discord_bot.bot import ActualDiscordBot


@pytest.fixture
def bot():
    return ActualDiscordBot()


@pytest.fixture
def actual():
    with Actual(
        base_url="http://localhost:6669",
        password="",
        bootstrap=True,
    ) as actual:
        actual.create_budget("TestBudget")
        actual.upload_budget()
        yield actual
        actual.delete_budget()
