import environ


@environ.config(prefix="ACTUAL")
class ActualConfig:
    url: str = environ.var(default="http://localhost:5006")
    password: str = environ.var()
    file: str = environ.var()
    encryption_password: str = environ.var(default=None)


@environ.config(prefix="DISCORD")
class DiscordConfig:
    token: str = environ.var()
