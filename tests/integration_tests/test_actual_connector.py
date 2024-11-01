from datetime import UTC, datetime

from actual_discord_bot.actual_connector import ActualConnector
from actual_discord_bot.config import ActualConfig
from actual_discord_bot.dataclasses_definitions import ActualTransactionData


def test_actual_connector(actual):
    connector = ActualConnector(
        ActualConfig(url="http://localhost:12012", password="test", file="TestBudget"),
    )
    connector.save_transaction(
        ActualTransactionData(
            date=datetime.now(tz=UTC).date(),
            account="TestAccount",
            amount=10,
        ),
    )
