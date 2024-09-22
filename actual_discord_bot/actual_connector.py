from actual import Actual
from actual.queries import create_transaction

from actual_discord_bot.bank_notifications import BankNotification
from actual_discord_bot.config import ActualConfig


class ActualConnector:
    def __init__(self, config: ActualConfig) -> None:
        self.actual_manager = Actual(
            base_url=config.url,
            password=config.password,
            encryption_password=config.encryption_password,
            file=config.file,
        )

    def add_transaction_from_bank_notification(
        self,
        notification: BankNotification,
    ) -> None:
        transaction_data = notification.to_transaction()
        with self.actual_manager as actual:
            create_transaction(
                actual.session,
                date=transaction_data.date,
                account=transaction_data.account,
                amount=transaction_data.amount,
                imported_payee=transaction_data.imported_payee,
                notes=transaction_data.notes,
            )
