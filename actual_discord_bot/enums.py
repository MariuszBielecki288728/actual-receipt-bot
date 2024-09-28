import decimal
from enum import IntEnum


class TransactionType(IntEnum):
    DEPOSIT = +1
    PAYMENT = -1

    def get_signed_amount(self, transaction_amount: decimal.Decimal) -> int:
        return transaction_amount * self.value
