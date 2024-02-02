from dataclasses import dataclass
from datetime import timedelta

@dataclass
class WattrouterSettings:
    """Class to manage component settings."""

    def __init__(
        self,
        username: str,
        password: str,
        url: str,
        update_interval: timedelta,
    ) -> None:
        """Initialize."""
        self.username = username
        self.password = password
        self.url = url
        self.update_interval = update_interval
