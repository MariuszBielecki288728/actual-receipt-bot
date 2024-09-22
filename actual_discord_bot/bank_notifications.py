import decimal
import re
from dataclasses import dataclass
from datetime import UTC, datetime

from babel.numbers import parse_decimal

from actual_discord_bot.dataclasses_definitions import ActualTransactionData


class ParseNotificationError(RuntimeError):
    def __init__(self, text: str) -> None:
        super().__init__(
            f'Error while parsing notification. "{text}" did not match any regexp.',
        )


@dataclass
class BankNotification:
    title: str
    text: str
    timestamp: float

    account: str

    def to_transaction(self) -> ActualTransactionData:
        raise NotImplementedError


@dataclass
class PekaoNotification(BankNotification):
    account: str = "Pekao"

    _regexes = (
        r"Wpłynęło (?P<amount>.+) PLN na konto (?P<account_imported>.+) od (?P<payee>.+). Bank Pekao S.A.",  # Blik przychodzący
    )

    def to_transaction(self) -> ActualTransactionData:
        matched = re.match("|".join(self._regexes), self.text)
        if not matched:
            raise ParseNotificationError(self.text)

        return ActualTransactionData(
            date=datetime.fromtimestamp(float(self.timestamp), tz=UTC).date(),
            account=self.account,
            amount=self._parse_amount(matched.group("amount")),
        )

    @staticmethod
    def _parse_amount(amount: str) -> decimal.Decimal:
        return parse_decimal(amount, locale="pl")
