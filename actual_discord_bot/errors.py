class ParseNotificationError(RuntimeError):
    def __init__(self, text: str) -> None:
        super().__init__(
            f'Error while parsing notification. "{text}" did not match any regexp.',
        )
