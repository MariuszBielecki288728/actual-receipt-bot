import decimal
from dataclasses import dataclass
from datetime import date


@dataclass
class ActualTransactionData:
    date: date
    account: str
    amount: decimal.Decimal | float | int

    imported_payee: str | None = None
    notes: str = ""
